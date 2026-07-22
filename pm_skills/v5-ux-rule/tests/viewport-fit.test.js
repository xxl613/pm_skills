const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const root = path.resolve(__dirname, '..');

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8');
}

test('desktop prototypes use a 1440 design canvas scaled strictly by viewport width', () => {
  const skill = read('SKILL.md');
  const shellRules = read('references/02-page-shell.md');
  const checklist = read('references/99-review-checklist.md');

  assert.match(skill, /桌面宽度适配铁律/);
  assert.match(skill, /viewportWidth\s*\/\s*1440/);
  assert.match(skill, /_viewport-fit\.js/);
  assert.match(skill, /sync-viewport-fit\.py --check/);
  assert.match(shellRules, /显示比例\s*=\s*viewportWidth\s*\/\s*1440/);
  assert.match(shellRules, /不按高度二次缩放/);
  assert.doesNotMatch(shellRules, /定制时若需响应式/);
  assert.match(checklist, /桌面 1440 画布已按视口宽度等比缩放/);
});

test('the stable viewport engine wraps desktop content and leaves review tools unscaled', () => {
  const runtime = read('assets/project-profile/_viewport-fit.js');

  assert.match(runtime, /BASE_WIDTH\s*=\s*1440/);
  assert.match(runtime, /window\.innerWidth\s*\/\s*BASE_WIDTH/);
  assert.doesNotMatch(runtime, /Math\.max\(0\.1,\s*window\.innerWidth\s*\/\s*BASE_WIDTH\)/);
  assert.match(runtime, /v5-viewport-stage/);
  assert.match(runtime, /v5-viewport-canvas/);
  assert.match(runtime, /transformOrigin\s*=\s*'top left'/);
  assert.match(runtime, /window\.addEventListener\('resize'/);
  assert.match(runtime, /ResizeObserver/);
  assert.match(runtime, /v5m-|data-v5-platform/);
  assert.match(runtime, /tagName\s*===\s*'SCRIPT'/);
  assert.match(runtime, /pgnav/);
});

test('the viewport injector adds desktop references, skips mobile pages, and is idempotent', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-viewport-fit-'));
  const injector = path.join(root, 'assets/project-profile/sync-viewport-fit.py');
  const runtime = path.join(root, 'assets/project-profile/_viewport-fit.js');
  fs.copyFileSync(injector, path.join(temp, 'sync-viewport-fit.py'));
  fs.copyFileSync(runtime, path.join(temp, '_viewport-fit.js'));
  fs.writeFileSync(path.join(temp, '页面-01-desktop.html'), '<!doctype html><html><body><main class="v5-app"></main></body></html>\n');
  fs.writeFileSync(path.join(temp, '页面-02-mobile.html'), '<!doctype html><html><body><main class="v5m-app"></main></body></html>\n');

  const first = spawnSync('python3', ['sync-viewport-fit.py'], { cwd: temp, encoding: 'utf8' });
  assert.equal(first.status, 0, first.stderr || first.stdout);
  const desktop = fs.readFileSync(path.join(temp, '页面-01-desktop.html'), 'utf8');
  const mobile = fs.readFileSync(path.join(temp, '页面-02-mobile.html'), 'utf8');
  assert.equal((desktop.match(/src="_viewport-fit\.js"/g) || []).length, 1);
  assert.doesNotMatch(mobile, /_viewport-fit\.js/);

  const check = spawnSync('python3', ['sync-viewport-fit.py', '--check'], { cwd: temp, encoding: 'utf8' });
  assert.equal(check.status, 0, check.stderr || check.stdout);
  const second = spawnSync('python3', ['sync-viewport-fit.py'], { cwd: temp, encoding: 'utf8' });
  assert.equal(second.status, 0, second.stderr || second.stdout);
  const desktopAgain = fs.readFileSync(path.join(temp, '页面-01-desktop.html'), 'utf8');
  assert.equal((desktopAgain.match(/src="_viewport-fit\.js"/g) || []).length, 1);
});
