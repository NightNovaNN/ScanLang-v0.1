import requests
import os
import json
from collections import defaultdict
from urllib.parse import urlparse

# ---------------- CONFIG ----------------

EXTENSION_MAP = {
    ".py": "Python",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++ Header",
    ".java": "Java",
    ".rs": "Rust",
    ".go": "Go",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".f": "Fortran",
    ".f90": "Fortran",
    ".f95": "Fortran",
    ".anl": "Antilang",
    ".c25": "Cryo"
}

IGNORE_DIRS = {
    "node_modules", "dist", "build", ".git",
    "__pycache__", ".venv", "venv"
}

# ----------------------------------------


def parse_github_url(url: str):
    parts = urlparse(url).path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub repo URL")
    return parts[0], parts[1]


def analyze_repo(owner: str, repo: str) -> dict:
    lang_counts = defaultdict(int)
    total_files = 0

    def walk(path=""):
        nonlocal total_files

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(api_url)
        response.raise_for_status()

        for item in response.json():
            if item["type"] == "dir":
                if item["name"] not in IGNORE_DIRS:
                    walk(item["path"])

            elif item["type"] == "file":
                _, ext = os.path.splitext(item["name"])
                ext = ext.lower()

                # count ONLY known code extensions
                if ext in EXTENSION_MAP:
                    total_files += 1
                    lang = EXTENSION_MAP[ext]
                    lang_counts[lang] += 1

    walk()

    languages = {}
    for lang, count in lang_counts.items():
        percentage = round((count / total_files) * 100, 2) if total_files else 0
        languages[lang] = {
            "files": count,
            "percentage": percentage
        }

    return {
        "total_files": total_files,
        "languages": languages
    }


if __name__ == "__main__":
    repo_url = "https://github.com/NightNovaNN/AntiLang-vAlpha"  # put repo link here
    owner, repo = parse_github_url(repo_url)

    result = analyze_repo(owner, repo)
    print(json.dumps(result, indent=2))
