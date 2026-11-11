#!/bin/bash
# One-time setup per session: voice engine (VOICEVOX core + ずんだもん model) and Python packages.
# Needs: ffmpeg, rsvg-convert, the "Noto Sans CJK JP" font (check with: fc-list | grep "Noto Sans CJK").
set -euo pipefail
ZVV="${ZVV:-$HOME/zvv}"
mkdir -p "$ZVV" && cd "$ZVV"
B=https://github.com/VOICEVOX
WHL=voicevox_core-0.16.3-cp310-abi3-manylinux_2_34_x86_64.whl
[ -f "$WHL" ] || curl -sSfL -O "$B/voicevox_core/releases/download/0.16.3/$WHL"
[ -d voicevox_onnxruntime-linux-x64-1.17.3 ] || { curl -sSfL -o ort.tgz "$B/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.17.3/voicevox_onnxruntime-linux-x64-1.17.3.tgz"; tar xzf ort.tgz; }
[ -f 0.vvm ] || curl -sSfL -o 0.vvm "$B/voicevox_vvm/releases/download/0.16.3/0.vvm"
pip install --break-system-packages -q numpy soundfile pyopenjtalk "./$WHL"
python3 -c "import pyopenjtalk; pyopenjtalk.g2p('あ'); print('voice setup ok')"
