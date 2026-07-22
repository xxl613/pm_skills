#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""走查导航器注入 / 校验器（配合 _pagenav.js 引擎 + _pagenav.pages.js 数据）。

把两行脚本引用注入所有 `页面-*.html`（</body> 前，pages 在前、engine 在后），幂等。
并可在缺失时脚手架出 `_pagenav.pages.js`（按文件名分组的起始版，供人工改分组）。

用法（在项目原型目录运行）：
  python3 sync-pagenav.py            # 注入/补齐所有页面；缺 pages.js 则脚手架
  python3 sync-pagenav.py --check    # 只检测，有页面缺引用则退出码 1（CI/自检用）

约定：本目录同级需有 _pagenav.js（引擎，copy 自技能，勿改）。
"""
import os, re, sys, glob

ENGINE = '_pagenav.js'
PAGES = '_pagenav.pages.js'
# 规范块：数据在前、引擎在后（两个 defer 脚本按序执行，保证 GROUPS 先就位）
CANON = ('  <script defer src="%s"></script>\n  <script defer src="%s"></script>' % (PAGES, ENGINE))
# 匹配任意已存在的 pagenav 脚本标签（兼容 defer / defer="" 等格式化差异）
TAG_RE = re.compile(r'[ \t]*<script[^>]*\bsrc="_pagenav(?:\.pages)?\.js"[^>]*>\s*</script>[ \t]*\n?')
PAGE_GLOB = '页面-*.html'


def desired(s):
    """去掉页面里所有 pagenav 标签，再在 </body> 前插入规范块；返回目标文本（无 </body> 则原样返回）。"""
    stripped = TAG_RE.sub('', s)
    idx = stripped.rfind('</body>')
    if idx == -1:
        return None
    return stripped[:idx] + CANON + '\n' + stripped[idx:]


def find_pages():
    return sorted(f for f in glob.glob(PAGE_GLOB) if os.path.isfile(f))


def page_no(fn):
    m = re.search(r'(?:页面|page)[-_]([0-9a-zA-Z]+)[-_]', fn, re.I)
    return m.group(1) if m else ''


def clean_label(fn):
    s = re.sub(r'\.html$', '', fn)
    s = re.sub(r'^(?:页面|page)[-_][0-9a-zA-Z]+[-_]', '', s, flags=re.I)
    return s or fn


def scaffold_pages():
    """缺 _pagenav.pages.js 时，按文件名生成起始清单（单组，待人工重分组）。"""
    files = find_pages()
    lines = ["/* 走查导航清单 · 项目数据（脚手架，请按业务/Agent 关系重新分组）",
             " * 引擎见 _pagenav.js（勿改）。items: ['文件.html','短标题','编号(可选)'] */",
             "window.PGNAV_TITLE = '页面走查导航';",
             "window.PGNAV_GROUPS = [",
             "  { name: '全部页面', items: ["]
    for f in files:
        lbl = clean_label(f).replace("'", "\\'")
        fn = f.replace("'", "\\'")
        lines.append("    ['%s', '%s']," % (fn, lbl))
    lines += ["  ]},", "];", ""]
    with open(PAGES, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print('[pagenav] 已脚手架 %s（%d 页，单组，请重新按关系分组）' % (PAGES, len(files)))


def inject(check_only=False):
    pages = find_pages()
    if not pages:
        print('[pagenav] 当前目录没有 %s' % PAGE_GLOB, file=sys.stderr)
        return 2
    bad, fixed = [], []
    for f in pages:
        s = open(f, encoding='utf-8').read()
        want = desired(s)
        if want is None:
            print('[pagenav] %s 无 </body>，跳过' % f, file=sys.stderr)
            continue
        if want == s:
            continue  # 已是规范块（两标签、顺序正确），幂等跳过
        bad.append(f)
        if check_only:
            continue
        open(f, 'w', encoding='utf-8').write(want)
        fixed.append(f)

    if check_only:
        if bad:
            print('[pagenav] 走查导航引用缺失/不规范的页面 (%d)：' % len(bad))
            for f in bad:
                print('  -', f)
            return 1
        print('[pagenav] 全部 %d 页均已规范接入走查导航 ✔' % len(pages))
        return 0

    print('[pagenav] 处理 %d 页，规范化 %d 页' % (len(pages), len(fixed)))
    for f in fixed:
        print('  +', f)
    return 0


def main():
    check_only = '--check' in sys.argv[1:]
    if not os.path.isfile(ENGINE):
        print('[pagenav] 缺引擎 %s：请从技能 assets/project-profile/ copy 过来' % ENGINE,
              file=sys.stderr)
        return 1
    if not check_only and not os.path.isfile(PAGES):
        scaffold_pages()
    return inject(check_only=check_only)


if __name__ == '__main__':
    sys.exit(main())
