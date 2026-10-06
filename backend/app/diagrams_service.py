import os
import re
import json
from typing import Optional, Dict, Any

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
INDEX_PATH = os.path.join(DIAGRAMS_DIR, "index.json")

_LIBRARY_INDEX: Dict[str, Any] = {}
_LIBRARY_SVGS: Dict[str, str] = {}

def _init_library():
    global _LIBRARY_INDEX, _LIBRARY_SVGS
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                _LIBRARY_INDEX = json.load(f)
            for k, meta in _LIBRARY_INDEX.items():
                svg_path = os.path.join(DIAGRAMS_DIR, meta["file"])
                if os.path.exists(svg_path):
                    with open(svg_path, "r", encoding="utf-8") as sf:
                        _LIBRARY_SVGS[k] = sf.read()
        except Exception:
            pass

_init_library()


def find_library_diagram(question: str, subject: str = "", chapter: str = "") -> Optional[Dict[str, Any]]:
    """Matches a question to a curated hand-written SVG diagram from our diagrams/ library."""
    if not _LIBRARY_INDEX:
        _init_library()

    q_low = question.lower()
    ch_low = chapter.lower()

    # Prioritized keyword matching
    for key, meta in _LIBRARY_INDEX.items():
        # Check direct keyword matches in question
        for kw in meta.get("keywords", []):
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", q_low):
                return {
                    "type": "svg_library",
                    "title": meta["title"],
                    "key": key,
                    "data": _LIBRARY_SVGS.get(key, "")
                }

    return None


def sanitize_svg(raw_svg: str) -> str:
    """Strips dangerous scripts, foreignObjects, and event handlers from model-generated SVGs."""
    if not raw_svg:
        return ""
    # Extract only <svg>...</svg> block
    svg_match = re.search(r"<svg[\s\S]*?</svg>", raw_svg, re.IGNORECASE)
    clean = svg_match.group(0) if svg_match else raw_svg
    # Remove script tags
    clean = re.sub(r"<script[\s\S]*?</script>", "", clean, flags=re.IGNORECASE)
    # Remove foreignObject tags
    clean = re.sub(r"<foreignObject[\s\S]*?</foreignObject>", "", clean, flags=re.IGNORECASE)
    # Remove all on* event handler attributes like onclick, onload, onerror
    clean = re.sub(r"\bon\w+\s*=\s*([\"'][^\"']*[\"']|[^\s>]+)", "", clean, flags=re.IGNORECASE)
    # Remove javascript: pseudo-protocol
    clean = re.sub(r"href\s*=\s*[\"']javascript:[^\"']*[\"']", "href=\"#\"", clean, flags=re.IGNORECASE)
    return clean.strip()


def needs_diagram(question: str) -> bool:
    """Returns True if the question explicitly asks to draw, label, plot, sketch, or explain cycles/circuits/processes."""
    q_low = question.lower()
    draw_words = [
        "draw", "sketch", "plot", "label", "diagram", "graph", "flowchart", 
        "circuit", "cycle", "phases", "stages", "process", "water cycle"
    ]
    return any(w in q_low for w in draw_words)
