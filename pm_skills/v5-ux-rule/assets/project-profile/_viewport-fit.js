/* V5 desktop viewport fit (stable layer)
 * Keeps a 1440px design coordinate system and scales the whole product canvas
 * by viewport width. Review tools such as pgnav stay outside the scaled canvas.
 */
(function () {
  'use strict';

  var BASE_WIDTH = 1440;
  var MIN_DESIGN_HEIGHT = 750;
  var stage = null;
  var canvas = null;
  var scale = 1;

  function isMobilePage() {
    return Boolean(document.querySelector('[data-v5-platform="mobile"], [class*="v5m-"]'));
  }

  function isReviewTool(node) {
    return node.nodeType === 1 && (
      node.tagName === 'SCRIPT' ||
      /^pgnav/.test(node.id || '') ||
      node.hasAttribute('data-v5-review-tool')
    );
  }

  function installStyles() {
    var style = document.createElement('style');
    style.setAttribute('data-v5-viewport-fit-style', '');
    style.textContent = ''
      + 'html{width:100%;min-width:0}'
      + 'body.v5-viewport-fit{display:block!important;width:100%!important;min-width:0!important;height:auto!important;min-height:100vh!important;margin:0!important;overflow-x:hidden!important}'
      + '.v5-viewport-stage{position:relative;margin:0 auto;overflow:visible}'
      + '.v5-viewport-canvas{position:relative;width:1440px;min-height:750px;transform-origin:top left}';
    document.head.appendChild(style);
  }

  function copyBodyLayout(target, computed) {
    var display = computed.display;
    target.style.display = display === 'inline' || display === 'contents' ? 'block' : display;
    target.style.flexDirection = computed.flexDirection;
    target.style.flexWrap = computed.flexWrap;
    target.style.alignItems = computed.alignItems;
    target.style.alignContent = computed.alignContent;
    target.style.justifyContent = computed.justifyContent;
    target.style.gap = computed.gap;
    target.style.gridTemplateColumns = computed.gridTemplateColumns;
    target.style.gridTemplateRows = computed.gridTemplateRows;
    target.style.background = computed.background;
    target.style.color = computed.color;
    target.style.overflowX = computed.overflowX;
    target.style.overflowY = computed.overflowY;
  }

  function syncStageHeight() {
    if (!stage || !canvas) return;
    var renderedHeight = Math.max(canvas.scrollHeight, parseFloat(canvas.style.height) || 0) * scale;
    stage.style.height = Math.max(window.innerHeight, renderedHeight) + 'px';
  }

  function fit() {
    if (!stage || !canvas) return;
    scale = window.innerWidth / BASE_WIDTH;
    if (!Number.isFinite(scale) || scale <= 0) return;
    var designViewportHeight = Math.max(MIN_DESIGN_HEIGHT, window.innerHeight / scale);
    document.documentElement.style.setProperty('--v5-viewport-scale', scale);
    canvas.style.width = BASE_WIDTH + 'px';
    canvas.style.height = designViewportHeight + 'px';
    canvas.style.transform = 'scale(' + scale + ')';
    canvas.style.transformOrigin = 'top left';
    stage.style.width = window.innerWidth + 'px';
    window.requestAnimationFrame(syncStageHeight);
  }

  function init() {
    if (isMobilePage() || document.querySelector('.v5-viewport-stage')) return;

    var body = document.body;
    var computed = window.getComputedStyle(body);
    var nodes = Array.prototype.slice.call(body.childNodes).filter(function (node) {
      return !isReviewTool(node);
    });

    installStyles();
    stage = document.createElement('div');
    stage.className = 'v5-viewport-stage';
    stage.setAttribute('data-v5-viewport-stage', '');
    canvas = document.createElement('div');
    canvas.className = 'v5-viewport-canvas';
    canvas.setAttribute('data-v5-viewport-canvas', '');
    copyBodyLayout(canvas, computed);

    body.insertBefore(stage, body.firstChild);
    stage.appendChild(canvas);
    nodes.forEach(function (node) { canvas.appendChild(node); });
    body.classList.add('v5-viewport-fit');

    fit();
    window.addEventListener('resize', fit);
    window.addEventListener('load', fit);
    if (window.ResizeObserver) new ResizeObserver(syncStageHeight).observe(canvas);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
