---
name: html-prototype-to-figma
description: 将 HTML/React/Vite 原型、设计预览站或本地网页同步为 Figma 设计稿的工作流规范。Use when Codex needs to convert HTML prototypes to Figma, push a local prototype into Figma, sync prototype pages to a Figma file, decide whether to create or use a target Figma file, exclude PRD/review/navigation helper UI from capture, expand hidden scroll content, document interaction states next to the main frame, troubleshoot Figma MCP connectivity, or verify 1:1 visual fidelity for responsive prototype screens.
---

# HTML Prototype To Figma

## Goal

Convert only the real business interface in an HTML prototype into editable Figma frames, while preserving visual fidelity and excluding prototype-only review tools such as page switchers, PRD panels, debug controls, route catalogs, and explanatory boards.

Use this together with `figma:figma-use` before every `use_figma` call. For first-time web capture, also use `figma:figma-generate-design`. If MCP or asset export fails, switch to `figma-mcp-troubleshooting` before continuing.

## Default Workflow

1. Confirm the Figma target before touching Figma.
   - If the user provides a Figma file URL, file key, or node, use that exact target and verify access.
   - If the user does not provide a target file, ask whether to create a new Figma file or use a specified existing file.
   - Do not silently create a new file when the user may expect an existing design file to be updated.
   - Do not silently write into a recent file unless the user explicitly selected it.

2. Lock scope before touching Figma.
   - Identify source URL, route, page id, and the exact user-facing state to draw.
   - List business UI that must be captured.
   - List prototype-only UI that must be excluded.
   - If the prototype contains PRD text, review panels, route navigation, state comparison boards, or implementation notes, treat them as authoring aids, not Figma deliverables.

3. Normalize the prototype state.
   - Run the local dev server or open the static HTML exactly as users would see it.
   - Navigate directly to the target route/state instead of capturing a page-list wrapper.
   - Close PRD overlays, drawers, debug panels, and review controls unless they are part of the actual product UI.
   - If helper UI cannot be hidden through normal state, create a temporary capture-only route or CSS override, then remove or clearly isolate it after capture.

4. Choose frame dimensions.
   - Capture at explicit viewports. Default desktop is `1440px` wide unless the prototype or user gives another design width.
   - Treat the browser viewport that fully represents the prototype as the source of truth. Verify `innerWidth`, `innerHeight`, and `devicePixelRatio` in the browser before capture; do not accept a smaller generated Figma frame just because it was successfully created.
   - Final Figma frames use fixed `1440px` width by default unless the user explicitly requests another width. If the generated frame is larger because of browser DPR or capture scaling, do not immediately run `frame.rescale(...)`. First compare at least one container width, one text font size, and one icon size against the source CSS/DOM.
   - For editable HTML-to-Figma output, only use whole-frame proportional scaling when containers, text, icons, strokes, and spacing all share the same scale factor. If containers are DPR-scaled but text/icons are already close to source CSS sizes, whole-frame scaling will make text/icons too small; recapture at DPR/deviceScaleFactor `1` or normalize layout containers without scaling text/icons.
   - If a previous or current source screenshot shows a larger intended canvas, keep that larger canvas unless the user asks for a different breakpoint. Do not downscale the browser to match an accidentally generated Figma frame.
   - For responsive prototypes, create one Figma frame per requested breakpoint, for example desktop and mobile. Do not stretch one generated frame to represent all responsive states.
   - Record viewport width, height, device scale factor, route, and state for each frame.

5. Generate the editable Figma layout with captureId.
   - The default editable-import path for HTML/React/Vite/local web pages is Figma MCP `generate_figma_design` plus the HTML-to-design capture script. Do not use screenshots, `upload_assets`, image fills, or PNG exports as the final deliverable when the user asks for editable Figma.
   - For each page or state, call `generate_figma_design` with the target `fileKey` and no `captureId` to generate one single-use captureId. Use one captureId per page/state; never reuse it.
   - For local/dev pages, temporarily inject this script into the HTML entry such as `index.html`, `public/index.html`, or the app layout:
     ```html
     <script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
     ```
     Remove the script after the capture batch unless the user explicitly asks to keep manual recapture available.
   - Open the exact route with this hash-based capture URL:
     ```text
     <target-url>#figmacapture=<captureId>&figmaendpoint=<encoded-submit-endpoint>&figmadelay=1000&figmaselector=<business-root-selector>
     ```
   - Use a selector such as `.figma-page`, `main[data-capture-root]`, or another real business root so the capture excludes route catalogs, PRD buttons, review bars, browser chrome, and page-switching shells. If the first capture grabs the whole app wrapper, discard/delete it and recapture with a tighter selector.
   - Poll `generate_figma_design` with the same `fileKey` and `captureId` every 5 seconds until it completes.
   - For multiple pages, generate one captureId per page and capture them independently.
   - Name final frames exactly with the prototype page name or user-facing page name when the user asks for names to stay unchanged. Do not append route ids or viewport suffixes unless they are needed to distinguish duplicate states or breakpoints.

6. Expand hidden content and interaction states.
   - If a page, panel, list, drawer, modal body, table, chat area, or form section scrolls, draw the off-screen content in Figma too.
   - If a button, tab, dropdown, segmented control, hover menu, popover, modal, drawer, validation message, submit result, or error state changes hidden UI, create an adjacent state frame.
   - Label adjacent states with the source component and state, for example `Create button / loading`, `Filter dropdown / expanded`, or `Submit button / validation-error`.
   - Keep adjacent state frames near the main frame, aligned on a simple grid, and do not mix them into the primary default-state frame.

7. Clean and structure the Figma result.
   - Remove captured helper UI that slipped in: page menus, PRD buttons, review notes, route selectors, dev toolbars, and explanatory text not visible to real users.
   - Preserve real product chrome: app navigation, sidebars, headers, input bars, drawers, dialogs, cards, and empty/error states when they are part of the target screen.
   - When placing a main page and its child pages into an existing business section, keep the main page and all of its direct child pages on the same horizontal row. Start a new row for each different main page. Do not put all main pages in one row and all child pages in later rows unless the prototype has no reliable parent-child mapping.
   - Keep imported page names unchanged when the task is to copy existing prototype pages into Figma. Rename root frames to the exact prototype page name after capture if the generated name differs.
   - Do not use `frame.rescale(1440 / frame.width)` as a default cleanup step for editable HTML-to-Figma imports. Use it only after proving text font sizes and icon sizes are scaled by the same factor as the containers. If text or icons would become smaller than the source CSS values, the capture is mismatched and must be recaptured or corrected selectively.
   - Delete or clearly move aside invalid captures after the editable frame is verified, especially whole-browser captures, whole-body captures, and screenshot-only frames.
   - Keep proportions from the source screenshot. Do not compress content to fit an arbitrary frame height; increase frame height when the real page is taller.
   - If the generated Figma frame is smaller than the verified browser viewport, discard or recapture it. If it contains the right content but clips scroll content, expand the frame height and parent containers to the full content height; never scale the captured image or child group to force it into the shorter frame.
   - When moving fixed or floating elements after expanding a frame, compute their position from `absoluteBoundingBox` relative to the root frame, not from local `x/y` alone. Parent frames may already have offsets, so local moves can accidentally push dialogs, chat input bars, popovers, or drawers outside the root frame.
   - Distinguish layout wrappers from visible components. A fixed footer, full-width docking area, or padded shell can be much wider than the actual rounded input card, modal, popover, or business dialog. Do not let the wrapper's width become the visible component's background or border.
   - Convert obvious groups into readable layer names, but avoid speculative componentization unless requested.

8. Verify fidelity before declaring done. This is a hard delivery gate.
   - Capture a browser screenshot of the source page at the same viewport.
   - Capture a Figma screenshot of the generated frame.
   - Do not use metadata alone as proof of correctness. Metadata can show that nodes exist while they are clipped, hidden, behind another layer, transparent, or placed in the wrong parent frame.
   - Compare structure, spacing, cropping, text wrapping, image loading, aspect ratios, hidden scroll content, and adjacent interaction-state frames.
   - Run the layer visibility checks below for the generated frame before reporting success.
   - Fix issues and re-check. Do not claim "1:1" unless a same-viewport visual check was completed.
   - If browser/Figma screenshot comparison or layer visibility checks cannot be completed, report the conversion as partial and list the missing verification. Do not say the Figma conversion is complete.

## What To Exclude

Exclude content that exists only to operate, explain, or review the prototype:

- Page lists, route catalogs, scenario switchers, and demo navigation controls.
- PRD information panels, PRD popovers, module text, requirements notes, and reviewer commentary.
- Debug badges, implementation labels, test controls, viewport rulers, and capture instructions.
- Comparison boards explaining multiple design options, unless the business product truly contains that comparison UI.
- Placeholder descriptions of future behavior that are not actual user-facing UI.

If uncertain, ask: "Would a real end user see this in the product?" If no, exclude it.

## Fidelity Rules

- Treat the rendered browser screenshot as the source of truth for visual layout.
- A `1440px` root frame is not sufficient proof of correctness. After HTML-to-Figma capture, compare representative CSS/DOM values against Figma values: card/input width, row height, badge size, text font size, and icon size. A common failure is a "false-correct" root frame where the outer frame has been scaled to `1440px`, but text becomes `7px` instead of source `12px` and icons become `10px` instead of source `18px`.
- Never fix a false-correct root frame by continuing to move or resize only visible containers. The content scale is already broken. Either recapture with a correct DPR/device scale, or selectively restore text/icon sizes from source CSS while preserving verified container dimensions.
- Keep image aspect ratios. Never stretch screenshots, icons, avatars, or product images to fill a mismatched box.
- Check broken images after capture. Missing or blank image nodes are failures, not acceptable placeholders.
- Preserve scroll height. If the source page or any internal region is taller than the viewport, draw the full content in a taller frame or adjacent continuation frame; do not leave important content invisible just because the browser viewport hides it.
- Compare every scroll root's `scrollHeight/clientHeight` at the selected viewport. A region can look acceptable in a screenshot while still having `scrollHeight > clientHeight`; the Figma output must represent the full `scrollHeight` without distorting the child content.
- Do not treat a resized Figma frame as scroll coverage. If the source capture screenshot was only the visible viewport, increasing the Figma frame height only creates empty/clipped space; it does not add the hidden DOM content. Recapture the page with the scroll root fully visible, or create a clearly labeled continuation frame from a real scrolled state.
- Match the source viewport. Differences caused by browser width, DPR, font loading, or collapsed responsive layouts must be resolved before comparison.
- Keep text readable and uncropped. Pay attention to line-height, overflow clipping, ellipsis, and Chinese text wrapping.
- Do not hide overflow with `clipsContent` just to mask layout mistakes.
- Treat unexpected `clipsContent`, zero-size containers, fully transparent nodes, and off-canvas children as possible conversion failures until checked visually.
- Avoid manual resizing of generated nodes unless you have verified it does not distort child content.
- Check expected component dimensions, not only frame bounds. If a source input card, modal, popover, or message bubble is visually `980px` wide inside a `2480px` footer/container, the Figma visible rounded rectangle must stay about `980px`; a `2480px` rounded rectangle is a distortion even if it stays inside the root frame.
- Check both axes after edits. A frame can pass vertical scroll validation while still having children overflow left or right. If a Figma screenshot's reported `original_width` is larger than the root frame width, treat it as a horizontal overflow warning and inspect descendant bounds.
- Check rendered bounds, not only layout bounds. In Figma, shadows, blurs, strokes, and effects can make `absoluteRenderBounds` exceed the frame even when every node's `absoluteBoundingBox` is inside. If the browser viewport clips those effects, set `clipsContent` on the root viewport/shell frames after verifying this matches the source; if the effect should remain visible, expand the frame instead.
- Clipping the root/shell is only valid after scroll coverage is proven. First verify that every scroll root's bottom content is present in Figma, using text sentinels or bottom-most node bounds; then clip root/shell to match viewport effects. Never use `clipsContent` to make a too-short or incomplete capture look clean.
- Prefer small Figma edits with returned `createdNodeIds` / `mutatedNodeIds`, followed by screenshot validation.

## Layer Visibility Validation

HTML/CSS visibility is not the same as Figma layer visibility. A node can exist in Figma metadata and still be invisible in the rendered design. Always check for conversion artifacts that change visual stacking, clipping, or parent-child relationships.

Required checks after each generated frame:

- Compare the source browser screenshot and the Figma screenshot at the same viewport before declaring the frame done.
- Inspect top-level and important nested frames for `clipsContent: true`. If a child visually needs to escape the parent in HTML, move it to the correct Figma parent or disable clipping only after screenshot verification.
- Check children whose bounds extend outside their parent frame. Decide whether the overflow is intentional product UI, hidden scroll content, or a conversion error.
- Check floating UI such as popovers, dropdowns, hover menus, sticky headers, fixed footers, modals, drawers, tooltips, badges, and command menus. These are likely to be reordered or reparented during conversion.
- Check every visible descendant against the root frame bounds: `child.left >= root.left`, `child.right <= root.right`, `child.top >= root.top`, and `child.bottom <= root.bottom`, allowing only intentional continuation frames or explicitly labeled off-canvas states. Do this with `absoluteBoundingBox`; local coordinates are not enough when parents are nested or offset.
- Repeat the root-boundary check with `absoluteRenderBounds` for visible descendants and for the root frame itself. A clean `absoluteBoundingBox` check is not sufficient when fixed footers, input bars, cards, dialogs, or floating panels have shadows or blur effects.
- Check occlusion, not only overflow. A fixed footer/input bar can cover a business card while both nodes remain fully inside the root frame. Measure overlap between bottom-fixed areas and previous business content; if overlap is greater than `0`, expand the frame or create a continuation state and move the fixed area below the content.
- Check layer order when a visible HTML element is missing in Figma. A node behind an opaque sibling is a failure even if metadata says it exists.
- For nested floating UI with CSS `z-index`, verify the ancestor stacking context, not only the floating node itself. In Figma, a child cannot visually rise above a later sibling of its ancestor. If a dropdown, command menu, popover, tooltip, or modal is captured inside a lower sibling and overlaps a later section/card, reparent the floating layer to the nearest shared parent, preserve its `absoluteBoundingBox` position, and append it after the overlapped sibling.
- Check for nodes with width or height near `0`, opacity `0`, invisible fills, missing image fills, or masks that make children disappear.
- Check text nodes for clipped line height, unexpected wrapping, ellipsis, or being placed inside a parent that is too small.
- If `generate_figma_design` re-parents components into noisy raw frames, use the capture as a pixel reference and fix with targeted `use_figma` edits. Return `mutatedNodeIds` for every fix.
- If a visibility issue is found and cannot be fixed quickly, label it as a residual difference in the final report with the affected component and likely cause.

Common failure patterns:

- `position: absolute` or `fixed` content is placed inside a clipped Figma frame.
- `z-index` stacking is flattened into DOM order, causing menus or overlays to sit behind cards.
- A nested overlay keeps its local order inside an input/card frame, but that ancestor sits below a later sibling such as a recommendation list; the overlay must be reparented to the shared stacking context and placed above the later sibling.
- Scroll containers are captured only at their visible viewport height.
- A hidden interaction state was not triggered before capture.
- Responsive layout was captured at the wrong viewport or device scale factor.
- An image becomes an empty frame or a stretched fill after conversion.
- A bottom-fixed input bar or modal has a drop shadow whose `absoluteRenderBounds` extends outside the root frame. If the source browser clips the shadow at the viewport edge, clip the root viewport/shell frame; do not move the component upward just to hide the overflow.
- A bottom-fixed input bar overlaps a result card, table, list, or form inside the root frame. Root-boundary checks pass, but business content is still hidden. Treat this as a failed scroll/visibility conversion.

## Scroll And Overflow States

HTML prototypes often use scroll containers that hide content inside a fixed page. Figma deliverables must still show the complete business information.

- Inspect likely scroll roots: `body`, `main`, drawers, modal bodies, side panels, chat histories, tables, lists, cards, and form sections.
- Compare each element's `scrollHeight` vs `clientHeight` and `scrollWidth` vs `clientWidth`.
- For vertical overflow, extend the Figma frame or create a nearby `continued` frame that shows the rest of the content.
- For bottom-fixed input/footer patterns, check whether the fixed area visually covers the last business card/list/table/form. If it does, extend the Figma frame height and move the fixed area below the complete business content, or create a labeled continuation frame. Do not leave the fixed area covering content just because the original browser viewport would scroll.
- For first-pass HTML-to-Figma capture of a vertically scrolling primary area, prefer recapturing with a browser viewport tall enough to expose the whole scroll root: `targetHeight = scrollRoot.scrollHeight + fixedHeaderHeight + fixedFooterHeight`. For shell patterns with fixed top chrome and bottom input areas, include both fixed regions in the target height formula. Record the formula and the measured values.
- After recapturing, validate the source screenshot dimensions. If the screenshot or capture artifact is still only the old viewport height, the hidden content was not captured; do not proceed by stretching Figma nodes.
- When a scroll container is represented by a captured image or large child group, compare that child height to the parent height. If the child is taller and the parent clips it, expand the parent/root frame to `ceil(child.y + child.height)` and re-check screenshot output.
- For horizontal overflow, preserve the full content width when it represents a real product canvas; if it is accidental overflow, report it instead of normalizing it away.
- Keep sticky headers, sticky footers, and fixed input bars in the main frame, then show the scrollable content continuation separately when needed. If a full-scroll frame is created by expanding the root height, move fixed bottom elements to the bottom only after recalculating their absolute position relative to the root frame. Example: for a `2560px` root and a `2480px` input bar, the final relative x should be `80`, not `80 + parentOffset`.
- For fixed bottom input areas, inspect the source DOM hierarchy before resizing or moving in Figma. In common shell patterns, the outer footer can span the full content column while the actual input card is centered with a narrower min/max width. If Figma captures the visible rounded input as the outer wrapper width, shrink the visible frame back to the source component width and preserve inner children by absolute position.
- Do not rely on a single clipped screenshot as the full Figma output when business content exists below or beside the visible viewport.

## Viewport Mismatch Recovery

If a capture is generated at the wrong size:

- Stop and identify the verified browser viewport, output Figma frame size, and any scroll-root dimensions.
- If the browser viewport was wrong, recapture at the correct explicit viewport.
- If the browser viewport was correct but the generated Figma frame is larger, diagnose what is scaled before changing it. Measure representative source CSS/DOM values and Figma values for: root frame width, a card/input container, a text font size, and an icon.
- If every measured value shares the same scale factor, proportional scaling is allowed.
- If containers are larger but font sizes/icons are not enlarged by the same factor, do not scale the whole frame. This creates a false-correct outer frame with tiny text/icons. Prefer recapturing with DPR/deviceScaleFactor `1`; if recapture is impossible, resize only the affected layout containers and preserve or restore text/icon sizes from the source CSS.
- If the browser viewport was correct but the Figma frame is smaller, treat that frame as invalid and recapture or replace it.
- If the frame width is correct but content is vertically clipped, expand the root frame and clipped parent containers to the full rendered content height. Keep image and child proportions unchanged.
- Delete or clearly mark invalid earlier captures so the user does not mistake them for final deliverables.

## Interaction State Frames

Static Figma output must include hidden states that are reachable through real user interaction.

- Identify interactive triggers from the prototype code and UI: buttons, tabs, selects, dropdowns, upload controls, accordions, modals, drawers, menus, toggles, submit actions, validation rules, and hover-only controls.
- Trigger each meaningful state in the browser or infer it from the component code when browser triggering is impractical.
- Draw each hidden state next to the default frame, not on top of it.
- Label every state with `Component / State`, and optionally add a short state note outside the frame, for example `Publish button / disabled` or `Resource picker / open`.
- Include only states that affect product UI. Do not draw debug-only, PRD-only, or prototype-navigation states.
- When a state depends on backend response, include the representative states defined by the prototype: loading, success, empty, validation error, permission error, or retryable failure.

## Responsive Prototype Handling

HTML prototypes are often adaptive; Figma frames are explicit states. Convert responsiveness into named frames:

- `desktop`: default full layout, usually `1440px` wide.
- `tablet`: only when the product has a distinct tablet state or the user asks for it.
- `mobile`: only when the prototype supports a real mobile layout or the user asks for it.

For each frame, use the matching browser viewport and capture that state. Do not infer a mobile design from desktop CSS without rendering it.

## Figma MCP Checks

Before claiming Figma is ready, separate these facts:

- Tool availability: Figma tools exist in the current Codex session.
- File readability: the target file or node can be read with metadata/screenshot.
- File writability: a write call succeeds and returns concrete node IDs.

If MCP fails:

1. Confirm Figma Desktop is open on the target file.
2. Confirm Dev Mode MCP server is enabled.
3. Check whether the current tool call or local MCP endpoint can list `get_metadata`, `get_screenshot`, and `get_design_context`.
4. If asset URLs return `404` or `502`, switch image export to download mode and provide an allowed absolute `dirForAssetWrites`.
5. Do not continue from stale assumptions after an authorization or MCP error. Re-run the smallest read/write check.

## Validation Checklist

Complete this checklist for every delivered Figma conversion:

- [ ] Target Figma file behavior is confirmed: new file or specified existing file.
- [ ] Target route/state and viewport are recorded.
- [ ] Editable import used `generate_figma_design` captureId plus capture script; no screenshot/image-fill frame is treated as the final deliverable.
- [ ] Each page/state used a distinct captureId and was polled until completed.
- [ ] Temporary capture script was removed after capture, or intentionally left in place because the user asked for manual recapture.
- [ ] Prototype-only PRD/review/navigation helpers are excluded.
- [ ] Business-root selector used for capture is recorded, for example `.figma-page` or `main[data-capture-root]`.
- [ ] Browser source screenshot exists or was visually inspected at the exact viewport.
- [ ] Figma frame screenshot was checked after generation.
- [ ] Browser and Figma screenshots were compared at the same viewport, or the conversion is explicitly reported as partial.
- [ ] Metadata was not used as the only proof of correctness.
- [ ] Final frame names match the prototype page names when names must be preserved.
- [ ] Final frame width is `1440px` by default, or the exact width requested by the user.
- [ ] Capture scaling mismatch was diagnosed with representative container, text, and icon measurements before any scaling operation.
- [ ] If `frame.rescale(...)` was used, containers, text font sizes, icon sizes, strokes, and spacing were confirmed to share the same scale factor. If not, recapture or selective correction was used instead.
- [ ] Editable proof was checked: text/vector/group layers exist, and the final root is not a single screenshot/image fill.
- [ ] Layer visibility was checked: clipping, overflow, z-order, masks, opacity, zero-size nodes, and off-canvas children.
- [ ] Root-boundary validation was checked on both axes with `absoluteBoundingBox`; no visible child unintentionally extends outside the root frame.
- [ ] Render-boundary validation was checked with `absoluteRenderBounds`; shadows, blurs, strokes, and effects do not make the screenshot larger than the root frame unless intentionally labeled.
- [ ] Floating UI was checked: dropdowns, popovers, modals, drawers, sticky/fixed areas, badges, and command menus.
- [ ] Bottom-fixed input/footer areas were checked for occluding business content inside the root frame. Passing root-boundary checks alone is not enough.
- [ ] Nested floating UI was checked against ancestor sibling order; any overlay that overlaps later sibling content is reparented to a shared stacking context and visually confirmed above the overlapped content.
- [ ] Images and icons are present, not blank, stretched, or wrong-format.
- [ ] Text is not clipped, overlapped, or unexpectedly wrapped.
- [ ] Visible component sizes match the source screenshot/DOM rects; full-width layout wrappers have not become stretched cards, dialogs, bubbles, or input boxes.
- [ ] Long pages and internal scroll regions show hidden/off-screen business content.
- [ ] Scroll coverage was proven from real captured content, not by merely resizing the Figma frame; bottom sentinels such as the final item, final scene label, final error message, or footer/input are present.
- [ ] Meaningful hidden interaction states are drawn beside the default frame and labeled by component/state.
- [ ] In each business section, every main page is placed on the same row as its direct child pages, and different main pages start different rows.
- [ ] Figma write operations returned concrete node IDs when `use_figma` was used.
- [ ] Remaining differences or blocked MCP/asset issues are explicitly reported.

## Report Format

When finished, report:

- Source: URL/route, viewport, and state.
- Figma target: file/page/frame name, changed node IDs when available, final frame size, captureId, and selector.
- Editable proof: whether text/vector/group layers were found and whether the final frame avoids single-image fills.
- Excluded helper UI: short list.
- Scroll coverage: whether hidden/off-screen business content was expanded.
- Interaction states: adjacent state frames created, or reason none were needed.
- Verification: browser/Figma screenshot check result.
- Layer visibility: clipping/z-order/overflow issues checked and fixed, or listed as residual differences.
- Residual differences: only if any remain.
