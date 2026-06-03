# Floating Review Shell Reference

Use this as the default reference when building the prototype review shell for `figma-prototype-system`.

The goal is to provide a project-agnostic floating review shell:

- Floating review toolbar, not a permanent left sidebar.
- Top toolbar includes only `页面目录`, `PRD 信息`, `变更记录`.
- `素材库` lives at the bottom of the page catalog popover.
- Do not include `说明信息`, `素材库`, or `打开 Figma` in the top toolbar.
- Page catalog opens as a popover and closes after navigation.
- Page catalog supports parent/child hierarchy, child-row expand/collapse, and a `收起全部` action in the catalog header.
- Each catalog row has an independent clickable status marker button that cycles `none -> yellow -> green -> red`.
- Catalog rows do not show text status labels such as `已复现待校准`; the colored marker button is the visible status control.
- Change records have `标记完成` and `还原未完成` actions that update the current page marker.
- PRD/change/material panels are overlays and do not resize the recreated Figma canvas.
- Canvas keeps the original Figma design size internally, but the preview frame scales it to fill the browser.

## React Pattern

```tsx
import { useEffect, useMemo, useRef, useState, type CSSProperties, type FC } from 'react'

const FIGMA_CANVAS_WIDTH = 1440
const MIN_PREVIEW_SCALE = 0.36
const MAX_PREVIEW_SCALE = 1.8

type ReviewPanel = 'prd' | 'changes' | 'materials' | null
type CatalogMarkerState = 'none' | 'yellow' | 'green' | 'red'
type ChangeRecordStatuses = Record<string, string>

const CATALOG_MARKER_STATE_ORDER: CatalogMarkerState[] = ['none', 'yellow', 'green', 'red']
const CATALOG_MARKER_LABELS: Record<CatalogMarkerState, string> = {
  none: '无色',
  yellow: '黄色',
  green: '绿色',
  red: '浅红色',
}

export default function CatalogShell() {
  const [activeId, setActiveId] = useState(CATALOG_PAGES[0].id)
  const [isCatalogOpen, setIsCatalogOpen] = useState(false)
  const [panel, setPanel] = useState<ReviewPanel>(null)
  const [collapsedPageIds, setCollapsedPageIds] = useState<Record<string, boolean>>({})
  const [pageMarkerStates, setPageMarkerStates] = useState<Record<string, CatalogMarkerState>>(
    getInitialPageMarkerStates,
  )
  const [changeRecordStatuses, setChangeRecordStatuses] = useState<ChangeRecordStatuses>(
    getInitialChangeRecordStatuses,
  )
  const [previewScale, setPreviewScale] = useState(1)
  const [previewHeight, setPreviewHeight] = useState(750)
  const stageRef = useRef<HTMLDivElement | null>(null)
  const canvasRef = useRef<HTMLDivElement | null>(null)
  const catalogRef = useRef<HTMLDivElement | null>(null)
  const panelRef = useRef<HTMLElement | null>(null)

  const activePage = CATALOG_PAGES.find((page) => page.id === activeId) ?? CATALOG_PAGES[0]
  const ActivePage = PAGE_COMPONENTS[activePage.id] as FC
  const records = CHANGE_RECORDS.filter((record) => record.pageId === activePage.id)
  const activeMarkerState = pageMarkerStates[activePage.id] ?? 'none'
  const hasCompletedActiveChangeRecord = records.some((record) =>
    Boolean(changeRecordStatuses[getChangeRecordStatusKey(activePage.id, record.title)]),
  )
  const canOpenChangeRecords =
    records.length > 0 && (activeMarkerState === 'red' || hasCompletedActiveChangeRecord)
  const groups = useMemo(
    () =>
      CATALOG_GROUPS.map((group) => ({
        ...group,
        pages: CATALOG_PAGES.filter((page) => page.group === group.id),
      })).filter((group) => group.pages.length > 0),
    [],
  )

  const previewFrameStyle = {
    '--preview-scale': String(previewScale),
    '--preview-height': `${previewHeight}px`,
  } as CSSProperties

  useEffect(() => {
    if (!isCatalogOpen) return
    const handlePointerDown = (event: PointerEvent) => {
      if (!catalogRef.current?.contains(event.target as Node)) setIsCatalogOpen(false)
    }
    window.addEventListener('pointerdown', handlePointerDown)
    return () => window.removeEventListener('pointerdown', handlePointerDown)
  }, [isCatalogOpen])

  useEffect(() => {
    if (!panel) return
    const handlePointerDown = (event: PointerEvent) => {
      const target = event.target as Node
      if (panelRef.current?.contains(target) || catalogRef.current?.contains(target)) return
      setPanel(null)
    }
    window.addEventListener('pointerdown', handlePointerDown)
    return () => window.removeEventListener('pointerdown', handlePointerDown)
  }, [panel])

  useEffect(() => {
    const stage = stageRef.current
    const canvas = canvasRef.current
    if (!stage || !canvas) return

    const updatePreviewSize = () => {
      const figmaPage = canvas.querySelector<HTMLElement>('.figma-page')
      const canvasHeight = Math.max(figmaPage?.scrollHeight ?? canvas.scrollHeight, 750)
      const availableWidth = Math.max(stage.clientWidth, 320)
      const availableHeight = Math.max(stage.clientHeight - 48, 320)
      const widthScale = availableWidth / FIGMA_CANVAS_WIDTH
      const heightScale = availableHeight / canvasHeight
      const shouldFitHeight = canvasHeight <= availableHeight * 1.25
      const nextScale = Math.min(
        MAX_PREVIEW_SCALE,
        Math.max(MIN_PREVIEW_SCALE, shouldFitHeight ? Math.min(widthScale, heightScale) : widthScale),
      )

      setPreviewHeight(canvasHeight)
      setPreviewScale(Number(nextScale.toFixed(3)))
    }

    updatePreviewSize()
    const frame = window.requestAnimationFrame(updatePreviewSize)
    const observer = new ResizeObserver(updatePreviewSize)
    observer.observe(stage)
    observer.observe(canvas)
    window.addEventListener('resize', updatePreviewSize)

    return () => {
      window.cancelAnimationFrame(frame)
      observer.disconnect()
      window.removeEventListener('resize', updatePreviewSize)
    }
  }, [activeId])

  const cyclePageMarkerState = (pageId: string) => {
    setPageMarkerStates((current) => {
      const currentState = current[pageId] ?? 'none'
      const currentIndex = CATALOG_MARKER_STATE_ORDER.indexOf(currentState)
      return {
        ...current,
        [pageId]: CATALOG_MARKER_STATE_ORDER[(currentIndex + 1) % CATALOG_MARKER_STATE_ORDER.length],
      }
    })
  }

  const toggleChangeRecordCompleted = (record: ChangeRecord) => {
    // Use the current page + record id/title as the storage key.
    // When all current-page records are completed, set the page marker to green.
    // When any current-page record is incomplete, set the page marker to red.
  }

  const toggleCollapsed = (pageId: string) => {
    setCollapsedPageIds((current) => ({
      ...current,
      [pageId]: !current[pageId],
    }))
  }

  const collapseAllMainPages = () => {
    const next: Record<string, boolean> = {}
    for (const page of CATALOG_PAGES) {
      if (!page.parentId && CATALOG_PAGES.some((child) => child.parentId === page.id)) {
        next[page.id] = true
      }
    }
    setCollapsedPageIds(next)
  }

  const renderCatalogItem = (page: CatalogPage, items: CatalogPage[], depth = 0) => {
    const children = items.filter((child) => child.parentId === page.id)
    const hasChildren = children.length > 0
    const isCollapsed = Boolean(collapsedPageIds[page.id])

    return (
      <li key={page.id}>
        <div className={page.id === activeId ? 'catalog-page is-active' : 'catalog-page'}>
          <button
            type="button"
            className="catalog-page-link"
            onClick={() => {
              setActiveId(page.id)
              setIsCatalogOpen(false)
              setPanel(null)
            }}
          >
            {depth > 0 ? <span className="catalog-child-prefix">↳</span> : null}
            <strong>{page.title}</strong>
          </button>
          {hasChildren ? (
            <button
              type="button"
              className={isCollapsed ? 'catalog-collapse-button is-collapsed' : 'catalog-collapse-button'}
              aria-label={isCollapsed ? '展开子页面' : '收起子页面'}
              onClick={(event) => {
                event.stopPropagation()
                toggleCollapsed(page.id)
              }}
            >
              <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M4.5 6.2 8 9.8l3.5-3.6" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          ) : null}
          <button
            type="button"
            className={`catalog-marker-button marker-${pageMarkerStates[page.id] ?? 'none'}`}
            aria-label={`当前为${CATALOG_MARKER_LABELS[pageMarkerStates[page.id] ?? 'none']}，点击切换`}
            onClick={(event) => {
              event.stopPropagation()
              cyclePageMarkerState(page.id)
            }}
          >
            <span />
          </button>
        </div>
        {hasChildren && !isCollapsed ? (
          <ul className="catalog-child-list">
            {children.map((child) => renderCatalogItem(child, items, depth + 1))}
          </ul>
        ) : null}
      </li>
    )
  }

  return (
    <div className="catalog-shell">
      <div className="catalog-floating" ref={catalogRef}>
        <div className="catalog-toolbar">
          <button
            type="button"
            className="catalog-directory-trigger"
            onClick={() => setIsCatalogOpen((current) => !current)}
          >
            <span className="catalog-menu-icon">
              <i />
              <i />
              <i />
            </span>
            页面目录
            <em>{activePage.title}</em>
          </button>
          <button
            className={panel === 'prd' ? 'is-active' : ''}
            onClick={() => {
              setPanel(panel === 'prd' ? null : 'prd')
              setIsCatalogOpen(false)
            }}
          >
            <span className="toolbar-dot is-muted" />
            PRD 信息
          </button>
          <button
            disabled={!canOpenChangeRecords}
            className={panel === 'changes' ? 'is-active danger' : ''}
            onClick={() => {
              if (!canOpenChangeRecords) return
              setPanel(panel === 'changes' ? null : 'changes')
              setIsCatalogOpen(false)
            }}
          >
            <span className={canOpenChangeRecords ? 'toolbar-dot is-red' : 'toolbar-dot is-muted'} />
            变更记录
          </button>
        </div>

        {isCatalogOpen ? (
          <nav className="catalog-popover">
            <div className="catalog-popover-head">
              <span>页面切换</span>
              <button type="button" onClick={collapseAllMainPages}>收起全部</button>
            </div>
            {groups.map((group) => (
              <section key={group.id} className="catalog-popover-group">
                <h3>{group.name}</h3>
                <ul>
                  {group.pages
                    .filter((page) => !page.parentId)
                    .map((page) => renderCatalogItem(page, group.pages))}
                </ul>
              </section>
            ))}
            <div className="catalog-popover-footer">
              <button
                type="button"
                onClick={() => {
                  setPanel('materials')
                  setIsCatalogOpen(false)
                }}
              >
                素材库
              </button>
            </div>
          </nav>
        ) : null}
      </div>

      {panel ? (
        <aside
          ref={panelRef}
          className={`reference-panel ${panel === 'changes' ? 'is-change-panel' : ''}`}
        >
          <button className="reference-close" onClick={() => setPanel(null)} aria-label="关闭面板">
            ×
          </button>
          {panel === 'prd' ? <PrdPanel page={activePage} /> : null}
          {panel === 'changes' ? (
            <ChangeRecordPanel
              records={records}
              page={activePage}
              changeRecordStatuses={changeRecordStatuses}
              onToggleCompleted={toggleChangeRecordCompleted}
            />
          ) : null}
          {panel === 'materials' ? <MaterialPanel /> : null}
        </aside>
      ) : null}

      <main className="catalog-main">
        <div className="preview-layout">
          <div className="preview-stage" ref={stageRef}>
            <div className="preview-canvas-frame" style={previewFrameStyle}>
              <div className="preview-canvas" ref={canvasRef}>
                <ActivePage />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
```

Panel components should follow this behavior:

- `PrdPanel` shows the current page title and the bound page-level PRD content. If no real PRD is bound, show `当前页面未绑定独立 PRD 功能模块。` and do not invent placeholder PRD text.
- `ChangeRecordPanel` receives the current page's records and renders `标记完成` / `还原未完成`. Completing every current-page record sets the page marker to green; restoring any record sets it back to red.
- `MaterialPanel` is opened only from the catalog popover footer.

## CSS Pattern

```css
.catalog-shell {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: #f7f8fa;
}

.catalog-floating {
  position: absolute;
  left: 12px;
  top: 12px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.catalog-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.catalog-toolbar button,
.catalog-toolbar a,
.catalog-directory-trigger {
  display: inline-flex;
  height: 36px;
  align-items: center;
  gap: 8px;
  border: 1px solid #f2f3f5;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  color: #1d2129;
  padding: 0 12px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
}

.catalog-toolbar button:disabled,
.catalog-toolbar .disabled {
  cursor: not-allowed;
  background: #f7f8fa;
  box-shadow: none;
  color: #c9cdd4;
}

.toolbar-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  border-radius: 50%;
}

.toolbar-dot.is-muted {
  background: #c9cdd4;
}

.toolbar-dot.is-red {
  background: #fca5a5;
}

.catalog-popover {
  width: 326px;
  max-height: 72vh;
  overflow-y: auto;
  border: 1px solid #e5e6eb;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 18px 48px rgba(15, 23, 42, 0.16);
  padding: 12px;
}

.catalog-popover-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  border-bottom: 1px solid #f2f3f5;
  padding: 4px 8px 12px;
}

.catalog-popover-head button {
  border: 0;
  border-radius: 8px;
  background: #f7f8fa;
  color: #4e5969;
  padding: 6px 8px;
  font-size: 12px;
  font-weight: 600;
}

.catalog-page {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 8px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  padding: 8px;
  text-align: left;
}

.catalog-page.is-active {
  background: #fff1f2;
  color: var(--brand-color, #a82126);
}

.catalog-page-link {
  display: flex;
  min-width: 0;
  flex: 1;
  align-items: center;
  gap: 8px;
  border: 0;
  background: transparent;
  padding: 0;
  text-align: left;
}

.catalog-collapse-button {
  display: grid;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  place-items: center;
  border: 0;
  border-radius: 6px;
  background: transparent;
  color: #86909c;
  padding: 0;
}

.catalog-collapse-button svg {
  width: 14px;
  height: 14px;
  transition: transform 0.16s ease;
}

.catalog-collapse-button.is-collapsed svg {
  transform: rotate(-90deg);
}

.catalog-child-prefix {
  flex-shrink: 0;
  color: #c9cdd4;
  font-size: 12px;
}

.catalog-child-list {
  margin: 2px 0 0;
  padding: 0 0 0 12px;
  list-style: none;
}

.catalog-marker-button {
  display: grid;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border: 1px solid #c9cdd4;
  border-radius: 50%;
  background: #fff;
  place-items: center;
  padding: 0;
}

.catalog-marker-button span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: transparent;
}

.catalog-marker-button.marker-yellow {
  border-color: #f7ba1e;
  background: #f7ba1e;
}

.catalog-marker-button.marker-green {
  border-color: #00c261;
  background: #00c261;
}

.catalog-marker-button.marker-red {
  border-color: #fca5a5;
  background: #fca5a5;
}

.catalog-marker-button.marker-yellow span,
.catalog-marker-button.marker-green span,
.catalog-marker-button.marker-red span {
  background: #fff;
}

.catalog-popover-footer {
  margin-top: 12px;
  border-top: 1px solid #f2f3f5;
  padding: 12px 8px 4px;
}

.catalog-popover-footer button {
  width: 100%;
  border: 1px solid #e5e6eb;
  border-radius: 10px;
  background: #f7f8fa;
  color: #1d2129;
  padding: 9px 10px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
}

.catalog-main,
.preview-layout {
  height: 100%;
  min-height: 0;
  min-width: 0;
}

.preview-stage {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 100%;
  min-width: 0;
  overflow: auto;
  padding: 0;
}

.preview-canvas-frame {
  position: relative;
  width: calc(1440px * var(--preview-scale));
  height: calc(var(--preview-height) * var(--preview-scale));
  flex: 0 0 auto;
  margin: 0 auto;
}

.preview-canvas {
  position: absolute;
  left: 0;
  top: 0;
  width: 1440px;
  min-height: 750px;
  overflow: hidden;
  background: #fff;
  transform: scale(var(--preview-scale));
  transform-origin: top left;
}

.reference-panel {
  position: absolute;
  left: 12px;
  top: 58px;
  z-index: 40;
  display: flex;
  width: min(760px, calc(100vw - 24px));
  max-height: calc(100vh - 76px);
  flex-direction: column;
  overflow: auto;
  border: 1px solid #e5e6eb;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 18px 48px rgba(15, 23, 42, 0.16);
  padding: 20px 24px;
}

.reference-panel.is-change-panel {
  width: min(640px, calc(100vw - 24px));
}

.change-record-actions {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.change-record-actions button {
  border: 1px solid var(--brand-color, #a82126);
  border-radius: 8px;
  background: #fff;
  color: var(--brand-color, #a82126);
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
}
```

## Do Not

- Do not use a permanent left sidebar for the page catalog.
- Do not make PRD/change panels occupy a fixed right column.
- Do not put PRD or change-record copy inside the recreated product UI.
- Do not place `说明信息`, `素材库`, or `打开 Figma` in the top floating toolbar.
- Do not use passive status dots; status markers in the page catalog must be clickable buttons.
- Do not use fixed `zoom` values.
- Do not cap the preview scale at `1` for wide desktops.
- Do not leave decorative outer cards, heavy shadows, or large fixed margins around the canvas unless they exist in the Figma node itself.
