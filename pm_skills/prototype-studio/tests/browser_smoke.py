#!/usr/bin/env python3
"""Exercise the coherent fixture after copying or exporting it. Requires Playwright Chromium."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--evidence', required=True, type=Path)
    args = parser.parse_args(); project = args.project.resolve(); evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    errors, checks = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1360, 'height': 980}, offline=True)
        page = context.new_page(); page.on('pageerror', lambda error: errors.append(str(error)))
        index = (project / 'index.html').as_uri(); summary = (project / 'summary.html').as_uri()
        page.goto(index); page.locator('#reset').click()
        expect(page.locator('[data-stat="total"]')).to_have_text('3')
        expect(page.get_by_role('button', name='打开页面列表', exact=True)).to_be_visible()
        page.get_by_role('button', name='打开当前页面 PRD', exact=True).click()
        expect(page.locator('#ps-panel-title')).to_have_text('全部记录 · PRD')
        source = (project / 'prd/records.md').read_text()
        assert page.locator('.ps-source pre').text_content() == source
        expect(page.get_by_text('用户未评审', exact=False)).to_be_visible()
        page.keyboard.press('Escape')
        expect(page.get_by_role('button', name='打开当前页面 PRD', exact=True)).to_be_focused()
        checks.append('offline complete PRD and separate user review status')
        # An in-memory fixture exercises rendering without editing the project's PRD files.
        table_fixture = '| 说明项 | 具体内容 |\n|---|---|\n| 状态选项 | 未完成 \\| 已完成 |\n| 空内容 | |\n'
        page.evaluate('(text) => { window.PROTOTYPE_REVIEW_DATA.pages[0].prdMarkdown = text; }', table_fixture)
        page.get_by_role('button', name='打开当前页面 PRD', exact=True).click()
        rows = page.locator('.ps-markdown tbody tr')
        expect(rows.nth(0).locator('td')).to_have_count(2)
        expect(rows.nth(0).locator('td').nth(1)).to_have_text('未完成 | 已完成')
        expect(rows.nth(1).locator('td')).to_have_count(2)
        expect(rows.nth(1).locator('td').nth(1)).to_have_text('')
        page.keyboard.press('Escape')
        page.evaluate('(text) => { window.PROTOTYPE_REVIEW_DATA.pages[0].prdMarkdown = text; }', source)
        checks.append('escaped Markdown pipes retain table columns and empty cells')
        page.locator('#new-title').fill('离线跨页测试'); page.locator('#create-form button').click()
        expect(page.locator('[data-stat="total"]')).to_have_text('4')
        row = page.locator('.record').filter(has_text='离线跨页测试')
        row.get_by_role('button', name='编辑', exact=True).click()
        page.locator('#edit-title').fill('离线跨页已编辑'); page.locator('#edit-form button[type="submit"]').click()
        row = page.locator('.record').filter(has_text='离线跨页已编辑')
        row.get_by_role('button', name='标为完成', exact=True).click()
        page.goto(summary)
        expect(page.locator('[data-stat="total"]')).to_have_text('4')
        expect(page.locator('[data-stat="open"]')).to_have_text('2')
        expect(page.locator('[data-stat="done"]')).to_have_text('2')
        expect(page.locator('.record').filter(has_text='离线跨页已编辑')).to_have_count(1)
        checks.append('offline create/edit/status share records and derived 4/2/2 across files')
        page.goto(summary + '?view=active#records')
        expect(page.locator('#visible-count')).to_have_text('2')
        expect(page.locator('.record').filter(has_text='离线跨页已编辑')).to_have_count(0)
        page.get_by_role('button', name='打开当前页面 PRD', exact=True).click()
        expect(page.locator('#ps-panel-title')).to_have_text('仅未完成记录 · PRD')
        page.screenshot(path=str(evidence / 'offline-scene-prd.png'), full_page=True)
        page.keyboard.press('Escape')
        page.goto(summary + '?view=unknown#records')
        page.get_by_role('button', name='打开当前页面 PRD', exact=True).click()
        expect(page.get_by_role('alert')).to_contain_text('未登记')
        checks.append('query/hash binding and unknown route rejection')
        page.goto(index)
        row = page.locator('.record').filter(has_text='离线跨页已编辑')
        row.get_by_role('button', name='删除', exact=True).click(); page.locator('#delete-cancel').click()
        expect(page.locator('[data-stat="total"]')).to_have_text('4')
        row.get_by_role('button', name='删除', exact=True).click(); page.locator('#delete-confirm').click()
        page.goto(summary)
        expect(page.locator('[data-stat="total"]')).to_have_text('3')
        expect(page.locator('[data-stat="open"]')).to_have_text('2')
        expect(page.locator('[data-stat="done"]')).to_have_text('1')
        checks.append('cancel is inert; confirmed deletion updates cross-page counts to 3/2/1')
        page.goto(index); page.get_by_role('button', name='打开页面列表', exact=True).click()
        expect(page.locator('nav[aria-label="原型页面"] li')).to_have_count(3)
        page.screenshot(path=str(evidence / 'offline-page-list.png'), full_page=True)
        page.keyboard.press('Escape')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.get_by_role('button', name='打开当前页面 PRD', exact=True).click()
        panel = page.locator('.ps-panel').bounding_box()
        assert panel['x'] >= 0 and panel['x'] + panel['width'] <= 391
        page.screenshot(path=str(evidence / 'offline-mobile-prd.png'), full_page=True)
        checks.append('page-list coverage and mobile review panel containment')
        assert not errors, errors
        report = {'ok': True, 'browser': browser.version, 'project': str(project), 'transport': 'file://',
                  'network': 'Playwright offline mode', 'checks': checks, 'pageErrors': errors,
                  'limits': 'This fixture and Chromium only; not all project behaviors or other browser file-origin policies.'}
        (evidence / 'browser-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        context.close(); browser.close()


if __name__ == '__main__':
    main()
