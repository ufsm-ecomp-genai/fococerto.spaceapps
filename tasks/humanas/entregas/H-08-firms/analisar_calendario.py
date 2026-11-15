"""H-08: calendário de atividade de fogo do Tocantins com o arquivo real do NASA FIRMS (2000–2026).

Só usa a biblioteca padrão. Entrada: os CSVs anuais do FIRMS (Brasil) já recortados para a bbox do Tocantins
(lat -13..-8, lon -49.5..-45.5), um por produto e ano: modis_<ano>_tocantins.csv e viirs-snpp_<ano>_tocantins.csv.

Calcula duas séries semanais:
  1. "formula_projeto": N = N_MODIS + 0.30 * N_VIIRS (fórmula do CLAUDE.md, aplicada a partir de 2012).
  2. "modis_equivalente": MODIS puro onde só há MODIS; a partir de 2012, a média entre N_MODIS e k * N_VIIRS,
     com k = soma(N_MODIS) / soma(N_VIIRS) no período de sobreposição. Fica na escala MODIS do começo ao fim.
E, para cada uma, a linha de base por semana do ano (mediana e MAD de 2001–2025), o Z robusto e o P95.

Uso: python -I analisar_calendario.py <pasta_csvs> <pasta_saida>
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ANO_BASE_INI, ANO_BASE_FIM = 2001, 2025  # 2000 fica de fora: o arquivo do FIRMS começa em nov/2000
FATOR_VIIRS = 0.30


def semana_do_ano(d: date) -> int:
    return min(52, (d.timetuple().tm_yday - 1) // 7 + 1)


def ler(pasta: Path, prefixo: str) -> dict[tuple[int, int], dict[str, float]]:
    """(ano, semana) -> {n, frp}. Só detecções de vegetação (type 0) quando a coluna existe."""
    agg: dict[tuple[int, int], dict[str, float]] = defaultdict(lambda: {"n": 0, "frp": 0.0})
    for arq in sorted(pasta.glob(f"{prefixo}_*_tocantins.csv")):
        with arq.open(newline="", encoding="utf-8") as f:
            for lin in csv.DictReader(f):
                if lin.get("type", "0") not in ("0", ""):
                    continue
                d = date.fromisoformat(lin["acq_date"])
                b = agg[(d.year, semana_do_ano(d))]
                b["n"] += 1
                b["frp"] += float(lin["frp"] or 0)
    return agg


def mad(vals: list[float], med: float) -> float:
    return statistics.median([abs(v - med) for v in vals])


def p95(vals: list[float]) -> float:
    s = sorted(vals)
    pos = 0.95 * (len(s) - 1)
    i = int(pos)
    return s[i] if i + 1 >= len(s) else s[i] + (s[i + 1] - s[i]) * (pos - i)


def main(pasta_in: Path, pasta_out: Path) -> None:
    pasta_out.mkdir(parents=True, exist_ok=True)
    modis, viirs = ler(pasta_in, "modis"), ler(pasta_in, "viirs-snpp")
    anos = sorted({a for a, _ in modis} | {a for a, _ in viirs})

    # k: quantos focos MODIS "vale" um foco VIIRS, medido na sobreposição (anos completos com os dois sensores)
    anos_sobrep = [a for a in anos if 2012 <= a <= 2025 and any(k[0] == a for k in viirs)]
    soma_m = sum(v["n"] for (a, _), v in modis.items() if a in anos_sobrep)
    soma_v = sum(v["n"] for (a, _), v in viirs.items() if a in anos_sobrep)
    k = soma_m / soma_v if soma_v else float("nan")

    linhas = []
    for a in anos:
        for w in range(1, 53):
            m, v = modis.get((a, w), {"n": 0, "frp": 0.0}), viirs.get((a, w), {"n": 0, "frp": 0.0})
            tem_viirs = a >= 2012 and (a, w) in viirs
            linhas.append({
                "ano": a, "semana": w, "n_modis": m["n"], "n_viirs": v["n"],
                "frp_modis_mw": round(m["frp"], 1), "frp_viirs_mw": round(v["frp"], 1),
                "formula_projeto": m["n"] + (FATOR_VIIRS * v["n"] if a >= 2012 else 0),
                "modis_equivalente": (m["n"] + k * v["n"]) / 2 if tem_viirs else m["n"],
            })

    # linha de base por semana do ano e anomalia, para as duas séries
    for serie in ("formula_projeto", "modis_equivalente"):
        por_semana: dict[int, list[float]] = defaultdict(list)
        for l in linhas:
            if ANO_BASE_INI <= l["ano"] <= ANO_BASE_FIM:
                por_semana[l["semana"]].append(l[serie])
        base = {}
        for w, vals in por_semana.items():
            med = statistics.median(vals)
            base[w] = (med, mad(vals, med), p95(vals))
        for l in linhas:
            med, dv, q95 = base[l["semana"]]
            sigma = max(1.0, 1.4826 * dv)
            z = (l[serie] - med) / sigma
            l[f"{serie}_mediana"] = round(med, 1)
            l[f"{serie}_z"] = round(z, 2)
            l[f"{serie}_critico"] = int(z >= 2.0 or l[serie] > q95)

    with (pasta_out / "calendario_semanal.csv").open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(linhas[0]))
        wr.writeheader()
        wr.writerows(linhas)

    # resumo anual
    anual = []
    for a in anos:
        ls = [l for l in linhas if l["ano"] == a]
        anual.append({
            "ano": a,
            "n_modis": sum(l["n_modis"] for l in ls),
            "n_viirs": sum(l["n_viirs"] for l in ls),
            "razao_viirs_modis": round(sum(l["n_viirs"] for l in ls) / max(1, sum(l["n_modis"] for l in ls)), 2),
            "formula_projeto": round(sum(l["formula_projeto"] for l in ls)),
            "modis_equivalente": round(sum(l["modis_equivalente"] for l in ls)),
            "semanas_criticas_formula": sum(l["formula_projeto_critico"] for l in ls),
            "semanas_criticas_modis_eq": sum(l["modis_equivalente_critico"] for l in ls),
        })
    with (pasta_out / "resumo_anual.csv").open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(anual[0]))
        wr.writeheader()
        wr.writerows(anual)

    def media(serie: str, a0: int, a1: int) -> float:
        xs = [r[serie] for r in anual if a0 <= r["ano"] <= a1]
        return round(statistics.mean(xs)) if xs else 0

    top = sorted(linhas, key=lambda l: -l["modis_equivalente_z"])[:10]
    resumo = {
        "k_modis_por_viirs": round(k, 3),
        "anos_sobreposicao": anos_sobrep,
        "total_focos_modis": sum(r["n_modis"] for r in anual),
        "total_focos_viirs": sum(r["n_viirs"] for r in anual),
        "degrau_2012": {
            "media_anual_2003_2011_formula": media("formula_projeto", 2003, 2011),
            "media_anual_2013_2021_formula": media("formula_projeto", 2013, 2021),
            "media_anual_2003_2011_modis_eq": media("modis_equivalente", 2003, 2011),
            "media_anual_2013_2021_modis_eq": media("modis_equivalente", 2013, 2021),
        },
        "top10_semanas_modis_equivalente": [
            {k2: l[k2] for k2 in ("ano", "semana", "n_modis", "n_viirs", "modis_equivalente",
                                  "modis_equivalente_mediana", "modis_equivalente_z")} for l in top],
    }
    (pasta_out / "resumo.json").write_text(json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(resumo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
