#!/usr/bin/env node
// Run with NODE_PATH set to an existing Playwright installation. No dependency install.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '../..');
const evidence = path.join(root, 'examples/component-reuse/evidence');
const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.json':'application/json'};
const server = http.createServer((req, res) => {
  const file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404); return res.end(); }
  res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
  res.end(fs.readFileSync(file));
});

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  fs.mkdirSync(evidence, {recursive:true});
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:900}});
  const failures = [], checks = [];
  page.on('pageerror', err => failures.push(String(err)));
  page.on('requestfailed', req => failures.push(`${req.url()}: ${req.failure()?.errorText}`));
  page.on('response', response => {if (response.status() >= 400) failures.push(`${response.status()} ${response.url()}`);});
  try {
    for (const protocol of ['http', 'file']) {
      for (const name of ['index.html', 'second.html']) {
        const route = `examples/component-reuse/project/${name}`;
        await page.goto(protocol === 'http' ? `${base}/${route}` : pathToFileURL(path.join(root, route)).href);
        const frame = page.frameLocator('#resource-note');
        const toggle = frame.getByRole('button', {name:'展开说明'});
        await toggle.click();
        assert.equal(await frame.getByRole('button', {name:'收起说明'}).getAttribute('aria-expanded'), 'true');
        assert.equal(await frame.locator('#details').isVisible(), true);
        await frame.getByRole('button', {name:'收起说明'}).click();
        assert.equal(await frame.locator('#details').isVisible(), false);
        assert.equal(await page.locator('h1').evaluate(el=>getComputedStyle(el).fontSize), '24px');
        checks.push(`${protocol}: ${name} expand/collapse, aria state, host CSS isolation`);
      }
    }
    const railRoute = '/assets/standards/v5/1.0.0/assets/standalone/history-rail.html';
    await page.setViewportSize({width:700,height:400});
    await page.goto(`${base}${railRoute}?conversation=04`);
    const rail = page.locator('[data-v5-history-rail]');
    assert.equal(await page.locator('.v5-history-rail__item[aria-current="page"]').count(), 1);
    assert.equal(await page.locator('.v5-history-rail__item[aria-current="page"]').getAttribute('href'), '?conversation=04');
    assert.equal(await page.locator('.v5-history-rail__ticks .current').count(), 1);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth), true);
    await rail.hover();
    await page.waitForFunction(()=>getComputedStyle(document.querySelector('.v5-history-rail__panel')).opacity === '1');
    await page.screenshot({path:path.join(evidence,'v5-history-expanded.png')});
    await rail.focus();
    await rail.press('Escape');
    assert.equal(await rail.evaluate(el=>el === document.activeElement), true);
    assert.equal(await rail.evaluate(el=>el.classList.contains('is-dismissed')), true);
    checks.push('V5 history: query=04, unique row/tick, hover open, Escape dismiss with focus retained, no 1440px host spill');
    await page.getByRole('button', {name:'打开模态确认'}).click();
    await page.waitForFunction(()=>document.querySelector('[data-v5-history-rail]').hidden);
    assert.equal(await rail.getAttribute('tabindex'), '-1');
    assert.equal(await page.locator('.v5-history-rail__item[tabindex="-1"]').count(),16);
    await page.screenshot({path:path.join(evidence,'v5-history-modal.png')});
    await page.getByRole('button', {name:'关闭确认'}).click();
    await page.waitForFunction(()=>!document.querySelector('[data-v5-history-rail]').hidden);
    assert.equal(await rail.getAttribute('tabindex'), '0');
    assert.equal(await page.locator('.v5-history-rail__item[tabindex="-1"]').count(),0);
    checks.push('V5 history: modal hides rail and removes 16 links from tab order; close restores them');
    await page.goto(`${base}${railRoute}?conversation=bad`);
    assert.equal(await page.locator('[aria-current="page"]').getAttribute('href'), '?conversation=01');
    checks.push('V5 history: invalid query falls back to 01');
    for (const folder of ['examples', 'examples-mobile']) {
      const dir = path.join(root,'assets/standards/v5/1.0.0/assets',folder);
      await page.setViewportSize(folder==='examples' ? {width:1440,height:900} : {width:375,height:812});
      for (const name of fs.readdirSync(dir).filter(name=>name.endsWith('.html'))) {
        await page.goto(`${base}/assets/standards/v5/1.0.0/assets/${folder}/${name}`);
        await page.waitForLoadState('load');
        const badImages = await page.locator('img').evaluateAll(images=>images.filter(img=>!img.complete || img.naturalWidth===0).map(img=>img.src));
        assert.deepEqual(badImages, [], `${folder}/${name} has broken images`);
        checks.push(`V5 ${folder}/${name}: rendered without failed image resources`);
        if (name==='chat-flow-full.html' || name==='mobile-chat.html') await page.screenshot({path:path.join(evidence,`${name.replace('.html','')}.png`),fullPage:true});
      }
    }
    assert.deepEqual(failures, [], 'runtime/resource failures');
    const report={ok:true,browser:await browser.version(),checks,errors:failures,limits:['No comparison with freshly exported Figma nodes.','Legacy full-page samples contain unconnected controls; only history interactions and reusable note interactions were exercised.','Image loading checks do not certify business-data consistency in legacy illustrative text.']};
    fs.writeFileSync(path.join(evidence,'browser-report.json'), JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report,null,2));
  } finally { await browser.close(); server.close(); }
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
