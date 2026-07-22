#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 desktop viewport-fit injector/checker.

Adds `_viewport-fit.js` to desktop `页面-*.html` files and removes it from
mobile `v5m-` pages. The script is idempotent and safe for file:// prototypes.
"""
import glob
import os
import re
import sys

ENGINE = '_viewport-fit.js'
PAGE_GLOB = '页面-*.html'
CANON = '  <script defer src="%s"></script>' % ENGINE
TAG_RE = re.compile(r'[ \t]*<script[^>]*\bsrc="_viewport-fit\.js"[^>]*>\s*</script>[ \t]*\n?')
MOBILE_RE = re.compile(r'data-v5-platform=["\']mobile["\']|\bv5m-', re.I)
PAGENAV_RE = re.compile(r'[ \t]*<script[^>]*\bsrc="_pagenav(?:\.pages)?\.js"', re.I)


def is_mobile(source):
    return bool(MOBILE_RE.search(source))


def desired(source):
    stripped = TAG_RE.sub('', source)
    if is_mobile(stripped):
        return stripped
    pagenav = PAGENAV_RE.search(stripped)
    if pagenav:
        return stripped[:pagenav.start()] + CANON + '\n' + stripped[pagenav.start():]
    closing = stripped.rfind('</body>')
    if closing == -1:
        return None
    return stripped[:closing] + CANON + '\n' + stripped[closing:]


def find_pages():
    return sorted(path for path in glob.glob(PAGE_GLOB) if os.path.isfile(path))


def sync(check_only=False):
    pages = find_pages()
    if not pages:
        print('[viewport-fit] 当前目录没有 %s' % PAGE_GLOB, file=sys.stderr)
        return 2
    changed = []
    for page in pages:
        with open(page, encoding='utf-8') as handle:
            source = handle.read()
        target = desired(source)
        if target is None:
            print('[viewport-fit] %s 无 </body>，跳过' % page, file=sys.stderr)
            continue
        if target == source:
            continue
        changed.append(page)
        if not check_only:
            with open(page, 'w', encoding='utf-8') as handle:
                handle.write(target)

    if check_only:
        if changed:
            print('[viewport-fit] 桌面适配引用缺失或移动页误引用 (%d)：' % len(changed))
            for page in changed:
                print('  -', page)
            return 1
        print('[viewport-fit] 全部 %d 页的平台引用正确 ✔' % len(pages))
        return 0

    print('[viewport-fit] 处理 %d 页，规范化 %d 页' % (len(pages), len(changed)))
    for page in changed:
        print('  +', page)
    return 0


def main():
    if not os.path.isfile(ENGINE):
        print('[viewport-fit] 缺引擎 %s：请从技能 assets/project-profile/ copy 过来' % ENGINE, file=sys.stderr)
        return 1
    return sync(check_only='--check' in sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())
