/* 原型走查导航器 · 通用引擎（review tool，非产品界面）
 * ------------------------------------------------------------------
 * 浮动列表按钮（默认左上角，可拖到页面任意位置）→ 弹出全站页面清单，按「关系分组·同类聚合」排列，点击跳转、当前页高亮。
 * 这是「稳定层」：直接 copy，**不改**。页面清单是「可变层」，写在 `_pagenav.pages.js`。
 *
 * 用法（每个原型页在 </body> 前引两行，pages 在前、engine 在后）：
 *   <script defer src="_pagenav.pages.js"></script>
 *   <script defer src="_pagenav.js"></script>
 * 由 `sync-pagenav.py` 自动注入 / 校验。
 *
 * 数据契约（_pagenav.pages.js 设置全局）：
 *   window.PGNAV_TITLE  = '页面走查导航';              // 可选
 *   window.PGNAV_GROUPS = [ { name:'分组名', items:[ ['文件.html','短标题', '编号?'], ... ] }, ... ];
 * 关系分组：把同一业务 / 同一 Agent / 同一流程的页面聚在一组。
 *
 * 拖拽：按钮可拖到页面任意位置，位置存 localStorage（跨页面/刷新保留，仅本机走查用，不影响产品数据）。
 * ------------------------------------------------------------------ */
(function () {
  var GROUPS = (typeof window !== 'undefined' && window.PGNAV_GROUPS) || [];
  var TITLE = (typeof window !== 'undefined' && window.PGNAV_TITLE) || '页面走查导航';
  if (!GROUPS.length) { try { console.warn('[pagenav] 未找到 window.PGNAV_GROUPS，请检查是否引入了 _pagenav.pages.js'); } catch (e) {} return; }

  var total = GROUPS.reduce(function (n, g) { return n + (g.items ? g.items.length : 0); }, 0);
  var cur = '';
  try { cur = decodeURIComponent((location.pathname.split('/').pop() || '')); } catch (e) { cur = location.pathname.split('/').pop() || ''; }
  function pageNo(file, given) { if (given != null && given !== '') return given; var m = String(file).match(/(?:页面|page)[-_]([0-9]+(?:-[0-9]+)?[a-zA-Z]?)[-_]/i); return m ? m[1] : ''; }

  var POS_KEY = 'pgnav-btn-pos';
  function loadPos() { try { var v = localStorage.getItem(POS_KEY); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
  function savePos(p) { try { localStorage.setItem(POS_KEY, JSON.stringify(p)); } catch (e) {} }

  var CSS = ''
    + '#pgnav-launch,#pgnav-panel,#pgnav-panel *{box-sizing:border-box}'
    + '#pgnav-launch{position:fixed;top:12px;left:calc((var(--v5-nav-width, 80px) - 40px) / 2);z-index:2147483600;width:40px;height:40px;border-radius:12px;border:1px solid rgba(20,26,45,.12);background:#fff;color:#2a3350;display:grid;place-items:center;cursor:grab;box-shadow:0 6px 20px rgba(20,26,45,.22);transition:box-shadow .12s ease;touch-action:none}'
    + '#pgnav-launch:hover{box-shadow:0 10px 26px rgba(20,26,45,.24)}'
    + '#pgnav-launch.on{background:#2b6cf6;color:#fff;border-color:#2b6cf6}'
    + '#pgnav-launch.dragging{cursor:grabbing;box-shadow:0 14px 32px rgba(20,26,45,.32)}'
    + '#pgnav-mask{position:fixed;inset:0;z-index:2147483500;background:transparent;display:none}'
    + '#pgnav-mask.show{display:block}'
    + '#pgnav-panel{position:fixed;top:62px;left:14px;z-index:2147483601;width:288px;max-height:82vh;overflow:auto;background:#fff;border:1px solid rgba(20,26,45,.12);border-radius:14px;box-shadow:0 18px 50px rgba(20,26,45,.28);padding:10px;display:none;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}'
    + '#pgnav-panel.show{display:block}'
    + '.pgnav-hd{display:flex;align-items:baseline;justify-content:space-between;gap:8px;padding:6px 8px 10px;border-bottom:1px solid rgba(20,26,45,.08);margin-bottom:8px}'
    + '.pgnav-hd b{font-size:13px;color:#141a2d;font-weight:600}'
    + '.pgnav-hd span{font-size:11px;color:#8b93a7;white-space:nowrap}'
    + '.pgnav-grp{margin-bottom:6px}'
    + '.pgnav-grp__t{display:flex;align-items:center;gap:6px;padding:8px 8px 4px;font-size:11px;font-weight:600;color:#6b7488;letter-spacing:.02em}'
    + '.pgnav-grp__c{font-size:10px;font-weight:600;color:#9aa2b4;background:#f0f2f7;border-radius:999px;padding:1px 7px}'
    + '.pgnav-i{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:9px;cursor:pointer;color:#374056;text-decoration:none;transition:background .1s ease}'
    + '.pgnav-i:hover{background:#f2f4f9}'
    + '.pgnav-i__no{flex:none;min-width:26px;height:20px;padding:0 5px;display:inline-grid;place-items:center;font-size:11px;font-weight:600;color:#8b93a7;background:#f0f2f7;border-radius:6px}'
    + '.pgnav-i__t{font-size:12.5px;line-height:1.3}'
    + '.pgnav-i.cur{background:#eaf1ff}'
    + '.pgnav-i.cur .pgnav-i__t{color:#2b6cf6;font-weight:600}'
    + '.pgnav-i.cur .pgnav-i__no{color:#fff;background:#2b6cf6}'
    + '.pgnav-i__now{margin-left:auto;flex:none;font-size:10px;font-weight:600;color:#2b6cf6;background:#dbe7ff;border-radius:999px;padding:1px 7px}';

  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }

  function build() {
    var style = document.createElement('style'); style.textContent = CSS; document.head.appendChild(style);

    var launch = h('button', null, '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="5" cy="6" r="1.5" fill="currentColor"/><circle cx="5" cy="12" r="1.5" fill="currentColor"/><circle cx="5" cy="18" r="1.5" fill="currentColor"/><path d="M9.5 6h10M9.5 12h10M9.5 18h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>');
    launch.id = 'pgnav-launch'; launch.type = 'button';
    launch.setAttribute('aria-label', TITLE); launch.title = TITLE + '（可拖动）';

    var mask = h('div'); mask.id = 'pgnav-mask';
    var panel = h('div'); panel.id = 'pgnav-panel';
    panel.appendChild(h('div', 'pgnav-hd', '<b>' + TITLE + '</b><span>共 ' + total + ' 页 · 仅走查用</span>'));

    GROUPS.forEach(function (g) {
      var items = g.items || [];
      var grp = h('div', 'pgnav-grp');
      grp.appendChild(h('div', 'pgnav-grp__t', (g.name || '') + '<span class="pgnav-grp__c">' + items.length + '</span>'));
      items.forEach(function (it) {
        var file = it[0], label = it[1] != null ? it[1] : it[0], no = pageNo(file, it[2]), isCur = file === cur;
        var a = h('a', 'pgnav-i' + (isCur ? ' cur' : ''));
        a.href = file;
        a.innerHTML = (no ? '<span class="pgnav-i__no">' + no + '</span>' : '')
          + '<span class="pgnav-i__t">' + label + '</span>'
          + (isCur ? '<span class="pgnav-i__now">当前</span>' : '');
        grp.appendChild(a);
      });
      panel.appendChild(grp);
    });

    function positionPanel() {
      var r = launch.getBoundingClientRect();
      var vw = window.innerWidth, vh = window.innerHeight;
      var pw = 288, gap = 8;
      var left = r.left, top = r.bottom + gap;
      // 面板右侧超出视口时改从按钮右边缘往左对齐
      if (left + pw > vw - gap) left = Math.max(gap, r.right - pw);
      // 下方放不下时改到按钮上方
      var estH = Math.min(vh * 0.82, 480);
      if (top + estH > vh - gap) top = Math.max(gap, r.top - estH - gap);
      panel.style.left = left + 'px';
      panel.style.top = top + 'px';
    }

    function open() { positionPanel(); panel.classList.add('show'); mask.classList.add('show'); launch.classList.add('on'); }
    function close() { panel.classList.remove('show'); mask.classList.remove('show'); launch.classList.remove('on'); }
    function toggle() { panel.classList.contains('show') ? close() : open(); }

    // ---- 恢复上次拖拽位置（跨页面共用，仅本机 localStorage，不入产品数据） ----
    var saved = loadPos();
    if (saved && typeof saved.left === 'number' && typeof saved.top === 'number') {
      launch.style.left = saved.left + 'px';
      launch.style.top = saved.top + 'px';
    }

    // ---- 拖拽逻辑：pointerdown 记录起点，移动超过阈值判定为拖拽（不触发点击） ----
    var dragging = false, moved = false, startX = 0, startY = 0, baseLeft = 0, baseTop = 0;
    var THRESHOLD = 4;

    launch.addEventListener('pointerdown', function (e) {
      if (e.button != null && e.button !== 0) return;
      dragging = true; moved = false;
      startX = e.clientX; startY = e.clientY;
      var r = launch.getBoundingClientRect();
      baseLeft = r.left; baseTop = r.top;
      try { launch.setPointerCapture(e.pointerId); } catch (err) {}
    });

    launch.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var dx = e.clientX - startX, dy = e.clientY - startY;
      if (!moved && (Math.abs(dx) > THRESHOLD || Math.abs(dy) > THRESHOLD)) {
        moved = true;
        launch.classList.add('dragging');
        if (panel.classList.contains('show')) close();
      }
      if (!moved) return;
      var w = launch.offsetWidth, hgt = launch.offsetHeight;
      var nl = clamp(baseLeft + dx, 4, window.innerWidth - w - 4);
      var nt = clamp(baseTop + dy, 4, window.innerHeight - hgt - 4);
      launch.style.left = nl + 'px';
      launch.style.top = nt + 'px';
    });

    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      launch.classList.remove('dragging');
      if (moved) {
        var r = launch.getBoundingClientRect();
        savePos({ left: r.left, top: r.top });
      }
      try { launch.releasePointerCapture(e.pointerId); } catch (err) {}
    }
    launch.addEventListener('pointerup', endDrag);
    launch.addEventListener('pointercancel', endDrag);

    launch.addEventListener('click', function (e) {
      e.stopPropagation();
      if (moved) { moved = false; return; } // 刚拖拽完的这次 click 不当作开关面板
      toggle();
    });

    mask.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    window.addEventListener('resize', function () { if (panel.classList.contains('show')) positionPanel(); });

    document.body.appendChild(mask);
    document.body.appendChild(launch);
    document.body.appendChild(panel);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
