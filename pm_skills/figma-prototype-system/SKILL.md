---
name: figma-prototype-system
description: "Use when bootstrapping a transferable prototype design system from existing Figma nodes: extracting design language, recreating supplied Figma canvases in a React/Vite preview project, generating DESIGN.md and README.md, localizing Figma assets, and creating a floating review shell with page catalog, PRD, change-record, and page-state controls. Use for first-time design-system/prototype foundation setup, not for drawing later new pages from an already established system."
---

# Figma Prototype System

Build a first-version React/Vite prototype foundation from existing Figma nodes. The goal is not to create a full product. The goal is to recreate the provided canvases well enough to calibrate the design language, then preserve that language in `DESIGN.md`, reusable shells/components, local assets, and a preview project that future prototype work can reuse.

## Scope

Use this skill only for **build-library mode**:

- Create the first prototype foundation from existing Figma nodes.
- Recreate each supplied Figma node as a preview page.
- Extract tokens, layout rules, shell patterns, and reusable components from the recreated pages.
- Deliver both `DESIGN.md` and a runnable React/Vite project.

Do not use this skill for later feature/page drawing after a design system already exists. That should use the target project's normal prototype skill and read the generated `DESIGN.md`.

## Input Gate

Collect these inputs before implementation:

- Project name.
- Output directory.
- Multiple Figma node URLs.
- Optional PRD or requirements document path.
- Optional screenshots, exported SVG/PNG files, or design notes.

If the collected information is not enough to produce a high-quality prototype, ask for more information before building. Keep asking until the minimum standard is met or the user explicitly says they will not provide more.

Ask for more when any of these are missing:

- Accessible Figma nodes.
- Enough node variety to infer page shell, navigation, core components, and overlays.
- Figma MCP access or screenshot/export fallback material.
- Project name or output directory.
- A real PRD/requirements document when the user expects PRD binding.
- Evidence for critical design rules such as primary color, typography, spacing, radius, shadow, or navigation structure.

If the user refuses to provide more, continue only if a useful low-confidence foundation can still be made. Mark low-confidence pages in the page catalog, `README.md`, and final response. Do not write guesses as confirmed rules in `DESIGN.md`.

## Figma Acquisition

Prefer Figma MCP data:

- Screenshots for visual comparison.
- Design context and metadata for layout, text, and assets.
- Variables for colors, fonts, spacing, radius, and component states.
- Asset download URLs for images, icons, and SVGs.

If MCP access fails, use screenshots or exported assets supplied by the user. Pages built from fallback material must be marked low confidence.

Never leave Figma MCP temporary URLs in the delivered project. Download assets into the project and import them from local files.

## Project Shape

Generate a React/Vite project with a reusable floating-review-shell design-preview structure:

```text
project/
  README.md
  DESIGN.md
  package.json
  index.html
  src/
    main.tsx
    App.tsx
    index.css
    components/
      CatalogShell.tsx
      PageDirectory.tsx
      PrdPanel.tsx
      ChangeRecordPanel.tsx
      AppShell.tsx
      DrawerShell.tsx
      CardShell.tsx
    pages/
      FigmaNodePageA.tsx
      FigmaNodePageB.tsx
    figma/
      catalog.ts
      changeRecords.ts
      pageMarkerStates.ts
      assets.ts
    material-library/
      registry.ts
    assets/
      figma-node-a/
      shared/
```

Adapt names to the project. Keep `App.tsx` as a catalog entry point. Put node recreations in `pages/`. Register every page in `src/figma/catalog.ts`.

## Preview Requirements

The prototype project must include:

- Before implementing the shell, read `references/floating-review-shell.md` and use it as the default code pattern for page catalog, PRD/change buttons, overlay panels, catalog collapse behavior, status markers, and responsive canvas scaling.
- Page catalog: switch between all Figma node recreation pages.
- Floating catalog presentation: use a lightweight floating page-catalog trigger near the top-left of the preview, not a permanently occupied left sidebar. The catalog opens as an overlay/popover and closes after page selection or outside click.
- Page catalog structure: support parent/child page hierarchy. Parent rows with children must have an expand/collapse arrow; the catalog header must include `收起全部`. If the input pages have an obvious main page plus related subpages, organize them into that hierarchy.
- Page status: at least `not-recreated`, `recreated-needs-calibration`, `calibrated`, `changed-needs-review`, and `low-confidence`. In the page catalog, every page row must include a separate clickable status marker button that cycles `none -> yellow -> green -> red`, matching the review workflow: unmarked, done-not-reviewed, reviewed, reviewed-but-changed.
- Page catalog rows must not show text status labels such as `已复现待校准`; the colored marker button is the visible status control.
- PRD button: keep `PRD 信息` in the top toolbar. If a real PRD or requirements document is bound, open the bound page-level PRD content. If no document exists, show a grey/empty PRD state such as `当前页面未绑定独立 PRD 功能模块`; do not invent PRD text.
- Change record panel: show page changes, why they changed, completion status, and whether `DESIGN.md` needs updating. Each change record must support `标记完成` and `还原未完成`; completion should update the current page marker to green when all records are completed and red when any record is incomplete. This panel must be an overlay panel next to the PRD controls, not content inside the user-facing prototype canvas.
- Material registry: register reusable Figma-derived shells, cards, dialogs, drawers, lists, and navigation fragments. The material-library entry belongs at the bottom of the page catalog popover, not in the top review toolbar.
- Review toolbar: include only `页面目录`, `PRD 信息`, and `变更记录` controls in a compact floating toolbar. Do not place `说明信息`, `素材库`, or `打开 Figma` in the top toolbar. These controls are for prototype review only and must be visually separated from the recreated product UI.

## Responsive Preview Standard

The recreated Figma canvas must adapt to the browser viewport by default:

- Keep the source canvas at its original design size internally, such as 1440px wide, so layout proportions remain faithful.
- Wrap the canvas in a responsive preview frame that calculates scale from the available viewport width and height.
- The preview must both shrink on smaller screens and enlarge on larger screens. Do not cap the scale at `1` unless the user explicitly asks for original-size-only review.
- Do not use a fixed `zoom` value such as `zoom: 0.58` as the final behavior.
- Do not leave a large unused grey area around the canvas on wide screens. The page should visually fill the available preview area.
- Do not make the review auxiliary panels, catalog, or PRD/change controls part of the canvas sizing calculation. They should float above the preview and not permanently reduce the canvas width.
- For very tall Figma nodes, fit width first and allow vertical scrolling instead of shrinking the page until text becomes unreadable.
- The outer preview should avoid decorative card framing, large fixed margins, rounded outer canvas chrome, or heavy shadows unless the original Figma canvas itself has those elements.

## Recreation Rules

- Create one recreation page for every input Figma node. Do not merge or skip nodes.
- Recreate the visible canvas first. This is the calibration surface for the design language.
- Extract shared components only after a structure appears in at least two supplied nodes or is clearly a global shell.
- Keep one-off structures local to the page.
- Prefer project tokens over scattered hard-coded values once a value is confirmed.
- Preserve visual hierarchy, spacing, typography, radius, shadows, and asset proportions.
- Do not add unrequested product features, flows, or business pages.

## DESIGN.md

Generate `DESIGN.md` using the existing project-style design document format when one is provided. Otherwise use this structure:

- Visual theme and atmosphere.
- Color specifications.
- Typography specifications.
- Component specifications.
- Shadow and elevation.
- Layout principles.
- State, feedback, or motion rules if supported by the provided nodes.
- AI drawing/prototype prompt guidance.

Only include rules supported by Figma data or verified recreations. Put uncertain or undersampled areas in a pending-calibration section.

## README.md

Generate `README.md` to explain how to use the foundation:

- Figma sources used for calibration.
- How to run the React/Vite project.
- Page catalog and node mapping.
- How to use `DESIGN.md` before future prototype work.
- Which shells/components are reusable and where content should be inserted.
- How to update the catalog, material registry, change records, and `DESIGN.md`.
- Confidence notes and recommended additional Figma nodes.

## Validation

Before final delivery:

- Start the React/Vite dev server.
- Open the local preview and verify no white screen.
- Check page catalog navigation.
- Check PRD button behavior: bound PRD opens page-level PRD content; missing PRD shows a grey/empty unbound state without invented content.
- Check change record panel and material panel.
- Check page catalog hierarchy, status marker cycling, `收起全部`, parent expand/collapse, and outside-click close behavior.
- Check responsive sizing at multiple viewport widths, including a wide desktop viewport. The recreated canvas must fill the available preview area instead of staying small in the center with large empty margins.
- Check that opening page catalog, PRD, change-record, or material panels does not permanently squeeze the canvas.
- Check local asset loading.
- Compare each recreated page against its Figma screenshot or supplied fallback image.
- Revise visible mismatches before claiming completion.

If the project cannot start, the work is not complete.

## Final Response

Report:

- Output project path.
- `DESIGN.md` path.
- `README.md` path.
- Recreated Figma nodes/pages.
- Calibrated pages and low-confidence pages.
- Reusable shells/components/materials.
- PRD binding status.
- Remaining information needed to improve confidence.
