# Manual Query Tool

A tiny, single-file Python CLI to search your **printed manual catalog** with smart, case‑insensitive matching.  
Results are shown in an aligned table with **Title**, **Box**, **Cover**, and **Score** columns.

- **Box-aware**: Items are organized in `BOX 1`, `BOX 2`, or `BOX 3` (or `COVER` for cover-only entries).
- **Cover flag**: Track hi‑res, **cover‑only** prints independently from storage boxes.
- **Smart search**: Substring hits, token overlap, and partial fuzzy matching (great for short queries like `gopro`).
- **Aligned output**: Fixed-width columns for quick scanning in a terminal.
- **No dependencies** beyond Python’s standard library.

> This repository contains a single script: `manual_query.py`

---

## Requirements

- Python **3.8+** (works on Windows/macOS/Linux)
- No third-party packages required

---

## Quick Start

1. Save the script as `manual_query.py` (already provided).
2. Run:
   ```bash
   python manual_query.py
   ```

You’ll see an interactive prompt. Type commands like:

```text
search gopro
search hp 71
list box 3
list cover
exact HP 15C Advanced Functions Handbook
quit
```

---

## Commands

| Command              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `search <text>`      | Smart fuzzy/partial search (case-insensitive). Shows an aligned table.      |
| `exact <title>`      | Exact match (case-insensitive). Shows a single aligned row.                 |
| `list`               | Lists all items grouped by display box (BOX 1/2/3, COVER, UNKNOWN).         |
| `list box 1|2|3`     | Lists only items in the specified box.                                      |
| `list cover`         | Lists all items that have a **cover** (cover flag = Yes).                   |
| `quit`/`exit`        | Exit the tool.                                                              |

---

## Example Output

### Search
```
> search gopro
Matches:
Title                                                             Box       Cover   Score
-----------------------------------------------------------------------------------------
Gopro 10 Black                                                   BOX 2     No       1.00
GOPRO Hero 5 Black                                               BOX 1     No       0.82
GOPRO HERO 12                                                    COVER     Yes      0.77
```

### DGX Example (cover-only item)
```
> search dgx
Matches:
Title                                                             Box       Cover   Score
-----------------------------------------------------------------------------------------
Yamaha dgx-670 owner manual                                      BOX 2     No       1.00
DGX670 Reference                                                 COVER     Yes      1.00
TDS 48GX Suveyin Card User's Manual                              BOX 1     No       0.57
An easy Course using the HP 48GX                                 COVER     Yes      0.57
TDS-48GX Survey Pro User's Manual                                COVER     Yes      0.57
```

### List
```
> list box 3
Title                                                             Box       Cover
----------------------------------------------------------------------------------
Baby Lock BLSA3 embroidery (few pages)                           BOX 3     No   
Denon AVR-760H                                                   BOX 3     No   
HP 41C Math Pac                                                  BOX 3     No   
HP 71 Made Easy                                                  BOX 3     No   
HP 71 Owner Manual                                               BOX 3     No   
HP 71 Reference Manual                                           BOX 3     No   
```

---

## Data Model

The script keeps a simple in‑memory catalog:

```python
# title -> {"box": "BOX 1|BOX 2|BOX 3|None", "cover": bool}
manuals = {
    "Canon EOS R6 Mark II": {"box": "BOX 2", "cover": True},
    "DGX670 Reference":     {"box": None,     "cover": True},  # cover-only => shows Box=COVER
    ...
}
```

- **Box column logic**:  
  - If `box` is set → shows that BOX label.  
  - Else if `cover` is `True` → shows `COVER`.  
  - Else → shows `UNKNOWN`.

- **Output widths** (tweak if you like):  
  ```python
  COL_TITLE = 64
  COL_BOX   = 8
  COL_COVER = 5
  COL_SCORE = 6
  ```

---

## Updating the Catalog

All titles and flags are defined **at the top** of `manual_query.py`:

- To add or move items between boxes: edit the `manuals` dictionary.
- To set/clear cover flags: edit the `cover_items` list (cover-only entries are created automatically).

### Add a New Manual in BOX 2
```python
manuals["New Manual Title"] = {"box": "BOX 2", "cover": False}
```

### Mark an Existing Title as COVER
Add the exact title string to the `cover_items` list (case-insensitive). Example:
```python
cover_items = [
    ...,
    "New Manual Title",  # will set cover=True for this title
]
```

> The script automatically links `cover_items` to existing titles (case-insensitive). If a title isn’t found, it’s created as a **cover-only** entry (Box will display as `COVER`).

---

## Search Details

The search engine combines:
- **Substring** detection (best match)
- **Token overlap** (word-level)
- **Global fuzzy** ratio
- **Partial-window** fuzzy (works when query is a small part of a long title)

This makes short queries (like `gopro`) effective even for long titles.

---

## Troubleshooting

- **“No close matches found.”**  
  Try a slightly longer query (e.g., `hp 12c handbook` instead of `hp 12c`).

- **Wrong or missing box/cover**  
  Edit the `manuals` dictionary (for box) or the `cover_items` list (for cover). Re-run the script.

- **Alignment looks off**  
  Increase `COL_TITLE` (e.g., to `72`) to fit longer titles; adjust other column widths as needed.

---

## Roadmap (Optional Ideas)

- Add `add`, `setbox`, `setcover` interactive commands.
- JSON/CSV import/export of the catalog.
- Unit tests for matching behavior.
- Packaging as a `pipx` app.

---

## License

MIT

