# Fieldnotes — HTML & CSS guide

Open `index.html` in a browser. All lessons, images, styles, and examples are local. A small vanilla script enables chapter navigation, search, copy buttons, theme choice, and local reading progress; the teaching content and projects cover HTML and CSS only. Without that script, all chapters remain readable in one document.

## Included

- 24 chapters with examples, browser previews, common mistakes, exercises, and 48 quiz answers.
- 9 original explanatory SVG diagrams, a cover illustration, and a bicycle illustration.
- 3 standalone projects in `projects/` with complete reference solutions.
- `guide.md`: the complete printable/source-friendly Markdown guide.

## Local preview

Run `python3 -m http.server 8766 --directory html-css-guide` from the parent directory, then open `http://localhost:8766`.

## Editing

The static document is generated from `scripts/lessons.py` and `scripts/build.py`. Run `python3 html-css-guide/scripts/build.py` from the parent directory after editing. Styles and client interactions live in `styles.css` and `app.js`.

## Sources and assets

Each chapter links to its official documentation. The roadmap was read from the local project's converted roadmap content because the public URL could not be retrieved. All SVG artwork is original and included in `assets/`; no external fonts, image hotlinks, analytics, or API keys are required.

Browser examples use sandboxed frames with scripts and form submission disabled. The standalone form projects use local GET submissions with demo values; no real booking or external data processing is implemented. Reading completion is self-reported and is not presented as mastery. Local storage is best-effort and may vary for file URLs.
