#!/bin/bash
cd -- "$(dirname -- "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3が必要です。python.orgからインストールしてください。'
else
  python3 update_frames.py
fi
read -r -p 'Enterで閉じる: '
