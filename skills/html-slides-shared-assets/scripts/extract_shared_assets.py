#!/usr/bin/env python3
"""Extract identical marked CSS and JavaScript from multiple HTML slide decks."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path


STYLE_RE = re.compile(
    r'<style\b(?=[^>]*\bid=["\']slides-core["\'])[^>]*>(?P<body>.*?)</style>',
    re.IGNORECASE | re.DOTALL,
)
RUNTIME_RE = re.compile(
    r'<script\b(?=[^>]*\bid=["\']slides-runtime["\'])[^>]*>(?P<body>.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
THEME_RE = re.compile(
    r'<style\b(?=[^>]*\bid=["\']deck-theme["\'])[^>]*>.*?</style>',
    re.IGNORECASE | re.DOTALL,
)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_block(value: str) -> str:
    return value.strip() + "\n"


def collect_inputs(raw: list[Path], recursive: bool) -> list[Path]:
    found: list[Path] = []
    for item in raw:
        path = item.resolve()
        if path.is_file():
            if path.suffix.lower() != ".html":
                raise ValueError(f"not an HTML file: {path}")
            found.append(path)
        elif path.is_dir():
            iterator = path.rglob("*.html") if recursive else path.glob("*.html")
            found.extend(candidate.resolve() for candidate in iterator if candidate.is_file())
        else:
            raise ValueError(f"input not found: {path}")

    unique = sorted(set(found), key=lambda path: str(path).lower())
    if len(unique) < 2:
        raise ValueError("at least two HTML files are required")

    names: dict[str, Path] = {}
    for path in unique:
        key = path.name.lower()
        if key in names:
            raise ValueError(f"duplicate output filename: {names[key]} and {path}")
        names[key] = path
    return unique


def extract_marked(text: str, path: Path) -> tuple[str, str]:
    style = STYLE_RE.search(text)
    runtime = RUNTIME_RE.search(text)
    theme = THEME_RE.search(text)
    missing = []
    if not theme:
        missing.append("deck-theme")
    if not style:
        missing.append("slides-core")
    if not runtime:
        missing.append("slides-runtime")
    if missing:
        raise ValueError(f"{path}: missing marked block(s): {', '.join(missing)}")
    return normalize_block(style.group("body")), normalize_block(runtime.group("body"))


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size / (1024 * 1024):.2f} MiB"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="HTML files or folders")
    parser.add_argument("--output-dir", required=True, type=Path, help="new optimized folder")
    parser.add_argument("--recursive", action="store_true", help="scan input folders recursively")
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        print(f"ERROR: output directory already exists: {output_dir}")
        return 2

    try:
        paths = collect_inputs(args.inputs, args.recursive)
        texts = {path: path.read_text(encoding="utf-8") for path in paths}
        blocks = {path: extract_marked(text, path) for path, text in texts.items()}
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    style_hashes = {digest(style) for style, _ in blocks.values()}
    runtime_hashes = {digest(runtime) for _, runtime in blocks.values()}
    if len(style_hashes) != 1 or len(runtime_hashes) != 1:
        print("ERROR: marked shared blocks are not identical across all decks")
        for path, (style, runtime) in blocks.items():
            print(f"  {path.name}: css={digest(style)[:12]} js={digest(runtime)[:12]}")
        return 1

    style = next(iter(blocks.values()))[0]
    runtime = next(iter(blocks.values()))[1]
    style_hash = next(iter(style_hashes))[:12]
    runtime_hash = next(iter(runtime_hashes))[:12]
    css_name = f"slides-core.{style_hash}.css"
    js_name = f"slides-runtime.{runtime_hash}.js"
    css_link = f'<link rel="stylesheet" href="shared/{css_name}">'
    js_link = f'<script src="shared/{js_name}"></script>'

    original_size = sum(path.stat().st_size for path in paths)
    parent = output_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}-", dir=parent))
    try:
        shared = staging / "shared"
        shared.mkdir()
        (shared / css_name).write_text(style, encoding="utf-8", newline="\n")
        (shared / js_name).write_text(runtime, encoding="utf-8", newline="\n")

        for path, text in texts.items():
            optimized, style_count = STYLE_RE.subn(css_link, text, count=1)
            optimized, runtime_count = RUNTIME_RE.subn(js_link, optimized, count=1)
            if style_count != 1 or runtime_count != 1:
                raise RuntimeError(f"failed to replace marked blocks in {path}")
            (staging / path.name).write_text(optimized, encoding="utf-8", newline="\n")

        optimized_size = sum(path.stat().st_size for path in staging.rglob("*") if path.is_file())
        shutil.move(str(staging), str(output_dir))
    except Exception as exc:
        shutil.rmtree(staging, ignore_errors=True)
        print(f"ERROR: {exc}")
        return 1

    saved = original_size - optimized_size
    percent = (saved / original_size * 100) if original_size else 0
    print(f"Decks: {len(paths)}")
    print(f"Shared CSS hash: {style_hash}")
    print(f"Shared JS hash: {runtime_hash}")
    print(f"Before: {format_size(original_size)}")
    print(f"After:  {format_size(optimized_size)}")
    print(f"Saved:  {format_size(saved)} ({percent:.1f}%)")
    print(f"Output: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

