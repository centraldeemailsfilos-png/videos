#!/usr/bin/env bash
# Cria o projeto HyperFrames de uma cena com o kit ja dentro.
set -euo pipefail
N="$1"; D="edit/rede/animations/cena_$N"
[ -d "$D" ] && { echo "$D ja existe"; exit 0; }
mkdir -p "$D"
( cd "$D" && npx --yes hyperframes init . --example blank --non-interactive --skip-skills >/dev/null 2>&1 \
  && npm install --no-audit --no-fund gsap@3.14.2 >/dev/null 2>&1 )
mkdir -p "$D/assets"
cp edit/rede/animations/_kit/estilo.css edit/rede/animations/_kit/kit.js "$D/assets/"
shift
for g in "$@"; do cp "edit/rede/gravacoes/$g.mp4" "$D/assets/"; done
echo "$D pronto  (gravacoes: $*)"
