"""
rhino_build.py  —  design-DNA  ->  production CAD (.3dm / .stl)

STUB / SPEC. This is the layer-3 bridge that runs INSIDE Rhino (RhinoPython) or
via rhino3dm + Grasshopper. It is deliberately a documented skeleton: the actual
NURBS operations require the Rhino runtime. The point is the deterministic
"parameters -> geometry" mapping — the geometry is CONSTRUCTED, never AI-drawn,
so it cannot drift and is manufacturable by construction.

Run inside Rhino:   RunPythonScript rhino_build.py  <design.json>
Headless option:    pip install rhino3dm  (subset of ops) or drive Grasshopper via GH_CPython.

--------------------------------------------------------------------------------
PARAMETER -> GEOMETRY MAP  (what each design-DNA field builds)
--------------------------------------------------------------------------------
centre.cut          -> load matching stone model from /stone-library/<cut>.3dm (real facets)
centre.carat + lw   -> scale stone to finished mm (see manufacturability.stone_mm)
centre.orientation  -> rotate stone 90deg for east_west
centre.setting
  prong             -> N cylinders Ø prong_dia_mm on the girdle at even angles, tipped over crown
  bezel             -> offset girdle outward by bezel_wall_mm, extrude bezel_height, inner seat ledge
composition
  solitaire         -> single head on shank
  hidden_halo       -> circular array of melee seats under the crown (peek-a-boo)
  toi_et_moi        -> second stone placed at bypass offset; two shanks cross
  three_stone       -> two accent heads flanking, shared gallery rail
band.profile+width  -> sweep the profile curve along the shank rails
  knife_edge        -> V profile ; round -> D profile ; cigar -> wide domed profile
FINALISE            -> boolean-union heads to shank; subtract stone seats; fillet stress points
EXPORT              -> <sku>.3dm (NURBS master) + <sku>.stl (print) + <sku>.png (Rhino render)
--------------------------------------------------------------------------------
"""
import json, sys

# import rhinoscriptsyntax as rs   # available only inside Rhino
# import Rhino.Geometry as rg


def build(dna):
    steps = []
    c = dna["centre"]
    steps.append(f"load stone: /stone-library/{c['cut']}.3dm")
    steps.append(f"scale stone to carat={c['carat']} lw={c['lw']} "
                 f"(orientation={c.get('orientation','north_south')})")
    if c["setting"] == "prong":
        steps.append(f"array {c.get('prongs',4)} prongs Ø{c.get('prong_dia_mm',1.2)}mm on girdle")
    else:
        steps.append(f"bezel: offset girdle +{c.get('bezel_wall_mm',0.8)}mm, extrude, cut seat")
    comp = dna["composition"]
    if comp == "hidden_halo":
        steps.append("array melee seats under crown (hidden halo)")
    elif comp == "toi_et_moi":
        steps.append("place 2nd stone at bypass offset; build crossing shanks")
    elif comp == "three_stone":
        steps.append("place 2 accent heads on shared gallery rail")
    b = dna["band"]
    steps.append(f"sweep {b['profile']} profile ({b['width_mm']}mm) along shank rails")
    steps.append("boolean union heads->shank; subtract seats; fillet")
    sku = dna.get("sku", "design")
    steps.append(f"export {sku}.3dm + {sku}.stl + {sku}.png")
    return steps


def main(path):
    with open(path) as f:
        dna = json.load(f)
    print(f"# build plan for {dna.get('sku') or path}")
    for i, s in enumerate(build(dna), 1):
        print(f"  {i:2}. {s}")
    print("\n(STUB — connect to Rhino/Grasshopper to emit real .3dm/.stl. "
          "See cad/grasshopper/README.md.)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    main(sys.argv[1])
