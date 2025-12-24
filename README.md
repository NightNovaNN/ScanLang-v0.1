# ScanLang

A tiny Python tool that analyzes a GitHub repository and outputs the **language distribution** based on **file extensions**.

* No cloning
* No guessing frameworks
* Pure, deterministic JSON output

---

## What it does

* Scans a GitHub repo via the GitHub API
* Counts source files by language (`.c`, `.cpp`, `.py`, `.f`, etc.)
* Calculates percentage share per language
* Ignores docs and config files

---

## Output example

```json
{
  "total_files": 5,
  "languages": {
    "C": { "files": 1, "percentage": 20.0 },
    "C++": { "files": 1, "percentage": 20.0 },
    "Fortran": { "files": 1, "percentage": 20.0 },
    "Python": { "files": 1, "percentage": 20.0 },
    "C/C++ Header": { "files": 1, "percentage": 20.0 }
  }
}
```

---

## Usage

1. Put a GitHub repo URL in `scan.py`
2. (Recommended) add a GitHub token to avoid rate limits
3. Run:

```bash
python scan.py > data.json
```

---

## Notes

* Percentages are file-based, not LOC-based
* Designed to work on mixed-language and non-standard repos

---

