#!/usr/bin/env bash
# 把布局线框 HTML 渲染成低保真预览 PNG（Chrome headless，零安装）。
#
# 用法：
#   render-wireframe.sh <input.html> <output.png> [宽 高]
# 例：
#   render-wireframe.sh 页面-01-student-chat.wireframe.html 页面-01-student-chat.layout.png
#   render-wireframe.sh in.html out.png 1440 900
#
# 默认视口 1440x900、2x 高清。线框用 height:100vh，故视口截图即整页。
# 找不到 Chrome 时设环境变量 CHROME 指向可执行文件。

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "用法: $(basename "$0") <input.html> <output.png> [宽 高]" >&2
  exit 2
fi

IN="$1"; OUT="$2"; W="${3:-1440}"; H="${4:-900}"

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  CHROME="$(command -v google-chrome-stable || command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
fi
if [ -z "$CHROME" ] || [ ! -x "$CHROME" ]; then
  echo "未找到 Chrome/Chromium。请安装 Chrome，或设置环境变量 CHROME 指向可执行文件。" >&2
  exit 1
fi

if [ ! -f "$IN" ]; then
  echo "输入文件不存在: $IN" >&2
  exit 1
fi

# 转绝对路径供 file:// 使用
ABS_IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"

"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size="${W},${H}" \
  --screenshot="$OUT" "file://${ABS_IN}" 2>/dev/null

if [ -f "$OUT" ]; then
  echo "✓ 已渲染 $OUT (${W}x${H} @2x)"
else
  echo "渲染失败：未生成 $OUT" >&2
  exit 1
fi
