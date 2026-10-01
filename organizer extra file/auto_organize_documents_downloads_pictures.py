#!/usr/bin/env python3
"""One-click organizer for Documents, Downloads, and Pictures."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tkinter as tk
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from tkinter import messagebox

APP_TITLE = "Auto File Organizer"
OUTPUT_FOLDER = "Organized Files"
LOG_FOLDER = ".auto_organizer_logs"
MAX_HASH_SIZE = 100 * 1024 * 1024
MAX_TEXT_SIZE = 1_500_000

TEXT_EXTENSIONS = {
    ".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm", ".css",
    ".js", ".ts", ".py", ".java", ".c", ".cpp", ".h", ".hpp", ".cs",
    ".ini", ".cfg", ".log", ".yaml", ".yml", ".sql"
}

TYPE_GROUPS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".heic", ".tif", ".tiff"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm", ".wmv", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".opus", ".wma"},
    "Documents": {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".epub"},
    "Spreadsheets": {".xls", ".xlsx", ".ods", ".csv", ".tsv"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Archives": {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"},
    "Programs": {".exe", ".msi", ".msix", ".appx", ".apk"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".sql"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
    "3D Models": {".obj", ".fbx", ".stl", ".gltf", ".glb", ".blend"},
}

STOP_WORDS = {"the", "and", "for", "from", "with", "this", "that", "copy", "final", "new", "old", "file"}


def find_standard_folder(name: str) -> Path | None:
    """Find a standard Windows folder, including common OneDrive locations."""
    home = Path.home()
    candidates = [
        home / name,
        home / "OneDrive" / name,
        home / "OneDrive - Personal" / name,
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    return None


def type_group(extension: str) -> str:
    for group, extensions in TYPE_GROUPS.items():
        if extension in extensions:
            return group
    return f"{extension[1:].upper()} Files" if extension else "Files Without Extension"


def clean_name(path: Path) -> str:
    name = path.stem.lower()
    name = re.sub(r"\b(copy|final|draft|edited|new|old)\b", " ", name)
    name = re.sub(r"\(\d+\)|\[\d+\]|[_\-.]+|\b\d+\b", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def words(path: Path) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{3,}", clean_name(path)) if w not in STOP_WORDS}


def safe_folder_name(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:60].rstrip(" .") or "Related Files"


def digest(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_HASH_SIZE:
            return ""
        result = hashlib.sha256()
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                result.update(chunk)
        return result.hexdigest()
    except OSError:
        return ""


def text_fingerprint(path: Path) -> set[str]:
    try:
        if path.suffix.lower() not in TEXT_EXTENSIONS or path.stat().st_size > MAX_TEXT_SIZE:
            return set()
        text = path.read_bytes().decode("utf-8", errors="ignore").lower()
        tokens = [w for w in re.findall(r"[a-z0-9]{3,}", text) if w not in STOP_WORDS]
        return {" ".join(tokens[i:i + 3]) for i in range(max(0, len(tokens) - 2))}
    except OSError:
        return set()


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def unique_path(path: Path) -> Path:
    candidate = path
    number = 2
    while candidate.exists():
        candidate = path.with_name(f"{path.stem} ({number}){path.suffix}")
        number += 1
    return candidate


def gather_files(root: Path, script_path: Path) -> list[Path]:
    output = root / OUTPUT_FOLDER
    logs = root / LOG_FOLDER
    result = []
    for path in root.rglob("*"):
        try:
            resolved = path.resolve()
            if not path.is_file() or path.is_symlink() or resolved == script_path:
                continue
            if output in resolved.parents or logs in resolved.parents:
                continue
            if any(part.startswith(".") for part in resolved.relative_to(root).parts):
                continue
            result.append(resolved)
        except (OSError, PermissionError, ValueError):
            continue
    return result


def organize_directory(root: Path, script_path: Path) -> tuple[int, list[str], Path | None]:
    files = gather_files(root, script_path)
    if not files:
        return 0, [], None

    metadata = []
    for path in files:
        metadata.append({
            "path": path,
            "name": clean_name(path),
            "words": words(path),
            "hash": digest(path),
            "text": text_fingerprint(path),
            "type": type_group(path.suffix.lower()),
        })

    parent = list(range(len(metadata)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    hashes = defaultdict(list)
    for i, item in enumerate(metadata):
        if item["hash"]:
            hashes[item["hash"]].append(i)
    duplicate_ids = set()
    for ids in hashes.values():
        if len(ids) > 1:
            duplicate_ids.update(ids)
            for i in ids[1:]:
                union(ids[0], i)

    content_ids = set()
    name_ids = set()
    for i in range(len(metadata)):
        for j in range(i + 1, len(metadata)):
            a, b = metadata[i], metadata[j]
            same_type = a["type"] == b["type"]
            name_score = SequenceMatcher(None, a["name"], b["name"]).ratio() if a["name"] and b["name"] else 0
            word_score = jaccard(a["words"], b["words"])
            content_score = jaccard(a["text"], b["text"])
            if content_score >= 0.68:
                union(i, j)
                content_ids.update((i, j))
            elif same_type and (name_score >= 0.76 or word_score >= 0.5):
                union(i, j)
                name_ids.update((i, j))

    clusters = defaultdict(list)
    for i in range(len(metadata)):
        clusters[find(i)].append(i)

    moved = []
    errors = []
    output = root / OUTPUT_FOLDER
    for ids in clusters.values():
        items = [metadata[i] for i in ids]
        if len(ids) > 1:
            common = Counter(word for item in items for word in item["words"]).most_common(3)
            label = safe_folder_name(" ".join(word.title() for word, _ in common) or items[0]["type"])
            if all(i in duplicate_ids for i in ids):
                destination_folder = output / "Duplicates" / label
            elif any(i in content_ids for i in ids):
                destination_folder = output / "Related by Content" / label
            else:
                destination_folder = output / "Related by Name" / label
        else:
            destination_folder = output / "By Type" / safe_folder_name(items[0]["type"])

        for item in items:
            source = item["path"]
            try:
                destination_folder.mkdir(parents=True, exist_ok=True)
                destination = unique_path(destination_folder / source.name)
                shutil.move(str(source), str(destination))
                moved.append({"source": str(source), "destination": str(destination)})
            except Exception as exc:
                errors.append(f"{source.name}: {exc}")

    if moved:
        log_dir = root / LOG_FOLDER
        log_dir.mkdir(exist_ok=True)
        log_path = log_dir / f"organize_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path.write_text(json.dumps({"moves": moved}, indent=2), encoding="utf-8")
    else:
        log_path = None
    return len(moved), errors, log_path


def main() -> None:
    root_window = tk.Tk()
    root_window.withdraw()

    answer = messagebox.askyesno(
        APP_TITLE,
        "Automatically organize all files in these folders?\n\n"
        "• Documents\n"
        "• Downloads\n"
        "• Pictures\n\n"
        "Files will be placed inside an 'Organized Files' folder in each location.\n"
        "Click Yes to begin or No to cancel."
    )
    if not answer:
        root_window.destroy()
        return

    folders = []
    missing = []
    for name in ("Documents", "Downloads", "Pictures"):
        folder = find_standard_folder(name)
        if folder:
            folders.append((name, folder))
        else:
            missing.append(name)

    if not folders:
        messagebox.showerror(APP_TITLE, "Documents, Downloads, and Pictures could not be found.")
        root_window.destroy()
        return

    script_path = Path(__file__).resolve()
    total_moved = 0
    all_errors = []
    results = []

    for name, folder in folders:
        moved, errors, _ = organize_directory(folder, script_path)
        total_moved += moved
        all_errors.extend(f"{name}: {error}" for error in errors)
        results.append(f"{name}: {moved} file(s) organized")

    summary = "Organization finished!\n\n" + "\n".join(results)
    summary += f"\n\nTotal: {total_moved} file(s) organized."
    if missing:
        summary += "\n\nNot found: " + ", ".join(missing)
    if all_errors:
        summary += f"\n\n{len(all_errors)} file(s) could not be moved."
    messagebox.showinfo(APP_TITLE, summary)
    root_window.destroy()


if __name__ == "__main__":
    main()
