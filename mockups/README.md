# Analyst visual mockups

Four conceptual screens show persistent chat, editable investigation plans, evidence-linked answers and explicit sharing confirmation. The analyst interface is a design concept, not a working application or validated customer workflow.

| Image | State |
|---|---|
| `01-clarify.png` | Clarify through suggested replies or free text |
| `02-review-plan.png` | Review an enrichment plan and revise it with controls or text |
| `03-evidence-partial.png` | Inspect an evidence-linked answer and partial-source caveat |
| `04-share-graph.png` | Review a sharing draft and recipients before confirmation |

Open `index.html` for the gallery. PNGs are 2880 × 2200; SVGs and `generate.py` are editable sources. Figure captions are in section 3 of the analyst PRD. Keep exported images and captions together at a readable size.

Regenerate SVGs with `python3 mockups/generate.py`. Raster exports use Sharp at 144 dpi; regenerate PNGs after changing the SVG source.
