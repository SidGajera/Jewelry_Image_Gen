#!/usr/bin/env bash
# MANDATORY FINAL STAGE for studio images: composite the preserved official logo
# onto every AI render (clean cloth) so the delivered image already includes the
# correctly printed logo. The AI never renders the logo; this stamps it.
#
# Usage:
#   bash scripts/finalize_studio.sh <renders_dir> [out_dir]
# Produces <out_dir>/PRINTED_<name> for each render (default out_dir=<renders_dir>/final).
set -euo pipefail
IN="${1:?usage: finalize_studio.sh <renders_dir> [out_dir]}"
OUT="${2:-$IN/final}"
LOGO="assets/logo/logo_official_transparent.png"
mkdir -p "$OUT"
shopt -s nullglob nocaseglob
n=0
for f in "$IN"/*.png "$IN"/*.jpg "$IN"/*.jpeg; do
  base="$(basename "$f")"
  python3 scripts/print_logo_on_cloth.py --image "$f" --logo "$LOGO" \
     --scale 0.42 --pos lower-right --opacity 0.9 --displace 6 \
     --out "$OUT/PRINTED_$base"
  n=$((n+1))
done
echo "finalized $n studio image(s) with official logo -> $OUT"
