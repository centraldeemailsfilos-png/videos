#!/usr/bin/env bash
# Prepara (ou apenas verifica) o ambiente de edição deste repositório.
#
#   bash scripts/setup.sh           # instala o que faltar
#   bash scripts/setup.sh --check   # só verifica, não instala
#
# O container é efêmero: rode isto no início de cada sessão nova.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK_ONLY=0
[ "${1:-}" = "--check" ] && CHECK_ONLY=1

FAIL=0
ok()   { printf '  \033[32mOK\033[0m    %s\n' "$1"; }
warn() { printf '  \033[33mAVISO\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31mFALTA\033[0m %s\n' "$1"; FAIL=1; }

echo "== ambiente de edição =="

# --- 1. ffmpeg / ffprobe (obrigatório) ---
if command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null; then
  ok "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
else
  if [ "$CHECK_ONLY" = 1 ]; then
    bad "ffmpeg/ffprobe ausente"
  else
    echo "  instalando ffmpeg..."
    if command -v apt-get >/dev/null; then
      apt-get update -qq >/dev/null 2>&1
      DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/dev/null 2>&1
    elif command -v brew >/dev/null; then
      brew install ffmpeg
    elif command -v pacman >/dev/null; then
      pacman -S --noconfirm ffmpeg
    fi
    command -v ffmpeg >/dev/null && ok "ffmpeg instalado" || bad "não consegui instalar ffmpeg — instale manualmente (https://ffmpeg.org/download.html)"
  fi
fi

# --- 2. Python + deps do video-use (obrigatório) ---
if command -v python3 >/dev/null; then
  ok "python $(python3 --version 2>&1 | awk '{print $2}')"
else
  bad "python3 ausente"
fi

MISSING_PY="$(python3 - <<'PY' 2>/dev/null
import importlib.util as u
mods = {"requests":"requests","librosa":"librosa","matplotlib":"matplotlib","PIL":"pillow","numpy":"numpy"}
print(" ".join(p for m, p in mods.items() if u.find_spec(m) is None))
PY
)"

if [ -z "${MISSING_PY// /}" ]; then
  ok "deps python (requests, librosa, matplotlib, pillow, numpy)"
elif [ "$CHECK_ONLY" = 1 ]; then
  bad "deps python faltando: $MISSING_PY"
else
  echo "  instalando deps python: $MISSING_PY"
  if command -v uv >/dev/null; then
    uv pip install --system $MISSING_PY >/dev/null 2>&1 || pip install $MISSING_PY >/dev/null 2>&1
  else
    pip install $MISSING_PY >/dev/null 2>&1
  fi
  python3 -c "import requests, librosa, matplotlib, PIL, numpy" 2>/dev/null \
    && ok "deps python instaladas" || bad "falha ao instalar deps python"
fi

# --- 3. Node 22+ (necessário para HyperFrames) ---
if command -v node >/dev/null; then
  NODE_MAJOR="$(node --version | sed 's/^v\([0-9]*\).*/\1/')"
  if [ "$NODE_MAJOR" -ge 22 ] 2>/dev/null; then
    ok "node $(node --version) (HyperFrames exige 22+)"
  else
    warn "node $(node --version) — HyperFrames exige 22+; slots HyperFrames vão falhar"
  fi
else
  warn "node ausente — só necessário para slots HyperFrames/Remotion"
fi

# --- 4. ELEVENLABS_API_KEY (obrigatório para transcrever) ---
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  ok "ELEVENLABS_API_KEY (via ambiente)"
elif grep -q '^ELEVENLABS_API_KEY=..' "$REPO_ROOT/.env" 2>/dev/null; then
  ok "ELEVENLABS_API_KEY (via .env)"
else
  bad "ELEVENLABS_API_KEY ausente — copie .env.example para .env e cole a chave de https://elevenlabs.io/app/settings/api-keys"
fi

# --- 5. yt-dlp (opcional) ---
command -v yt-dlp >/dev/null && ok "yt-dlp (opcional)" || warn "yt-dlp ausente (opcional; só para baixar de URL)"

# --- 6. helpers do video-use respondem ---
H="$REPO_ROOT/.claude/skills/video-use/helpers"
if python3 "$H/timeline_view.py" --help >/dev/null 2>&1; then
  ok "helpers do video-use respondem"
else
  bad "helpers do video-use não rodam (deps python faltando?)"
fi

# --- 7. diretórios de trabalho ---
mkdir -p "$REPO_ROOT/footage" "$REPO_ROOT/edit"
ok "footage/ e edit/ prontos"

echo
if [ "$FAIL" = 0 ]; then
  echo "Tudo pronto. Coloque o material bruto em footage/ e diga o que você quer editar."
else
  echo "Resolva os itens marcados como FALTA antes de editar."
  exit 1
fi
