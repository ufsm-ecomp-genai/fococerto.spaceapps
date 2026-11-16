#!/usr/bin/env bash
# H-08: baixa os CSVs anuais do FIRMS (Brasil) e guarda só os focos dentro da bbox do Tocantins.
# bbox (config/regioes/tocantins.yaml): lat -13.0..-8.0, lon -49.5..-45.5
# Uso: baixar_firms_tocantins.sh <pasta_saida>
set -u
OUT="$1"; mkdir -p "$OUT"
BASE="https://firms.modaps.eosdis.nasa.gov/data/country"
filtrar() {  # stdin = CSV do país -> stdout = só linhas na bbox (mantém o cabeçalho)
  awk -F, 'NR==1{for(i=1;i<=NF;i++){if($i=="latitude")la=i;if($i=="longitude")lo=i}; print; next}
           $la>=-13.0 && $la<=-8.0 && $lo>=-49.5 && $lo<=-45.5'
}
baixar() {  # $1 = produto (modis | viirs-snpp), $2 = ano
  local dst="$OUT/${1}_${2}_tocantins.csv"
  [ -s "$dst" ] && { echo "ja existe: $dst"; return; }
  if curl -sfL -m 1800 "$BASE/$1/$2/${1}_${2}_Brazil.csv" | filtrar > "$dst.tmp" && [ "$(wc -l < "$dst.tmp")" -gt 1 ]; then
    mv "$dst.tmp" "$dst"; echo "ok $1 $2: $(($(wc -l < "$dst")-1)) focos"
  else
    rm -f "$dst.tmp"; echo "FALHOU $1 $2"
  fi
}
for ano in $(seq 2000 2026); do baixar modis "$ano"; done
for ano in $(seq 2012 2026); do baixar viirs-snpp "$ano"; done
echo FIM
