#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-design.py — DESIGN.md ⟷ theme.css 一致性校验（项目级工具）
============================================================
让 UI 设计语言（DESIGN.md）与其 CSS 实现（theme.css）共同服务、互不漂移。
约定：DESIGN.md 的「## 9. 令牌契约」里有一个 ```css :root{…}``` 块，是机器源；
它应与 theme.css 的 :root 覆盖逐条一致。tokens.css = V5 base（参考，不校验值）。

校验三类问题（任一存在则 --check 退出码 1）：
  ① 漏实现：契约里有、theme.css 没有的令牌
  ② 野令牌：theme.css 覆盖了、契约里没登记的令牌（未文档化）
  ③ 值漂移：两边都有但值不一致
另：契约/theme 新增了 base 没有的令牌 → 提示（允许，属扩展）。
     DESIGN.md 正文引用了 base/theme/契约都没有的 --v5-* → 警告（疑似坏引用）。

用法（在原型目录运行）：
  python3 check-design.py            # 校验并打印报告
  python3 check-design.py --check    # 同上；有①②③则退出码 1
============================================================
"""
import re, sys, os

DESIGN = "DESIGN.md"
THEME = "theme.css"
BASE = "tokens.css"

DECL_RE = re.compile(r'(--v5-[A-Za-z0-9-]+)\s*:\s*([^;}\n]+?)\s*(?:;|\n|})')


def strip_comments(text: str) -> str:
    # 先去 CSS 注释（含跨行 /* */ 与 // 行注释），避免示例/说明被当成真令牌
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'//.*', '', text)
    return text


def _norm(v: str) -> str:
    return re.sub(r'\s+', ' ', v).strip().lower()


def decls(text: str) -> dict:
    text = strip_comments(text)
    return {m.group(1): _norm(m.group(2)) for m in DECL_RE.finditer(text)}


def contract_block(md: str) -> str:
    """取 DESIGN.md 里『令牌契约』下的第一个 ```css fenced 块。"""
    m = re.search(r'令牌契约.*?```css(.*?)```', md, re.S)
    if m:
        return m.group(1)
    # 兜底：任意 ```css 块
    m = re.search(r'```css(.*?)```', md, re.S)
    return m.group(1) if m else ""


def main():
    check = "--check" in sys.argv
    for fn in (DESIGN, THEME):
        if not os.path.exists(fn):
            sys.exit(f"[check-design] 缺少 {fn}（请在原型目录运行）")
    md = open(DESIGN, encoding="utf-8").read()
    contract = decls(contract_block(md))
    theme = decls(open(THEME, encoding="utf-8").read())
    base = decls(open(BASE, encoding="utf-8").read()) if os.path.exists(BASE) else {}

    missing = [k for k in contract if k not in theme]                 # ① 漏实现
    wild = [k for k in theme if k not in contract]                    # ② 野令牌
    drift = [k for k in contract if k in theme and contract[k] != theme[k]]  # ③ 值漂移
    extend = [k for k in contract if k not in base]                  # 扩展（提示）

    # 坏引用：正文（去掉契约块后）提到的 --v5-* 不在 base∪theme∪contract
    known = set(base) | set(theme) | set(contract)
    prose = re.sub(r'```css.*?```', '', md, flags=re.S)
    referenced = set(re.findall(r'--v5-[A-Za-z0-9-]+', prose))
    bad_ref = sorted(r for r in referenced if r not in known)

    err = bool(missing or wild or drift)
    print("=== check-design：DESIGN.md ⟷ theme.css ===")
    print(f"契约令牌 {len(contract)} · theme 覆盖 {len(theme)} · base {len(base)}")
    if missing: print("① 漏实现（契约有、theme 无）：" + ", ".join(missing))
    if wild:    print("② 野令牌（theme 有、契约未登记）：" + ", ".join(wild))
    if drift:
        print("③ 值漂移：")
        for k in drift: print(f"    {k}: 契约={contract[k]!r} ≠ theme={theme[k]!r}")
    if extend:  print("· 扩展令牌（base 无，属新增，正常）：" + ", ".join(extend))
    if bad_ref: print("⚠ 疑似坏引用（正文提到但无定义）：" + ", ".join(bad_ref))
    if not err:
        print("✔ 契约与 theme.css 逐条一致" + ("（均空 = 沿用 V5 base）" if not contract and not theme else ""))

    if check and err:
        sys.exit(1)


if __name__ == "__main__":
    main()
