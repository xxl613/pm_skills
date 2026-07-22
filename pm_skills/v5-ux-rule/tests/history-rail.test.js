const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const { fileURLToPath, pathToFileURL } = require('node:url');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const component = 'assets/components/history-rail.html';
const standardPages = [
  'assets/shell/chat-flow.html',
  'assets/shell/drawer.html',
  'assets/shell/drawer-half.html',
  'assets/examples/chat-flow-full.html',
  'assets/examples/chat-flow-execution.html',
  'assets/examples/chat-flow-plan-edit.html',
];
const allRailPages = [component, ...standardPages];
const expectedTitles = [
  '当前对话',
  ...Array.from({ length: 15 }, (_, index) => `历史对话 ${String(index + 2).padStart(2, '0')}`),
];

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8');
}

function normalize(value) {
  return value.replace(/\s+/g, ' ').trim();
}

function getAttribute(tag, name) {
  const match = tag.match(new RegExp(`\\b${name}="([^"]*)"`, 'i'));
  return match ? match[1] : null;
}

function decodeHtmlEntities(value) {
  const named = {
    amp: '&',
    apos: "'",
    colon: ':',
    gt: '>',
    lt: '<',
    newline: '\n',
    quot: '"',
    tab: '\t',
  };

  return value.replace(/&(#x[0-9a-f]+|#[0-9]+|amp|apos|colon|gt|lt|newline|quot|tab);?/gi, (match, entity) => {
    const normalized = entity.toLowerCase();
    if (normalized.startsWith('#x')) return String.fromCodePoint(Number.parseInt(normalized.slice(2), 16));
    if (normalized.startsWith('#')) return String.fromCodePoint(Number.parseInt(normalized.slice(1), 10));
    return named[normalized] ?? match;
  });
}

function extractRail(html, label) {
  const rails = html.match(/<aside\b[^>]*data-v5-history-rail[^>]*>[\s\S]*?<\/aside>/g) || [];
  assert.equal(rails.length, 1, `${label}: expected one History Rail`);
  return rails[0];
}

function extractInitializer(html, label) {
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((match) => match[1]);
  const initializer = scripts.find((script) => script.includes("document.querySelectorAll('[data-v5-history-rail]')"));
  assert.ok(initializer, `${label}: missing complete History Rail initializer`);
  return initializer.trim();
}

function extractRailCss(html, label) {
  const match = html.match(/\.v5-main\s*\{\s*position:\s*relative;\s*\}[\s\S]*?\.v5-history-rail\.is-dismissed \.v5-history-rail__ticks\s*\{[^}]*opacity:\s*1;[^}]*\}/);
  assert.ok(match, `${label}: missing complete History Rail CSS`);
  return match[0];
}

function assertSafeSelfQuery(href, relativePath, label) {
  const decoded = decodeHtmlEntities(href).trim();
  const schemeProbe = decoded.replace(/[\u0000-\u0020\u007f-\u009f]/g, '');
  assert.doesNotMatch(schemeProbe, /^(?:javascript|data|vbscript):/i, `${label}: unsafe href ${href}`);

  const localPath = path.join(root, relativePath);
  const resolved = new URL(decoded, pathToFileURL(localPath));
  assert.equal(resolved.protocol, 'file:', `${label}: history href must remain local`);
  assert.equal(fileURLToPath(resolved), localPath, `${label}: self-query must resolve to its containing HTML file`);
  assert.equal(resolved.hash, '', `${label}: history href must not use an unresolved fragment`);
  assert.match(resolved.search, /^\?conversation=(?:0[1-9]|1[0-6])$/, `${label}: invalid conversation query`);
}

function assertRailDataContract(html, label, relativePath) {
  const rail = extractRail(html, label);
  const railOpening = rail.match(/^<aside\b[^>]*>/i)[0];
  assert.equal(getAttribute(railOpening, 'tabindex'), '0', `${label}: rail must start in the tab order`);
  assert.ok(getAttribute(railOpening, 'aria-label')?.trim(), `${label}: rail needs a usable aria-label`);

  const ticksContainer = rail.match(/<div\b[^>]*class="v5-history-rail__ticks"[^>]*>([\s\S]*?)<\/div>/);
  assert.ok(ticksContainer, `${label}: missing tick container`);
  const ticks = ticksContainer[1].match(/<i\b[^>]*>/g) || [];
  assert.equal(ticks.length, 16, `${label}: expected 16 ticks`);
  assert.equal(ticks.filter((tick) => /\bcurrent\b/.test(getAttribute(tick, 'class') || '')).length, 1, `${label}: expected one current tick`);

  const panel = rail.match(/<nav\b[^>]*class="v5-history-rail__panel"[^>]*>/);
  assert.ok(panel, `${label}: missing history navigation panel`);
  assert.ok(getAttribute(panel[0], 'aria-label')?.trim(), `${label}: panel needs a usable aria-label`);
  assert.doesNotMatch(panel[0], /aria-modal|v5-overlay|v5-modal-mask/, `${label}: history panel must not identify as a modal`);

  const links = rail.match(/<a\b[^>]*class="[^"]*v5-history-rail__item[^"]*"[^>]*>[\s\S]*?<\/a>/g) || [];
  assert.equal(links.length, 16, `${label}: expected 16 history links`);
  assert.equal(links.filter((link) => /\bis-current\b/.test(link)).length, 1, `${label}: expected one current row`);
  assert.equal(links.filter((link) => /\baria-current=/.test(link)).length, 1, `${label}: expected exactly one aria-current`);
  assert.match(links[0], /\bis-current\b/);
  assert.match(links[0], /aria-current="page"/);

  const titles = links.map((link, index) => {
    const opening = link.match(/^<a\b[^>]*>/i)[0];
    const href = getAttribute(opening, 'href');
    const title = getAttribute(opening, 'title');
    const text = link.replace(/^<a\b[^>]*>/i, '').replace(/<\/a>$/i, '').trim();
    assert.ok(href, `${label}: row ${index + 1} needs an href`);
    assert.ok(title?.trim(), `${label}: row ${index + 1} needs a usable title`);
    assert.ok(text, `${label}: row ${index + 1} needs visible text`);
    assert.equal(title, text, `${label}: row ${index + 1} title and text must agree`);
    assertSafeSelfQuery(href, relativePath, `${label}: row ${index + 1}`);
    return text;
  });

  assert.deepEqual(titles, expectedTitles, `${label}: history titles must stay generic and neutral`);
  assert.doesNotMatch(rail, /气道|心衰|患者|护理|导管|输血|压疮|呼吸机|镇静|外渗|跌倒|血管活性|SBAR/, `${label}: project-specific clinical copy leaked into the standard component`);
  return rail;
}

function createClassList(initial = '') {
  const values = new Set(initial.split(/\s+/).filter(Boolean));
  return {
    add(name) { values.add(name); },
    contains(name) { return values.has(name); },
    remove(name) { values.delete(name); },
    toggle(name, force) {
      if (force === undefined) {
        if (values.has(name)) values.delete(name);
        else values.add(name);
        return values.has(name);
      }
      if (force) values.add(name);
      else values.delete(name);
      return force;
    },
  };
}

function createElement(initialClass = '', initialAttributes = {}) {
  const attributes = new Map(Object.entries(initialAttributes));
  const listeners = new Map();
  let hidden = false;

  return {
    classList: createClassList(initialClass),
    computedStyle: { display: 'block', opacity: '1', visibility: 'visible' },
    focused: false,
    focusOptions: null,
    rendered: true,
    addEventListener(type, handler) {
      const handlers = listeners.get(type) || [];
      handlers.push(handler);
      listeners.set(type, handlers);
    },
    dispatch(type, event = {}) {
      for (const handler of listeners.get(type) || []) handler(event);
    },
    focus(options) {
      this.focused = true;
      this.focusOptions = options;
    },
    getAttribute(name) {
      return attributes.has(name) ? attributes.get(name) : null;
    },
    getClientRects() {
      return this.rendered && !hidden ? [{}] : [];
    },
    hasAttribute(name) {
      return attributes.has(name);
    },
    removeAttribute(name) {
      attributes.delete(name);
    },
    setAttribute(name, value) {
      attributes.set(name, String(value));
    },
    get hidden() {
      return hidden;
    },
    set hidden(value) {
      hidden = Boolean(value);
      if (hidden) attributes.set('hidden', '');
      else attributes.delete('hidden');
    },
  };
}

function runInitializer(initializer, search = '', initialModals = []) {
  const items = Array.from({ length: 16 }, (_, index) => createElement(
    index === 0 ? 'v5-history-rail__item is-current' : 'v5-history-rail__item',
    {
      href: `?conversation=${String(index + 1).padStart(2, '0')}`,
      ...(index === 0 ? { 'aria-current': 'page' } : {}),
    },
  ));
  const ticks = Array.from({ length: 16 }, (_, index) => createElement(index === 0 ? 'current' : ''));
  const rail = createElement('v5-history-rail', { 'aria-label': '历史对话', tabindex: '0' });
  const modals = [...initialModals];
  let observerCallback = null;
  let observerOptions = null;

  rail.querySelectorAll = (selector) => {
    if (selector === '.v5-history-rail__item') return items;
    if (selector === '.v5-history-rail__ticks i') return ticks;
    return [];
  };
  rail.contains = (target) => target === rail || items.includes(target) || ticks.includes(target);

  const document = {
    documentElement: createElement(),
    querySelectorAll(selector) {
      if (selector === '[data-v5-history-rail]') return [rail];
      if (selector === '[aria-modal="true"], .v5-overlay, .v5-modal-mask') return modals;
      return [];
    },
  };

  class FakeMutationObserver {
    constructor(callback) {
      observerCallback = callback;
    }
    observe(target, options) {
      assert.equal(target, document.documentElement);
      observerOptions = options;
    }
  }

  const window = {
    location: { href: `file:///history-rail.html${search}`, search },
    getComputedStyle(element) { return element.computedStyle; },
    MutationObserver: FakeMutationObserver,
    URLSearchParams,
  };

  vm.runInNewContext(initializer, { document, MutationObserver: FakeMutationObserver, URLSearchParams, window });
  return {
    items,
    modals,
    observerOptions: () => observerOptions,
    rail,
    ticks,
    triggerMutation() {
      assert.ok(observerCallback, 'initializer must install a MutationObserver');
      observerCallback([]);
    },
  };
}

function currentIndexes(elements, className) {
  return elements.flatMap((element, index) => element.classList.contains(className) ? [index] : []);
}

test('canonical and desktop assets keep strict neutral markup and safe self-query links', () => {
  for (const file of allRailPages) {
    assertRailDataContract(read(file), file, file);
  }
});

test('history href validation decodes entities before rejecting unsafe schemes', () => {
  for (const href of [
    '  &#x6a;avascript&#58;alert(1)',
    '&NewLine;data&colon;text/html,unsafe',
    '&#118;bscript&#58;msgbox(1)',
  ]) {
    assert.throws(
      () => assertSafeSelfQuery(href, component, component),
      /unsafe href/,
      `${href} must be rejected after entity decoding`,
    );
  }
});

test('canonical history rail keeps the Figma geometry and a visible focus treatment', () => {
  const html = read(component);
  assert.match(html, /<!doctype html>/i);
  assert.match(html, /\.v5-history-rail\s*\{[^}]*width:\s*32px[^}]*height:\s*168px[^}]*right:\s*0[^}]*top:\s*50%/s);
  assert.match(html, /\.v5-history-rail__ticks i\.current\s*\{[^}]*width:\s*32px[^}]*background:\s*#1d2129/s);
  assert.match(html, /\.v5-history-rail__panel\s*\{[^}]*width:\s*300px[^}]*height:\s*244px[^}]*border-radius:\s*16px/s);
  assert.match(html, /\.v5-history-rail__item\s*\{[^}]*height:\s*38px/s);
  assert.match(html, /\.v5-history-rail:hover \.v5-history-rail__panel,\s*\.v5-history-rail:focus-within \.v5-history-rail__panel/);
  const focusRule = html.match(/\.v5-history-rail:focus-visible\s*\{([^}]*)\}/);
  assert.ok(focusRule, 'rail needs a :focus-visible rule');
  assert.match(focusRule[1], /outline:\s*(?!none\b)[^;]+;/, 'focus-visible treatment must be visibly rendered');
});

test('initializer applies query state, Escape behavior, and modal exclusion lifecycle', () => {
  const initializer = extractInitializer(read(component), component);
  assert.doesNotMatch(initializer, /innerHTML|insertAdjacentHTML|document\.write/, 'query state must not inject HTML');

  const queryState = runInitializer(initializer, '?conversation=09');
  assert.deepEqual(currentIndexes(queryState.items, 'is-current'), [8]);
  assert.deepEqual(currentIndexes(queryState.ticks, 'current'), [8]);
  assert.deepEqual(queryState.items.flatMap((item, index) => item.getAttribute('aria-current') === 'page' ? [index] : []), [8]);
  assert.equal(queryState.rail.hidden, false, 'pages without visible modals must keep the rail available');
  assert.equal(queryState.rail.getAttribute('tabindex'), '0');
  assert.ok(queryState.items.every((item) => item.getAttribute('tabindex') === null));

  const invalidState = runInitializer(initializer, '?conversation=99');
  assert.deepEqual(currentIndexes(invalidState.items, 'is-current'), [0], 'invalid query must safely fall back to 01');
  assert.deepEqual(currentIndexes(invalidState.ticks, 'current'), [0]);

  let prevented = false;
  queryState.rail.dispatch('keydown', {
    key: 'Escape',
    preventDefault() { prevented = true; },
  });
  assert.equal(prevented, true);
  assert.equal(queryState.rail.classList.contains('is-dismissed'), true);
  assert.equal(queryState.rail.focused, true);
  assert.equal(queryState.rail.focusOptions.preventScroll, true);
  queryState.rail.dispatch('pointerenter');
  assert.equal(queryState.rail.classList.contains('is-dismissed'), false);

  const modal = createElement('v5-overlay', { 'aria-modal': 'true' });
  const modalState = runInitializer(initializer, '?conversation=04', [modal]);
  assert.equal(modalState.rail.hidden, true);
  assert.equal(modalState.rail.getAttribute('aria-hidden'), 'true');
  assert.equal(modalState.rail.getAttribute('tabindex'), '-1');
  assert.ok(modalState.items.every((item) => item.getAttribute('tabindex') === '-1'));

  const observerOptions = modalState.observerOptions();
  assert.equal(observerOptions.attributes, true);
  assert.equal(observerOptions.childList, true);
  assert.equal(observerOptions.subtree, true);
  for (const attribute of ['aria-hidden', 'aria-modal', 'class', 'hidden', 'style']) {
    assert.ok(observerOptions.attributeFilter.includes(attribute), `observer must watch ${attribute}`);
  }

  modal.computedStyle.display = 'none';
  modal.rendered = false;
  modalState.triggerMutation();
  assert.equal(modalState.rail.hidden, false);
  assert.equal(modalState.rail.getAttribute('aria-hidden'), null);
  assert.equal(modalState.rail.getAttribute('tabindex'), '0');
  assert.ok(modalState.items.every((item) => item.getAttribute('tabindex') === null));

  modal.computedStyle.display = 'block';
  modal.rendered = true;
  modalState.triggerMutation();
  assert.equal(modalState.rail.hidden, true);
  modalState.modals.splice(0, 1);
  modalState.triggerMutation();
  assert.equal(modalState.rail.hidden, false);
});

test('all desktop assets copy the complete canonical markup, CSS, and initializer', () => {
  const canonicalHtml = read(component);
  const canonicalRail = normalize(extractRail(canonicalHtml, component));
  const canonicalCss = normalize(extractRailCss(canonicalHtml, component));
  const canonicalInitializer = normalize(extractInitializer(canonicalHtml, component));
  assert.match(canonicalInitializer, /URLSearchParams/);
  assert.match(canonicalInitializer, /MutationObserver/);
  assert.match(canonicalInitializer, /\[aria-modal="true"\], \.v5-overlay, \.v5-modal-mask/);

  for (const file of standardPages) {
    const html = read(file);
    assert.equal(normalize(extractRail(html, file)), canonicalRail, `${file}: canonical rail markup drift`);
    assert.equal(normalize(extractRailCss(html, file)), canonicalCss, `${file}: canonical rail CSS drift`);
    assert.equal(normalize(extractInitializer(html, file)), canonicalInitializer, `${file}: canonical initializer drift`);
    assert.doesNotMatch(html, /topbar-history\.svg|aria-label="历史对话"[^>]*><img|aria-label="对话"[^>]*><svg|v5-minimap/, file);

    const main = html.match(/<main\b[^>]*class="[^"]*v5-main[^"]*"[^>]*>([\s\S]*?)<\/main>/);
    assert.ok(main, `${file}: missing .v5-main`);
    assert.match(main[1], /data-v5-history-rail/, `${file}: rail must be anchored inside .v5-main`);
    assert.match(main[1], /data-v5-history-rail[\s\S]*class="v5-dock-wrap"/, `${file}: rail must precede .v5-dock-wrap`);
  }
});

test('skill instructions make the desktop component and overlay behavior mandatory', () => {
  const skill = read('SKILL.md');
  const components = read('references/03-components.md');
  const patterns = read('references/05-ai-patterns.md');

  assert.match(skill, /历史对话轨道铁律（V5 History Rail）/);
  assert.match(skill, /不得同时保留顶部历史按钮/);
  assert.match(skill, /模态遮罩出现时隐藏且禁止聚焦/);
  assert.match(skill, /移动端不套用该桌面组件/);

  assert.match(components, /history-rail\.html/);
  assert.match(components, /16 条消息刻度/);
  assert.match(components, /300×244/);
  assert.match(components, /38px/);
  assert.match(components, /aria-current="page"/);
  assert.match(components, /Escape/);

  assert.match(patterns, /V5 History Rail/);
  assert.match(patterns, /history-rail\.html/);
  assert.doesNotMatch(patterns, /消息小地图|\.v5-minimap/);
});
