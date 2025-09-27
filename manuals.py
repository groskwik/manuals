import difflib
import re
from typing import Dict, List, Tuple, Optional

# -----------------------------
# Data: title -> box label
# -----------------------------
manuals_by_title: Dict[str, str] = {
    # BOX 1
    "Free42": "BOX 1",
    "Pentax 645D": "BOX 1",
    "HP 48G Advanced user's reference manual": "BOX 1",
    "Nikon Z7 Z6 Reference Manual": "BOX 1",
    "Fujifilm X-T5": "BOX 1",
    "HP 67 EE PAC": "BOX 1",
    "HP 82404A HP IL interface HP 71B": "BOX 1",
    "HP 19C HP 29C Owner Manual": "BOX 1",
    "Canon EOS 4000D": "BOX 1",
    "HP 35S Quick Start Guide": "BOX 1",
    "GOPRO Hero 5 Black": "BOX 1",
    "Baby Lock Coronet": "BOX 1",
    "Baby Lock BLSA3 Embroidery Design Guide": "BOX 1",
    "Nikon D7200": "BOX 1",
    "Getting Started with TI Nspire CX II": "BOX 1",
    "Nikon Coolpix P950 reference manual": "BOX 1",
    "Lowrance Hook 2 series": "BOX 1",
    "PFAFF ICON 1": "BOX 1",
    "HP 75 Forth / Assembler": "BOX 1",
    "TI NSPIRE CX II Guidebook": "BOX 1",
    "HP 82104A Card Reader": "BOX 1",
    "HP 75 Reference Manual": "BOX 1",
    "Tandy Model 100 Reference": "BOX 1",
    "HP 75 Owner Manual": "BOX 1",
    "TDS 48GX Suveyin Card User's Manual": "BOX 1",
    "Lowrance Hook Reveal Series": "BOX 1",
    "HP 12C Solutions Handbook": "BOX 1",
    "HP 12C Platinum Owner and Problem Solving": "BOX 1",
    "Brother xp3 embroidery design guide (beginning only)": "BOX 1",

    # BOX 2
    "Gopro 10 Black": "BOX 2",
    "Tektronix MS022 MSO24": "BOX 2",
    "Bernina 790 Plus": "BOX 2",
    "HP 15C Limited Edition Owner Handbook": "BOX 2",
    "HP 41C P 41CV Owener handbook and Programming Guide": "BOX 2",
    "HP 50G User's Manual": "BOX 2",
    "Canon EOS R6 Mark II": "BOX 2",
    "BlackMagic Pocket Cinema Camera": "BOX 2",
    "Canon EOS 70D": "BOX 2",
    "Sony DSC-H300": "BOX 2",
    "Nikon 3500 Reference Manual": "BOX 2",
    "Nikon D5": "BOX 2",
    "HP 67 Civil Engineering": "BOX 2",
    "HP 71 Owner Manual": "BOX 2",
    "HP 50g advanced user's reference manual": "BOX 2",
    "Brother XP2 Embroidery Design Guide": "BOX 2",
    "Yamaha dgx-670 owner manual": "BOX 2",
    "Canon Powershot SX500 IS": "BOX 2",
    "HP 15C advanced function handbook (half letter)": "BOX 2",
    "Brother XP2 Embroidery": "BOX 2",
    "Singer 7285Q": "BOX 2",
}

# Lowercase index for exact case-insensitive lookup
_lc_index: Dict[str, str] = {t.lower(): t for t in manuals_by_title.keys()}

# --------- Formatting helpers (fixed-width table) ---------
COL_TITLE = 64
COL_BOX = 8
COL_SCORE = 6

def _truncate(s: str, width: int) -> str:
    if len(s) <= width:
        return s
    if width <= 3:
        return s[:width]
    return s[: width - 3] + "..."

def _format_row(title: str, box: str, score: Optional[float]) -> str:
    t = _truncate(title, COL_TITLE)
    b = _truncate(box, COL_BOX)
    if score is None:
        sc = " " * COL_SCORE
    else:
        sc = f"{score:>{COL_SCORE}.2f}"
    return f"{t:<{COL_TITLE}}  {b:<{COL_BOX}}  {sc}"

def _print_header(show_score: bool) -> None:
    title_h = "Title"
    box_h = "Box"
    score_h = "Score" if show_score else ""
    line = f"{title_h:<{COL_TITLE}}  {box_h:<{COL_BOX}}"
    if show_score:
        line += f"  {score_h:>{COL_SCORE}}"
    print(line)
    print("-" * (COL_TITLE + 2 + COL_BOX + (2 + COL_SCORE if show_score else 0)))

def print_table(rows: List[Tuple[str, str, Optional[float]]], show_score: bool) -> None:
    _print_header(show_score)
    for title, box, score in rows:
        print(_format_row(title, box, score))

# --------- Utilities for smarter fuzzy search ---------
_word_re = re.compile(r"[a-z0-9]+")

def normalize(s: str) -> str:
    return " ".join(_word_re.findall(s.lower()))

def tokens(s: str) -> List[str]:
    return _word_re.findall(s.lower())

def token_overlap_score(q_tokens: List[str], c_tokens: List[str]) -> float:
    if not q_tokens:
        return 0.0
    qset, cset = set(q_tokens), set(c_tokens)
    overlap = len(qset & cset)
    return overlap / max(1, len(qset))

def partial_window_ratio(query: str, candidate: str, max_window_words: int = 8) -> float:
    q = normalize(query)
    c = normalize(candidate)
    q_tokens = q.split()
    c_tokens = c.split()
    if not q_tokens or not c_tokens:
        return 0.0
    if q in c:
        return 1.0
    w = min(max(len(q_tokens), 1), max_window_words)
    best = 0.0
    for i in range(0, len(c_tokens)):
        window = " ".join(c_tokens[i:i + w])
        if not window:
            continue
        r = difflib.SequenceMatcher(None, q, window).ratio()
        if r > best:
            best = r
    return best

def composite_score(query: str, candidate: str) -> float:
    q_norm = normalize(query)
    c_norm = normalize(candidate)
    sub = 1.0 if q_norm and q_norm in c_norm else 0.0
    tok = token_overlap_score(tokens(query), tokens(candidate))
    glob = difflib.SequenceMatcher(None, q_norm, c_norm).ratio()
    part = partial_window_ratio(query, candidate)
    return max(sub, part, 0.85 * tok, 0.75 * glob)

# --------- Lookup functions ---------
def exact_lookup(query: str) -> Tuple[str, str] | None:
    key = query.strip().lower()
    if key in _lc_index:
        orig = _lc_index[key]
        return (orig, manuals_by_title[orig])
    return None

def smart_search(query: str, top_n: int = 10, min_score: float = 0.52) -> List[Tuple[str, str, float]]:
    scored: List[Tuple[str, str, float]] = []
    for title, box in manuals_by_title.items():
        s = composite_score(query, title)
        if s >= min_score:
            scored.append((title, box, s))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:top_n]

def list_by_box(box_filter: str | None = None) -> Dict[str, List[str]]:
    by_box: Dict[str, List[str]] = {}
    for title, box in manuals_by_title.items():
        if box_filter and box.lower() != box_filter.lower():
            continue
        by_box.setdefault(box, []).append(title)
    for v in by_box.values():
        v.sort(key=str.lower)
    return by_box

# --------- Interactive CLI ---------
def interactive():
    print("Manual Query Tool (case-insensitive, smarter fuzzy search)")
    print("Commands:")
    print("  search <text>     — fuzzy/partial search (aligned table)")
    print("  exact <title>     — exact (case-insensitive, aligned row)")
    print("  list              — list all grouped by box (aligned tables)")
    print("  list box 1|2      — list a specific box (aligned table)")
    print("  quit              — exit")

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not raw:
            continue
        if raw.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        parts = raw.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd == "list":
            if arg.lower().startswith("box"):
                box = arg.upper().strip()
                grouped = list_by_box(box)
                titles = grouped.get(box, [])
                rows = [(t, box, None) for t in titles]
                if not rows:
                    print(f"No items in {box}.")
                else:
                    print_table(rows, show_score=False)
            else:
                grouped = list_by_box()
                for box in sorted(grouped.keys()):
                    print(f"\n{box}")
                    print_table([(t, box, None) for t in grouped[box]], show_score=False)
            continue

        if cmd == "exact":
            if not arg:
                print("Usage: exact <title>")
                continue
            res = exact_lookup(arg)
            if res:
                t, b = res
                print_table([(t, b, None)], show_score=False)
            else:
                print("No exact (case-insensitive) match.")
            continue

        if cmd == "search":
            if not arg:
                print("Usage: search <text>")
                continue
            # Show exact (if any) first as a single row, then matches
            res = exact_lookup(arg)
            if res:
                print("Exact match:")
                t, b = res
                print_table([(t, b, 1.00)], show_score=True)

            matches = smart_search(arg)
            if matches:
                print("Matches:")
                print_table(matches, show_score=True)
            else:
                print("No close matches found.")
            continue

        # Fallback: treat line as a search
        matches = smart_search(raw)
        if matches:
            print("Matches:")
            print_table(matches, show_score=True)
        else:
            print("No close matches found.")

if __name__ == "__main__":
    interactive()
