"""cad_render.py — render catalog angles straight from the master CAD (Blender headless).

Why this exists: nano_banana re-synthesises the ring every frame, so any camera move
invents head/gallery/prong geometry (docs/07 Catalog 0152 FAILURE MEMORY 001-010).
Rendering the angles from the CAD makes geometry exact BY CONSTRUCTION; AI then only
supplies cloth, logo, lighting and lifestyle scenes.

Metal comes from the SKU's .stl (the casting mesh — exact CAD vertices).
The centre stone is NOT in the .stl, so it is built as a standard round brilliant at the
diameter/height/centre read from the .3dm gem layer (see cad_probe.py). Placement is CAD
truth; only the cut's facet proportions are standard.

Run:
  blender --background --factory-startup --python scripts/cad_render.py -- \
      --stl workspace/golden/LR-0152/109.stl \
      --gem 8.85,5.177,0,0,12.852 \
      --out workspace/cad_renders/LR-0152 \
      --angles front,three_quarter,side,rear
"""
import argparse
import math
import os
import sys

import bpy
import bmesh
from mathutils import Vector

# Standard round-brilliant proportions, as fractions of girdle diameter.
TABLE_PCT = 0.57
CROWN_H = 0.162
GIRDLE_H = 0.030
PAVILION_D = 0.431

# Catalog angles: (yaw°, pitch°) with the ring standing upright, 0° = straight-on front.
ANGLES = {
    "front": (0.0, 8.0),
    "three_quarter": (40.0, 30.0),
    "side": (90.0, 8.0),
    "rear": (180.0, 25.0),
    "top": (0.0, 88.0),
}


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--stl", required=True)
    p.add_argument("--gem", required=True,
                   help="dia,height,cx,cy,cz in CAD units (from the .3dm gem layer)")
    p.add_argument("--out", required=True)
    p.add_argument("--angles", default="front,three_quarter,side,rear")
    p.add_argument("--res", type=int, default=2048)
    p.add_argument("--samples", type=int, default=256)
    return p.parse_args(argv)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def gold_material():
    m = bpy.data.materials.new("18K_Yellow_Gold")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1.0, 0.766, 0.336, 1.0)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = 0.08
    return m


def diamond_material():
    m = bpy.data.materials.new("Diamond")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    b.inputs["Roughness"].default_value = 0.0
    b.inputs["IOR"].default_value = 2.417          # real diamond
    b.inputs["Transmission Weight"].default_value = 1.0
    return m


def build_round_brilliant(dia, height, centre):
    """A true 57-facet round brilliant sized to the CAD's gem bounds, centred on `centre`.

    Facets: table + 8 bezel + 8 star + 16 upper-girdle + girdle band
            + 16 lower-girdle + 8 pavilion mains (+ culet point) = 57.
    Proportions are the industry standard; the DIAMETER, HEIGHT and CENTRE come from
    the SKU's .3dm gem layer, so placement is CAD truth.
    """
    r = dia / 2.0
    span = CROWN_H + GIRDLE_H + PAVILION_D
    crown = height * (CROWN_H / span)
    girdle = height * (GIRDLE_H / span)
    pav = height * (PAVILION_D / span)

    z_g_lo = 0.0
    z_g_hi = girdle
    z_table = girdle + crown
    z_culet = -pav
    table_r = r * TABLE_PCT
    star_r = r * 0.80            # star tips sit ~80% out on the crown
    z_star = girdle + crown * 0.42

    def polar(rad, ang, z):
        return (math.cos(ang) * rad, math.sin(ang) * rad, z)

    bm = bmesh.new()
    A8 = [2 * math.pi * i / 8 for i in range(8)]          # bezel / main axes
    A16 = [2 * math.pi * i / 16 for i in range(16)]       # girdle points

    T = [bm.verts.new(polar(table_r, a, z_table)) for a in A8]
    S = [bm.verts.new(polar(star_r, a + math.pi / 8, z_star)) for a in A8]
    Ghi = [bm.verts.new(polar(r, a, z_g_hi)) for a in A16]
    Glo = [bm.verts.new(polar(r, a, z_g_lo)) for a in A16]
    culet = bm.verts.new((0.0, 0.0, z_culet))

    bm.faces.new(T)                                        # table (octagon)
    for i in range(8):
        j = (i + 1) % 8
        bm.faces.new((T[i], S[i], T[j]))                   # 8 star facets
        bm.faces.new((T[i], Ghi[(2 * i - 1) % 16], Ghi[2 * i], S[i]))  # 8 bezels
        bm.faces.new((S[i], Ghi[2 * i], Ghi[2 * i + 1]))               # upper girdle
        bm.faces.new((S[i], Ghi[2 * i + 1], Ghi[(2 * i + 2) % 16]))    # upper girdle
    for i in range(16):
        j = (i + 1) % 16
        bm.faces.new((Glo[i], Glo[j], Ghi[j], Ghi[i]))     # girdle band
        bm.faces.new((Glo[j], Glo[i], culet))              # pavilion mains + lower girdle

    # The .3dm gives the gem's BOUNDING-BOX centre, so centre this mesh on its bbox
    # before placing it — otherwise the stone seats low by (pav - crown)/2.
    dz = (z_table + z_culet) / 2.0
    for v in bm.verts:
        v.co.z -= dz

    me = bpy.data.meshes.new("CentreStone")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("CentreStone", me)
    bpy.context.collection.objects.link(ob)
    ob.location = Vector(centre)
    ob.data.materials.append(diamond_material())
    for poly in ob.data.polygons:      # flat facets — a diamond has no smooth shading
        poly.use_smooth = False
    return ob


def import_metal(stl_path):
    try:
        bpy.ops.wm.stl_import(filepath=stl_path)          # Blender 4.2+
    except AttributeError:
        bpy.ops.import_mesh.stl(filepath=stl_path)        # older
    obs = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    mat = gold_material()
    for o in obs:
        o.data.materials.clear()
        o.data.materials.append(mat)
    return obs


def studio_lighting(radius):
    """Neutral white studio: even ambient for the gold, three softboxes for facet contrast."""
    world = bpy.data.worlds.new("W")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

    scale = radius * radius
    for name, loc, energy, size in [
        ("Key", (radius * 2.2, -radius * 2.0, radius * 2.6), 900 * scale, radius * 2),
        ("Fill", (-radius * 2.4, -radius * 1.4, radius * 1.2), 300 * scale, radius * 3),
        ("Rim", (0.0, radius * 3.0, radius * 2.0), 500 * scale, radius * 2),
    ]:
        d = bpy.data.lights.new(name, type="AREA")
        d.energy, d.size = energy, size
        ob = bpy.data.objects.new(name, d)
        ob.location = loc
        bpy.context.collection.objects.link(ob)
        track = ob.constraints.new("TRACK_TO")
        track.target = bpy.data.objects["Target"]


def setup_camera(target, radius):
    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 100                      # macro-ish compression, real product look
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    return cam


def place_camera(cam, centre, yaw, pitch, dist):
    ry, rp = math.radians(yaw), math.radians(pitch)
    cam.location = (
        centre.x + dist * math.cos(rp) * math.sin(ry),
        centre.y - dist * math.cos(rp) * math.cos(ry),
        centre.z + dist * math.sin(rp),
    )


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    a = parse_args(argv)

    clear_scene()
    metal = import_metal(a.stl)
    if not metal:
        raise SystemExit("no mesh imported from " + a.stl)

    dia, h, cx, cy, cz = (float(v) for v in a.gem.split(","))
    build_round_brilliant(dia, h, (cx, cy, cz))

    # Frame on the whole ring.
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    for o in metal:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector((min(mins[i], w[i]) for i in range(3)))
            maxs = Vector((max(maxs[i], w[i]) for i in range(3)))
    centre = (mins + maxs) / 2
    radius = (maxs - mins).length / 2

    tgt = bpy.data.objects.new("Target", None)
    tgt.location = centre
    bpy.context.collection.objects.link(tgt)

    studio_lighting(radius)
    cam = setup_camera(tgt, radius)

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = a.samples
    sc.cycles.use_denoising = True
    try:
        sc.cycles.device = "GPU"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.get_devices()
        for dev in prefs.devices:
            dev.use = dev.type != "CPU"
    except Exception:
        sc.cycles.device = "CPU"
    sc.render.resolution_x = sc.render.resolution_y = a.res
    sc.render.film_transparent = True            # AI supplies cloth/scene behind it
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"

    os.makedirs(a.out, exist_ok=True)
    for name in a.angles.split(","):
        if name not in ANGLES:
            raise SystemExit("unknown angle: " + name)
        yaw, pitch = ANGLES[name]
        place_camera(cam, centre, yaw, pitch, radius * 5.5)
        sc.render.filepath = os.path.join(a.out, name + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", sc.render.filepath)


if __name__ == "__main__":
    main()
