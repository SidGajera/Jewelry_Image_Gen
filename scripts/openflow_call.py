#!/usr/bin/env python3
"""Call an openflow MCP tool from the shell so local files can be sent as base64
without being retyped by the model. Token comes from the registered MCP config
(~/.claude.json) or $OPENFLOW_TOKEN; it is never printed.

  python scripts/openflow_call.py generate_image --prompt-file p.txt \
      --control src.jpg --aspect IMAGE_ASPECT_RATIO_PORTRAIT --out out/shot
"""
import argparse, base64, json, os, sys, time, urllib.request

URL = "https://openflowmcp.com/mcp"

def token():
    t = os.environ.get("OPENFLOW_TOKEN")
    if t:
        return t
    cfg = json.load(open(os.path.expanduser("~/.claude.json")))
    h = cfg["mcpServers"]["openflow"]["headers"]["Authorization"]
    return h.split()[-1]

class Client:
    def __init__(self):
        self.h = {"Authorization": "Bearer " + token(), "Content-Type": "application/json",
                  "Accept": "application/json, text/event-stream"}
        self.id = 0
        r = self.rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                    "clientInfo": {"name": "lucent-script", "version": "1"}})
        self.notify("notifications/initialized")

    def _post(self, body):
        req = urllib.request.Request(URL, json.dumps(body).encode(), self.h)
        resp = urllib.request.urlopen(req, timeout=300)
        sid = resp.headers.get("Mcp-Session-Id")
        if sid:
            self.h["Mcp-Session-Id"] = sid
        raw = resp.read().decode()
        if "text/event-stream" in resp.headers.get("Content-Type", ""):
            for line in raw.splitlines():
                if line.startswith("data:"):
                    return json.loads(line[5:].strip())
            return None
        return json.loads(raw) if raw.strip() else None

    def rpc(self, method, params):
        self.id += 1
        return self._post({"jsonrpc": "2.0", "id": self.id, "method": method, "params": params})

    def notify(self, method):
        self._post({"jsonrpc": "2.0", "method": method})

    def tool(self, name, args):
        r = self.rpc("tools/call", {"name": name, "arguments": args})
        if r is None or "error" in r:
            raise SystemExit("rpc error: %s" % (r and r.get("error")))
        res = r["result"]
        texts = [c["text"] for c in res.get("content", []) if c.get("type") == "text"]
        imgs = [c for c in res.get("content", []) if c.get("type") == "image"]
        if res.get("isError"):
            raise SystemExit("tool error: " + " ".join(texts)[:800])
        return texts, imgs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tool")
    ap.add_argument("--prompt-file")
    ap.add_argument("--control", action="append", default=[])
    ap.add_argument("--aspect", default="IMAGE_ASPECT_RATIO_PORTRAIT")
    ap.add_argument("--model", default="NARWHAL")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--args-json", help="raw JSON args (other tools)")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    c = Client()
    if a.args_json:
        args = json.loads(a.args_json)
    else:
        args = {"prompt": open(a.prompt_file).read(), "aspect": a.aspect, "model": a.model,
                "include_preview": False,
                "control_images": [base64.b64encode(open(p, "rb").read()).decode() for p in a.control] or None}
        if a.seed:
            args["seed"] = a.seed
    texts, imgs = c.tool(a.tool, args)
    for t in texts:
        print(t[:3000])
    for i, im in enumerate(imgs):
        p = "%s_%d.png" % (a.out, i)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        open(p, "wb").write(base64.b64decode(im["data"]))
        print("saved", p)

if __name__ == "__main__":
    main()
