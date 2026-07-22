#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync-nav.py — 导航单一来源同步器（项目级工具）
============================================================
静态原型用 file:// 打开无法真正 include 公共导航，故约定：
  `_nav.html` 是导航唯一真源（母版），各 `页面-*.html` 内各存一份拷贝。
本脚本把母版的 <nav class="v5-nav"> 块回灌到所有页面，并按 ACTIVE_MAP
为每页设置高亮项 —— 改导航只改母版 + 跑一次脚本，全站零漏改。

用法（在本目录运行）：
  python3 sync-nav.py            # 回灌：把母版同步到所有页面
  python3 sync-nav.py --check    # 只检测：有漂移则列出并以退出码 1 返回，不改文件

ACTIVE_MAP：页面文件名 → 该页高亮的导航项（按 v5-nav__cap 文本）。
未列出的页面用 DEFAULT_ACTIVE。新增页面/改高亮，编辑下面两处即可。
============================================================
"""
import re, sys, glob, os

MASTER = "_nav.html"
PAGE_GLOB = "页面-*.html"
DEFAULT_ACTIVE = ""  # 留空=各页逐字照搬母版（含母版自带高亮）；要按页设高亮则填默认项名
ACTIVE_MAP = {
    # "页面-02-交小研AI对话首页.html": "交小研",
    # "页面-XX-课程页.html": "工作台",
}

NAV_RE = re.compile(r'<nav class="v5-nav">.*?</nav>', re.S)


def extract_master_nav(text: str) -> str:
    """取母版里真正的 nav 块（含 v5-nav__items，跳过注释里的示例文字）。"""
    blocks = [m.group(0) for m in NAV_RE.finditer(text) if "v5-nav__items" in m.group(0)]
    if not blocks:
        sys.exit(f"[sync-nav] 母版 {MASTER} 未找到 <nav class=\"v5-nav\"> 块")
    return blocks[-1]


def strip_active(nav: str) -> str:
    """去掉母版里 baked 的高亮，得到中性基底。"""
    return nav.replace(" v5-nav__item--active", "")


def apply_active(nav: str, cap: str) -> str:
    """给 v5-nav__cap 文本 == cap 的那个 <a> 加上高亮 class。"""
    def repl(m):
        item = m.group(0)
        if f'>{cap}</span>' in item:
            return item.replace('class="v5-nav__item"', 'class="v5-nav__item v5-nav__item--active"', 1)
        return item
    return re.sub(r'<a\b[^>]*class="v5-nav__item[^"]*"[^>]*>.*?</a>', repl, nav, flags=re.S)


def expected_for(page: str, raw_master: str, base_nav: str) -> str:
    # 未配置任何高亮规则 → 逐字照搬母版（含母版自带的高亮）。
    if not DEFAULT_ACTIVE and not ACTIVE_MAP:
        return raw_master
    return apply_active(base_nav, ACTIVE_MAP.get(page, DEFAULT_ACTIVE))


def main():
    check = "--check" in sys.argv
    if not os.path.exists(MASTER):
        sys.exit(f"[sync-nav] 找不到母版 {MASTER}（请在原型目录运行）")
    raw_master = extract_master_nav(open(MASTER, encoding="utf-8").read())
    base_nav = strip_active(raw_master)

    drift, changed = [], []
    for page in sorted(glob.glob(PAGE_GLOB)):
        s = open(page, encoding="utf-8").read()
        m = NAV_RE.search(s)
        if not m:
            continue
        want = expected_for(page, raw_master, base_nav)
        if m.group(0) == want:
            continue
        drift.append(page)
        if not check:
            open(page, "w", encoding="utf-8").write(s[:m.start()] + want + s[m.end():])
            changed.append(page)

    if check:
        if drift:
            print("[sync-nav] 导航漂移，需回灌：")
            for p in drift:
                print("  - " + p)
            sys.exit(1)
        print("[sync-nav] 全部页面与母版一致 ✔")
        return
    if changed:
        print(f"[sync-nav] 已回灌 {len(changed)} 页：")
        for p in changed:
            print("  - " + p)
    else:
        print("[sync-nav] 无需改动，已全部一致 ✔")


if __name__ == "__main__":
    main()
