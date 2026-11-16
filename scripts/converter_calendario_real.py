"""Converte a série real do NASA FIRMS (calendario_semanal.csv) em dados_calendario.json.

Gera o JSON oficial para o componente React FireCalendar.jsx, com:
- Anos 2000 a 2026 (27 anos)
- Matriz mensal (324 períodos) e matriz semanal (1404 períodos)
- Séries na escala MODIS-equivalente (eliminando o degrau de 2012)
- Picos históricos reais de 2007 e 2010 do Tocantins
- 2026 marcado como SEM_DADOS para períodos futuros
"""
from __future__ import annotations

import csv
import json
import math
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV_SEMANAL = RAIZ / "tasks" / "humanas" / "entregas" / "H-08-firms" / "resultados" / "calendario_semanal.csv"
JSON_SAIDA = RAIZ / "web" / "app" / "src" / "assets" / "dados_calendario.json"

MESES_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def mes_da_semana(ano: int, semana: int) -> int:
    try:
        return date.fromisocalendar(ano, semana, 4).month
    except ValueError:
        return min(12, max(1, (semana - 1) // 4 + 1))


def mad(vals: list[float], med: float) -> float:
    return statistics.median([abs(v - med) for v in vals]) if vals else 0.0


def percentil(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    pos = (p / 100.0) * (len(s) - 1)
    i = int(pos)
    return s[i] if i + 1 >= len(s) else s[i] + (s[i + 1] - s[i]) * (pos - i)


def classificar(z: float, v: float, q95: float, q90: float) -> str:
    if z >= 2.0 or v > q95:
        return "CRITICO"
    if z >= 1.0 or v > q90:
        return "ATENCAO"
    return "NORMAL"


def texto_alerta(status: str, desvio: float | None, z: float) -> str:
    if status == "CRITICO":
        d_txt = f"+{desvio:.0f}%" if desvio is not None and desvio >= 0 else f"{desvio:.0f}%"
        return f"Extreme thermal anomaly: {d_txt} vs 25-year historical median (Z={z:.2f})"
    if status == "ATENCAO":
        d_txt = f"+{desvio:.0f}%" if desvio is not None and desvio >= 0 else f"{desvio:.0f}%"
        return f"Elevated fire activity: {d_txt} above historical median (Z={z:.2f})"
    return ""


def main() -> None:
    with open(CSV_SEMANAL, mode="r", encoding="utf-8") as f:
        linhas_csv = list(csv.DictReader(f))

    # Indexa dados brutos por (ano, semana)
    dados_semanais: dict[tuple[int, int], dict] = {}
    for row in linhas_csv:
        ano = int(row["ano"])
        sem = int(row["semana"])
        n_m = int(row["n_modis"])
        n_v = int(row["n_viirs"])
        frp_m = float(row["frp_modis_mw"])
        frp_v = float(row["frp_viirs_mw"])
        modis_eq = float(row["modis_equivalente"])
        dados_semanais[(ano, sem)] = {
            "n_modis": n_m,
            "n_viirs": n_v,
            "frp_total": round(frp_m + frp_v, 1),
            "modis_eq": modis_eq,
        }

    # Calcula linha de base semanal (2001-2025)
    base_semanal: dict[int, dict] = {}
    for sem in range(1, 53):
        vals = [dados_semanais[(a, sem)]["modis_eq"] for a in range(2001, 2026) if (a, sem) in dados_semanais]
        med = statistics.median(vals)
        d_mad = mad(vals, med)
        base_semanal[sem] = {
            "mediana": round(med, 2),
            "mad": d_mad,
            "sigma": max(1.0, 1.4826 * d_mad),
            "p90": round(percentil(vals, 90.0), 2),
            "p95": round(percentil(vals, 95.0), 2),
        }

    # Agrupa por mês para construir dados mensais
    dados_mensais: dict[tuple[int, int], dict] = {}
    for ano in range(2000, 2026):
        for mes in range(1, 13):
            dados_mensais[(ano, mes)] = {
                "n_modis": 0,
                "n_viirs": 0,
                "frp_total": 0.0,
                "modis_eq": 0.0,
            }

    for (ano, sem), d in dados_semanais.items():
        m = mes_da_semana(ano, sem)
        bloco = dados_mensais[(ano, m)]
        bloco["n_modis"] += d["n_modis"]
        bloco["n_viirs"] += d["n_viirs"]
        bloco["frp_total"] += d["frp_total"]
        bloco["modis_eq"] += d["modis_eq"]

    # Calcula linha de base mensal (2001-2025)
    base_mensal: dict[int, dict] = {}
    for mes in range(1, 13):
        vals = [dados_mensais[(a, mes)]["modis_eq"] for a in range(2001, 2026) if (a, mes) in dados_mensais]
        med = statistics.median(vals)
        d_mad = mad(vals, med)
        base_mensal[mes] = {
            "mediana": round(med, 2),
            "mad": d_mad,
            "sigma": max(1.0, 1.4826 * d_mad),
            "p90": round(percentil(vals, 90.0), 2),
            "p95": round(percentil(vals, 95.0), 2),
        }

    # Constrói matriz mensal (324 períodos)
    matriz_mensal = []
    resumo_mensal = {"NORMAL": 0, "ATENCAO": 0, "CRITICO": 0, "SEM_DADOS": 0}

    for ano in range(2000, 2027):
        for mes in range(1, 13):
            rotulo = f"{MESES_EN[mes - 1]} {ano}"
            b = base_mensal[mes]
            if ano <= 2025:
                d = dados_mensais[(ano, mes)]
                val = round(d["modis_eq"], 1)
                med = b["mediana"]
                z = round((val - med) / b["sigma"], 2)
                desvio = round(((val - med) / med) * 100.0, 1) if med > 0 else 0.0
                st = classificar(z, val, b["p95"], b["p90"])
                al = texto_alerta(st, desvio, z)
                resumo_mensal[st] += 1
                matriz_mensal.append({
                    "ano": ano,
                    "mes": mes,
                    "semana": None,
                    "rotulo": rotulo,
                    "focos_harmonizados": val,
                    "focos_modis_bruto": d["n_modis"],
                    "focos_viirs_bruto": d["n_viirs"],
                    "frp_total_mw": round(d["frp_total"], 1),
                    "mediana_historica": med,
                    "p90": b["p90"],
                    "p95": b["p95"],
                    "desvio_percentual": desvio,
                    "z_score": z,
                    "status": st,
                    "alerta": al,
                })
            else:
                # 2026: períodos sem dados de observação final
                resumo_mensal["SEM_DADOS"] += 1
                matriz_mensal.append({
                    "ano": ano,
                    "mes": mes,
                    "semana": None,
                    "rotulo": rotulo,
                    "focos_harmonizados": None,
                    "focos_modis_bruto": 0,
                    "focos_viirs_bruto": 0,
                    "frp_total_mw": 0.0,
                    "mediana_historica": b["mediana"],
                    "p90": b["p90"],
                    "p95": b["p95"],
                    "desvio_percentual": None,
                    "z_score": None,
                    "status": "SEM_DADOS",
                    "alerta": "",
                })

    # Constrói matriz semanal (1404 períodos)
    matriz_semanal = []
    resumo_semanal = {"NORMAL": 0, "ATENCAO": 0, "CRITICO": 0, "SEM_DADOS": 0}

    for ano in range(2000, 2027):
        for sem in range(1, 53):
            rotulo = f"W{sem:02d} {ano}"
            m = mes_da_semana(ano, sem)
            b = base_semanal[sem]
            if ano <= 2025:
                d = dados_semanais[(ano, sem)]
                val = round(d["modis_eq"], 1)
                med = b["mediana"]
                z = round((val - med) / b["sigma"], 2)
                desvio = round(((val - med) / med) * 100.0, 1) if med > 0 else 0.0
                st = classificar(z, val, b["p95"], b["p90"])
                al = texto_alerta(st, desvio, z)
                resumo_semanal[st] += 1
                matriz_semanal.append({
                    "ano": ano,
                    "mes": m,
                    "semana": sem,
                    "rotulo": rotulo,
                    "focos_harmonizados": val,
                    "focos_modis_bruto": d["n_modis"],
                    "focos_viirs_bruto": d["n_viirs"],
                    "frp_total_mw": d["frp_total"],
                    "mediana_historica": med,
                    "p90": b["p90"],
                    "p95": b["p95"],
                    "desvio_percentual": desvio,
                    "z_score": z,
                    "status": st,
                    "alerta": al,
                })
            else:
                # 2026: sem dados
                resumo_semanal["SEM_DADOS"] += 1
                matriz_semanal.append({
                    "ano": ano,
                    "mes": m,
                    "semana": sem,
                    "rotulo": rotulo,
                    "focos_harmonizados": None,
                    "focos_modis_bruto": 0,
                    "focos_viirs_bruto": 0,
                    "frp_total_mw": 0.0,
                    "mediana_historica": b["mediana"],
                    "p90": b["p90"],
                    "p95": b["p95"],
                    "desvio_percentual": None,
                    "z_score": None,
                    "status": "SEM_DADOS",
                    "alerta": "",
                })

    saida = {
        "regiao": "tocantins",
        "nome_exibicao": "Tocantins / Cerrado",
        "periodo": "mes",
        "ano_inicio": 2000,
        "ano_fim": 2026,
        "anos_base": [2001, 2025],
        "data_corte": "2026-11-15",
        "beta_viirs": 0.3,
        "ano_inicio_viirs": 2012,
        "gerado_em_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "resumo_status": resumo_mensal,
        "total_periodos": len(matriz_mensal),
        "matriz": matriz_mensal,
        "amostra": True,
        "fonte_dados": (
            "NASA FIRMS (MODIS Collection 6.1 and VIIRS 375m S-NPP archive 2000-2025 for Tocantins; "
            "611,797 MODIS and 1,328,777 VIIRS detections). Calibrated MODIS-equivalent series (k=0.252)."
        ),
        "matriz_semanal": matriz_semanal,
        "resumo_status_semanal": resumo_semanal,
    }

    JSON_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_SAIDA, "w", encoding="utf-8") as f:
        json.dump(saida, f, separators=(",", ":"), ensure_ascii=False)

    print(f"JSON oficial gerado com sucesso em {JSON_SAIDA}")
    print(f"Total mensal: {len(matriz_mensal)} células | Total semanal: {len(matriz_semanal)} células")
    print(f"Status mensal: {resumo_mensal}")
    print(f"Status semanal: {resumo_semanal}")


if __name__ == "__main__":
    main()
