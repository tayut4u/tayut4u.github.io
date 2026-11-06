#!/bin/bash
cd -- "$(dirname -- "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1 || ! python3 -c 'import sys; assert sys.version_info >= (3,9)' 2>/dev/null; then
  echo 'Python 3.9以降が必要です。python.orgからPython 3をインストールしてください。'
  read -r -p 'Enterで閉じる: '
  exit 1
fi
python3 serve_local.py
read -r -p 'Enterで閉じる: '
