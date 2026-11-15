"""Local page for hand-labelling the Sentinel-1 chips in data/sar/label_sample.csv.

Run:  .venv/Scripts/python research/label_tool.py [--check]   then open http://127.0.0.1:8765
      --check shows only the 50 chips of the human check sample (data/sar/model_labels.csv, human_check = 1).
Every answer is written straight into label_sample.csv (only is_vessel, n_vessels_seen, note change),
so you can stop and resume at any time. The page shows only the chip, its kind and zone: no detector
score, no suggested label, so the labels stay an independent human check.
"""
import csv
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SAR = Path(__file__).resolve().parents[1] / "data" / "sar"
CSV_PATH = SAR / "label_sample.csv"
CHIPS = SAR / "label_chips"
LABEL_COLS = ("is_vessel", "n_vessels_seen", "note")
SHOWN = ("sample_id", "kind", "zone", "chip_file") + LABEL_COLS  # nothing else reaches the page


def read_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        return header, [dict(zip(header, row)) for row in r]


def write_rows(header, rows):
    tmp = CSV_PATH.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")  # same layout pandas wrote on Windows
        w.writerow(header)
        w.writerows([row[c] for c in header] for row in rows)
    os.replace(tmp, CSV_PATH)  # atomic: a crash never leaves a half-written sheet


def clean(kind, data):
    """Validate one answer; raises ValueError on anything unexpected."""
    v = str(data.get("is_vessel", "")).strip()
    n = str(data.get("n_vessels_seen", "")).strip()
    note = " ".join(str(data.get("note", "")).split())[:500]
    if v not in ("", "yes", "no", "unsure"):
        raise ValueError("is_vessel must be yes, no or unsure")
    if n and not (n.isdigit() and int(n) <= 99):
        raise ValueError("n_vessels_seen must be a whole number 0-99")
    if kind == "detection" and n or kind == "empty_tile" and v:
        raise ValueError("wrong field for this kind of chip")
    return {"is_vessel": v, "n_vessels_seen": n, "note": note}


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            return self.send(200, PAGE, "text/html; charset=utf-8")
        if self.path == "/rows":
            _, rows = read_rows()
            rows = [r for r in rows if CHECK is None or r["sample_id"] in CHECK]
            return self.send(200, json.dumps([{c: r[c] for c in SHOWN} for r in rows]))
        m = re.fullmatch(r"/label_chips/(S\d{4}\.png)", self.path)
        if m and (CHIPS / m[1]).is_file():
            return self.send(200, (CHIPS / m[1]).read_bytes(), "image/png")
        self.send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/save":
            return self.send(404, "not found", "text/plain")
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            header, rows = read_rows()
            row = next(r for r in rows if r["sample_id"] == data.get("sample_id"))
            row.update(clean(row["kind"], data))
            write_rows(header, rows)
        except (ValueError, StopIteration, json.JSONDecodeError) as e:
            return self.send(400, json.dumps({"error": str(e) or "unknown sample_id"}))
        self.send(200, json.dumps({c: row[c] for c in SHOWN}))

    def log_message(self, *a):
        pass


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Alat radar labels</title>
<style>
body{margin:0;background:#111;color:#eee;font:15px/1.4 system-ui,sans-serif}
main{max-width:1200px;margin:0 auto;padding:16px}
img{width:100%;image-rendering:pixelated;background:#000;display:block}
.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:10px 0}
button{background:#333;color:#eee;border:1px solid #555;border-radius:6px;padding:8px 14px;font:inherit;cursor:pointer}
button.on{background:#2d6cdf;border-color:#2d6cdf}
input{background:#222;color:#eee;border:1px solid #555;border-radius:6px;padding:8px;font:inherit}
#note{flex:1;min-width:240px} #count{width:70px}
.q{font-size:18px;font-weight:600} .muted{color:#999} #msg{color:#f77}
kbd{background:#333;border-radius:4px;padding:0 5px} [hidden]{display:none!important}
</style></head><body><main>
<div class="bar"><span id="pos" class="q"></span><span id="meta" class="muted"></span><span id="prog" class="muted"></span><span id="saved" class="muted"></span></div>
<img id="chip" alt="radar chip">
<div class="bar" id="det">
 <span class="q">Is the object at the centre (yellow ticks) a vessel?</span>
 <button data-v="yes">Vessel <kbd>Y</kbd></button><button data-v="no">Not a vessel <kbd>N</kbd></button>
 <button data-v="unsure">Unsure <kbd>U</kbd></button><button data-v="">Clear</button>
</div>
<div class="bar" id="emp">
 <span class="q">How many vessels do you see in this tile? (0 if none)</span>
 <input id="count" type="number" min="0" max="99" step="1" aria-label="vessels seen"> <span class="muted">type a number, Enter = save and next</span>
</div>
<div class="bar"><input id="note" placeholder="note (optional), Enter = save and next" aria-label="note"></div>
<div class="bar">
 <button id="prev">&larr; Back</button><button id="next">Next &rarr;</button><button id="skip">First unlabelled</button>
 <span class="muted">Keys: <kbd>Y</kbd>/<kbd>N</kbd>/<kbd>U</kbd> answer and go on, <kbd>&larr;</kbd>/<kbd>&rarr;</kbd> move, <kbd>/</kbd> note. Every answer is saved to label_sample.csv at once.</span>
</div>
<div id="msg"></div>
</main><script>
let rows=[], i=0;
const $=id=>document.getElementById(id);
const done=r=>r.kind==="detection"?r.is_vessel!=="":r.n_vessels_seen!=="";
async function save(patch){
  const r=rows[i], body={sample_id:r.sample_id,is_vessel:r.is_vessel,n_vessels_seen:r.n_vessels_seen,note:r.note,...patch};
  const res=await fetch("/save",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const j=await res.json();
  if(!res.ok){$("msg").textContent="NOT saved: "+j.error;return false}
  rows[i]=j;$("msg").textContent="";$("saved").textContent="saved "+j.sample_id;return true;
}
function show(){
  const r=rows[i], n=rows.filter(done).length;
  $("chip").src="/"+r.chip_file;
  $("pos").textContent=r.sample_id+" ("+(i+1)+" of "+rows.length+")";
  $("meta").textContent=(r.kind==="detection"?"detection":"tile with no detection")+", "+r.zone;
  const z=k=>rows.filter(x=>x.kind===k[0]&&x.zone===k[1]);
  $("prog").textContent="labelled "+n+"/"+rows.length+" | "+[["detection","roadstead"],["detection","basin"],["empty_tile","roadstead"],["empty_tile","basin"]]
    .map(k=>k[0].replace("empty_tile","empty")+" "+k[1]+" "+z(k).filter(done).length+"/"+z(k).length).join(", ");
  $("det").hidden=r.kind!=="detection"; $("emp").hidden=r.kind!=="empty_tile";
  document.querySelectorAll("#det button").forEach(b=>b.classList.toggle("on",b.dataset.v!==""&&b.dataset.v===r.is_vessel));
  $("count").value=r.n_vessels_seen; $("note").value=r.note;
  if(r.kind==="empty_tile")$("count").focus(); else document.activeElement.blur();
}
const go=d=>{i=Math.max(0,Math.min(rows.length-1,i+d));show()};
const firstOpen=()=>{const k=rows.findIndex(r=>!done(r));i=k<0?0:k;show()};
async function answer(v){if(await save({is_vessel:v,note:$("note").value}))go(1)}
document.querySelectorAll("#det button").forEach(b=>b.onclick=()=>answer(b.dataset.v));
$("prev").onclick=()=>go(-1); $("next").onclick=()=>go(1); $("skip").onclick=firstOpen;
for(const id of ["count","note"])$(id).addEventListener("keydown",async e=>{
  if(e.key!=="Enter")return; e.preventDefault();
  const p={note:$("note").value}; if(rows[i].kind==="empty_tile")p.n_vessels_seen=$("count").value;
  if(await save(p))go(1);
});
document.addEventListener("keydown",e=>{
  if(e.target.tagName==="INPUT")return;
  const k=e.key.toLowerCase(), det=rows[i].kind==="detection";
  if(det&&k==="y")answer("yes"); else if(det&&k==="n")answer("no"); else if(det&&k==="u")answer("unsure");
  else if(e.key==="ArrowLeft")go(-1); else if(e.key==="ArrowRight")go(1);
  else if(e.key==="/"){e.preventDefault();$("note").focus()}
});
fetch("/rows").then(r=>r.json()).then(j=>{rows=j;firstOpen()});
</script></body></html>"""

def check_ids():
    """The fixed 50-chip human check sample; only the human_check flag is read, never the model's labels."""
    with open(SAR / "model_labels.csv", newline="", encoding="utf-8") as f:
        return {r["sample_id"] for r in csv.DictReader(f) if r["human_check"] == "1"}


CHECK = None  # None = all 314 chips; --check = only the 50-chip agreement sample

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--check"]
    if "--check" in sys.argv:
        CHECK = check_ids()
    port = int(args[0]) if args else 8765
    print(f"Labelling page: http://127.0.0.1:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
