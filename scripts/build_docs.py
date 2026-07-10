#!/usr/bin/env python3
"""Build static documentation site from Markdown sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "web"

PAGES: list[tuple[str, Path, str]] = [
    ("Requirements", DOCS / "requirements.md", "index.html"),
    ("Architecture", DOCS / "architecture.md", "architecture.html"),
    ("Reasoning system", DOCS / "reasoning-system.md", "reasoning-system.html"),
    ("Vision", DOCS / "vision.md", "vision.html"),
    ("Ontology", DOCS / "ontology" / "living-semantic-model.md", "ontology.html"),
]


def _try_markdown(text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "toc", "sane_lists"],
            extension_configs={"toc": {"permalink": True}},
        )
    except ImportError:
        return _fallback_md(text)


def _fallback_md(text: str) -> str:
    """Minimal stdlib conversion when markdown package absent."""
    lines = text.splitlines()
    out: list[str] = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            out.append("<pre><code>" if in_code else "</code></pre>")
            continue
        if in_code:
            out.append(_escape(line))
            continue
        if line.startswith("# "):
            out.append(f"<h1>{_escape(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{_escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{_escape(line[4:])}</h3>")
        elif line.startswith("|") and "|" in line[1:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            tag = "th" if cells and all(set(c) <= set("-: ") for c in cells) is False and "---" in line else "td"
            if "---" in line:
                continue
            if tag == "th" and out and not out[-1].startswith("<table"):
                out.append("<table>")
            if line.startswith("|"):
                out.append("<tr>" + "".join(f"<{tag}>{_escape(c)}</{tag}>" for c in cells) + "</tr>")
        elif line.strip() == "---":
            out.append("<hr>")
        elif line.strip().startswith("- "):
            if not out or not out[-1].endswith("</li>"):
                if out and out[-1] != "<ul>":
                    out.append("<ul>")
            out.append(f"<li>{_inline(_escape(line.strip()[2:]))}</li>")
        elif not line.strip():
            if out and out[-1] == "<ul>":
                pass
            elif out and out[-1].endswith("</li>"):
                out.append("</ul>")
            else:
                out.append("")
        else:
            out.append(f"<p>{_inline(_escape(line))}</p>")
    if out and out[-1].endswith("</li>"):
        out.append("</ul>")
    return "\n".join(out)


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(s: str) -> str:
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def _shell(title: str, body: str, active: str) -> str:
    nav = []
    for label, _, outfile in PAGES:
        href = outfile
        cls = ' class="active"' if label == active else ""
        nav.append(f'<a href="{href}"{cls}>{label}</a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_escape(title)} · Hanani</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <p class="eyebrow">Hanani · Geopolitical reasoning system</p>
      <h1>{_escape(title)}</h1>
      <nav class="nav">{''.join(nav)}</nav>
    </div>
  </header>
  <main class="wrap content">
    {body}
  </main>
  <footer class="site-footer wrap">
    <p>REQ-HANANI-001 · Built from <code>docs/</code> via <code>scripts/build_docs.py</code></p>
  </footer>
</body>
</html>"""


def build() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    css_src = DOCS / "web" / "style.css"
    if not css_src.exists():
        print("warning: style.css missing", file=sys.stderr)

    for title, src, outfile in PAGES:
        if not src.exists():
            print(f"skip missing: {src}", file=sys.stderr)
            continue
        body = _try_markdown(src.read_text(encoding="utf-8"))
        # Fix internal .md links → .html
        for _, _, name in PAGES:
            stem = name.replace(".html", "")
            body = body.replace(f'href="{stem}.md"', f'href="{name}"')
            body = body.replace(f"href=\"{src.name}\"", f'href="{outfile}"')
        html = _shell(title, body, title)
        (OUT / outfile).write_text(html, encoding="utf-8")
        print(f"wrote {OUT / outfile}")

    return 0


if __name__ == "__main__":
    raise SystemExit(build())