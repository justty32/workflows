---
name: html-slides-shared-assets
description: Reduce the total size of a collection of similar HTML slide decks by extracting their identical marked CSS and JavaScript into shared local assets. Use for folders containing multiple browser-playable slide decks that should remain separate presentations but no longer need to be individually self-contained. Do not use for a single deck or when every HTML file must remain portable by itself.
---

# HTML Slides Shared Assets

Optimize a collection, not an individual deck. Preserve each presentation's content, notes, theme, and filename while moving identical reusable code into shared local files.

## Expected Markers

Decks produced by `$markdown-html-slides` contain:

- `<style id="deck-theme">` for deck-specific colors and overrides;
- `<style id="slides-core">` for reusable layout and print CSS;
- `<script id="slides-runtime">` for reusable playback behavior.

Only `slides-core` and `slides-runtime` are extracted. Keep `deck-theme` inline so decks may retain different visual identities.

## Workflow

1. Inspect all target `.html` files and confirm there are at least two. Determine whether the user needs individually portable files; if so, explain that shared assets trade portability for smaller total size and do not optimize without consent.
2. Preserve the originals. Use a new output directory unless the user explicitly requests in-place modification. The bundled script intentionally refuses an existing output directory.
3. Confirm every file has the three expected IDs. For older compatible decks without markers, work on copies and add IDs only after verifying the proposed core CSS and runtime JavaScript are identical across all decks. Do not guess which deck-specific CSS is safe to share.
4. Run:

   ```text
   python scripts/extract_shared_assets.py --output-dir <new-folder> <html-file-or-folder> [...]
   ```

   Add `--recursive` only when nested input folders are intended.
5. The script must report identical hashes for the common CSS and JavaScript before writing. If the blocks differ, stop and describe the difference; do not force one deck's runtime or styles onto the others.
6. Inspect the output: each HTML file should retain its inline `deck-theme` and link to the two files under `shared/`. Open representative decks and exercise next/previous, overview, notes, fullscreen, hash navigation, and print layout when browser control is available.
7. Report input size, optimized collection size, savings, output location, and the portability tradeoff. Do not delete or replace the source decks.

## Safety and Scope

- Never deduplicate presentation content, speaker notes, or deck-specific theme rules merely because they look similar.
- Use only relative local URLs so the optimized folder can be moved as one unit and opened without a server.
- Keep the `shared/` folder beside the optimized HTML files. Moving an HTML file out of that folder breaks its shared references.
- Do not minify content automatically. Extraction is reversible and reviewable; minification can be a separate explicit request.
- Do not create a playback guide or README unless requested.

