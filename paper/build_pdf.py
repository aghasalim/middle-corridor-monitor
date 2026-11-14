"""paper.md -> paper.html -> paper.pdf (headless Chrome). Usage: python paper/build_pdf.py [path-to-chrome]"""
import pathlib
import re
import subprocess
import sys

import markdown
from pypdf import PdfReader

HERE = pathlib.Path(__file__).parent
CHROME = sys.argv[1] if len(sys.argv) > 1 else r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CSS = """
@page{size:A4;margin:14mm 15mm}
body{font:9.5pt/1.25 Georgia,'Times New Roman',serif;color:#000}
h1{font-size:17pt;margin:0 0 6pt}h2{font-size:12pt;margin:10pt 0 3pt}h3{font-size:11pt;margin:10pt 0 3pt}
p{margin:0 0 6pt;text-align:justify}img{max-width:100%;max-height:50mm;display:block;margin:4pt auto}img[src*="roro_step"]{max-height:68mm}
table{border-collapse:collapse;font-size:8.5pt;margin:6pt auto}tr{break-inside:avoid}
th,td{border-bottom:.5pt solid #999;padding:2pt 6pt;text-align:right}th:first-child,td:first-child{text-align:left}
code{font-size:9pt}
h2:last-of-type~*{font-size:7.5pt}h2:last-of-type~ul{column-count:2;column-gap:8mm;padding-left:10pt}h2:last-of-type~ul li{break-inside:avoid;word-break:break-word}
"""

md = (HERE / "paper.md").read_text(encoding="utf-8")
# [@key] -> [n], numbered by the order of the reference list at the end of paper.md
num = {k: i + 1 for i, k in enumerate(re.findall(r"^- \[@(\w+)\]", md, flags=re.M))}
md = re.sub(r"\[(@\w+(?:; @\w+)*)\]", lambda m: "[" + ", ".join(str(num[k[1:]]) for k in m.group(1).split("; ")) + "]", md)
body = markdown.markdown(md, extensions=["tables"])
html = f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Middle Corridor Monitor</title><style>{CSS}</style>{body}</html>'
(HERE / "paper.html").write_text(html, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={HERE / 'paper.pdf'}", (HERE / "paper.html").as_uri()], check=True, timeout=120)
print("pages:", len(PdfReader(HERE / "paper.pdf").pages))
