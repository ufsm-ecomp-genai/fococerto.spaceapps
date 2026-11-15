"""Comandos de harmonização MODIS/VIIRS e Fire Activity Calendar da CLI (task A-07).

    python3 -m app.cli --sample --harmonizar
    python3 -m app.cli --sample --calendario [--regiao tocantins] [--json-saida caminho.json]
    python3 -m app.cli calendario --sample [--harmonizar] ...   (forma com subcomando)

Só usa a biblioteca padrão (app.data.harmonizacao e app.data.calendario), para rodar mesmo num python3
sem as dependências do motor de despacho (pydantic, langgraph...). A saída é em inglês (jurados).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from app.data.calendario import construir_matriz_temporal, exportar_calendario_json
from app.data.harmonizacao import (
    FATOR_ESCALA_VIIRS_MODIS,
    carregar_e_padronizar_focos,
    harmonizar_series,
)

RAIZ = Path(__file__).resolve().parent.parent
PASTA_AMOSTRAS = RAIZ / "data" / "samples_firms"
MODIS_CSV = PASTA_AMOSTRAS / "modis_sample_c6.csv"
VIIRS_CSV = PASTA_AMOSTRAS / "viirs_sample_375m.csv"

FLAGS = ("--calendario", "--harmonizar")
SUBCOMANDOS = ("calendario", "harmonizar")
REGIOES = {"tocantins": "Tocantins / Cerrado"}
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MESES_LONGOS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                "October", "November", "December"]
LARGURA = 96
STATUS_EN = {"CRITICO": "CRITICAL", "ATENCAO": "ELEVATED", "NORMAL": "NORMAL"}

AVISO_LINHA_BASE = (
    "NOTICE: the multi-decadal baseline (2000-2026) is SYNTHETIC / ILLUSTRATIVE. Weeks without input data use\n"
    "        a calibrated seasonal curve for the Cerrado (estimar_linha_base_sazonal_cerrado) and a reconstructed\n"
    "        series with fixed per-year multipliers. Only the cells marked '*' come from the small NASA\n"
    "        FIRMS-format sample in data/samples_firms/ (Sep 2024: {n_modis} MODIS + {n_viirs} VIIRS detections).\n"
    "        Do not read these numbers as observed historical statistics."
)


def deve_tratar(argv: list[str]) -> bool:
    """True quando a linha de comando é deste módulo (flags --calendario/--harmonizar ou subcomando)."""
    if not argv:
        return False
    if argv[0] in SUBCOMANDOS:
        return True
    return argv[0].startswith("-") and any(f in argv for f in FLAGS)


def montar_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python3 -m app.cli",
        description="FocoCerto Harmonizer: MODIS/VIIRS harmonization and Fire Activity Calendar.")
    p.add_argument("--sample", action="store_true",
                   help="offline mode using data/samples_firms/ (the only mode available for these commands)")
    p.add_argument("--calendario", action="store_true", help="print the year x month Fire Activity Calendar")
    p.add_argument("--harmonizar", action="store_true", help="print MODIS/VIIRS harmonization statistics")
    p.add_argument("--regiao", default="tocantins", help="area of interest (sample: tocantins)")
    p.add_argument("--ano-inicio", type=int, default=2000)
    p.add_argument("--ano-fim", type=int, default=2026)
    p.add_argument("--modis-csv", default=str(MODIS_CSV), help=argparse.SUPPRESS)
    p.add_argument("--viirs-csv", default=str(VIIRS_CSV), help=argparse.SUPPRESS)
    p.add_argument("--json-saida", default=None,
                   help="also write the calendar JSON (same schema as web/app/src/assets/dados_calendario.json)")
    return p


def carregar_e_harmonizar(args) -> tuple[list, list, list]:
    modis = carregar_e_padronizar_focos(args.modis_csv, sensor="MODIS")
    viirs = carregar_e_padronizar_focos(args.viirs_csv, sensor="VIIRS")
    return modis, viirs, harmonizar_series(modis, viirs, step=0.1)


def estatisticas(modis: list, viirs: list, harm: list) -> dict:
    n_modis, n_viirs = len(modis), len(viirs)
    frp_modis = round(sum(f["frp_mw"] for f in modis), 2)
    frp_viirs = round(sum(f["frp_mw"] for f in viirs), 2)
    datas = sorted({f["data"] for f in modis + viirs})
    return {
        "n_modis": n_modis,
        "n_viirs": n_viirs,
        "n_harmonizado": round(sum(r["focos_harmonizados"] for r in harm), 2),
        "n_harmonizado_formula": round(n_modis + FATOR_ESCALA_VIIRS_MODIS * n_viirs, 2),
        "n_bruto_somado": n_modis + n_viirs,
        "frp_modis": frp_modis,
        "frp_viirs": frp_viirs,
        "frp_harmonizado": round(sum(r["frp_harmonizado_mw"] for r in harm), 2),
        "celulas": len({(r["celula_lat"], r["celula_lon"]) for r in harm}),
        "grupos": len(harm),
        "datas": (datas[0], datas[-1]) if datas else ("-", "-"),
        "satelites": sorted({f["satelite"] for f in modis + viirs}),
    }


def imprimir_harmonizacao(e: dict, args) -> None:
    print("=" * LARGURA)
    print("   FOCOCERTO HARMONIZER - MODIS (1 km) + VIIRS (375 m) HARMONIZATION")
    print(f"   Input: {Path(args.modis_csv).name} + {Path(args.viirs_csv).name} "
          f"({e['datas'][0]} to {e['datas'][1]})")
    print("=" * LARGURA)
    print(f"Satellites                       : {', '.join(e['satelites'])}")
    print(f"MODIS detections (N_MODIS)       : {e['n_modis']}")
    print(f"VIIRS detections (N_VIIRS)       : {e['n_viirs']}")
    print(f"Naive raw sum (NOT used)         : {e['n_bruto_somado']}  (double counts the same fires)")
    print(f"Harmonized count N_harm          : {e['n_harmonizado']:.2f}  "
          f"(= N_MODIS + {FATOR_ESCALA_VIIRS_MODIS:.2f} x N_VIIRS = {e['n_harmonizado_formula']:.2f})")
    print(f"FRP MODIS                        : {e['frp_modis']:,.2f} MW")
    print(f"FRP VIIRS                        : {e['frp_viirs']:,.2f} MW")
    print(f"FRP harmonized (sum)             : {e['frp_harmonizado']:,.2f} MW")
    print(f"0.1 deg grid cells with fire     : {e['celulas']}  ({e['grupos']} cell x week groups)")
    print("-" * LARGURA)
    print("Method: 0.1 x 0.1 deg grid; for t >= 2012, FRP_harm = sum FRP_MODIS + sum FRP_VIIRS and")
    print(f"        N_harm = N_MODIS + {FATOR_ESCALA_VIIRS_MODIS:.2f} * N_VIIRS (pre-2012: MODIS only).")
    print("Data: small NASA FIRMS-format sample in data/samples_firms/ (not a full archive download).")
    print("=" * LARGURA)


def simbolo(celula: dict) -> str:
    if celula["status"] == "CRITICO":
        return "!"
    if celula["status"] == "ATENCAO":
        return "X"
    if celula["desvio_percentual"] > 0:
        return "o"
    return "."


def cenario_exemplo(regiao: str) -> str:
    """Primeiro cenarios/<regiao>-*.yaml em ordem alfabética (o mesmo critério do ``run`` sem --recursos)."""
    candidatos = sorted((RAIZ / "cenarios").glob(f"{regiao}-*.yaml"))
    return candidatos[0].stem if candidatos else f"{regiao}-<scenario>"


def imprimir_calendario(cal: dict, harm: list, e: dict) -> None:
    reais = {(r["ano"], r["semana"]) for r in harm}
    por_ano: dict[int, dict[int, dict]] = {}
    for c in cal["matriz"]:
        por_ano.setdefault(c["ano"], {})[c["mes"]] = c

    print("=" * LARGURA)
    print("   FOCOCERTO HARMONIZER - FIRE ACTIVITY CALENDAR (MODIS + VIIRS, harmonized)")
    print(f"   Area of Interest: {cal['nome_exibicao']} ({cal['ano_inicio']} - {cal['ano_fim']})")
    print("=" * LARGURA)
    print("Year | " + " ".join(f"{m:<4}" for m in MESES) + "| Sum FRP (12 ref. weeks)")
    for ano in sorted(por_ano, reverse=True):
        celulas = []
        for mes in range(1, 13):
            c = por_ano[ano].get(mes)
            if c is None:
                celulas.append("    ")
                continue
            s = simbolo(c)
            txt = f"[{s}]" if s == "!" else f" {s} "
            txt += "*" if (ano, c["semana"]) in reais else " "
            celulas.append(txt)
        frp = sum(c["frp_total_mw"] for c in por_ano[ano].values())
        print(f"{ano} | " + " ".join(celulas) + f"| {frp:>12,.0f} MW")
    print("-" * LARGURA)
    print("Legend: [.] at/below weekly median  [o] above median  [X] Elevated (Z>=1 or >=P90)")
    print("        [!] Critical anomaly (Z>=2 or >=P95)  * cell computed from the FIRMS sample (rest: synthetic)")
    print("=" * LARGURA)

    pior = max(cal["matriz"], key=lambda c: (c["z_score"], c["desvio_percentual"]))
    sinal = "+" if pior["desvio_percentual"] >= 0 else ""
    print(f"Status: most anomalous month is {MESES_LONGOS[pior['mes'] - 1]} {pior['ano']} "
          f"({sinal}{pior['desvio_percentual']}% vs weekly median, Z={pior['z_score']:.2f}, {STATUS_EN.get(pior['status'], pior['status'])}).")
    n_crit = sum(1 for c in cal["matriz"] if c["status"] == "CRITICO")
    n_aten = sum(1 for c in cal["matriz"] if c["status"] == "ATENCAO")
    print(f"        {n_crit} critical and {n_aten} elevated month(s) out of {len(cal['matriz'])}.")
    for c in cal["matriz"]:
        if (c["ano"], c["semana"]) in reais:
            print(f"Sample cell {MESES[c['mes'] - 1]} {c['ano']} (week {c['semana']}): "
                  f"N_harm={c['focos_harmonizados']} vs median {c['mediana_historica']} -> {STATUS_EN.get(c['status'], c['status'])} "
                  f"(the sample covers only a few km2, so it is not comparable to a state-wide median)")
    print()
    print(AVISO_LINHA_BASE.format(n_modis=e["n_modis"], n_viirs=e["n_viirs"]))
    print()
    print("Tactical brigade dispatch (Planner-Critic engine) is a separate run:")
    print(f"    python3 -m app.cli --sample --cenario {cenario_exemplo(cal['regiao'])}")
    print("=" * LARGURA)


def main(argv: list[str]) -> int:
    t0 = time.perf_counter()
    if argv and argv[0] in SUBCOMANDOS:
        argv = argv[1:] + ([f"--{argv[0]}"] if f"--{argv[0]}" not in argv else [])
    args = montar_parser().parse_args(argv)
    if not (args.calendario or args.harmonizar):
        args.calendario = True
    regiao = args.regiao.strip().lower()
    if regiao not in REGIOES:
        print(f"Error: region '{args.regiao}' has no FIRMS sample/baseline. Available: {', '.join(REGIOES)}",
              file=sys.stderr)
        return 2
    if not args.sample:
        print("[fococerto] live FIRMS download is not wired into these commands; using data/samples_firms/ "
              "(same as --sample)", file=sys.stderr)
    try:
        modis, viirs, harm = carregar_e_harmonizar(args)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    e = estatisticas(modis, viirs, harm)
    if args.harmonizar:
        imprimir_harmonizacao(e, args)
        if args.calendario:
            print()
    if args.calendario:
        cal = construir_matriz_temporal(harm, ano_inicio=args.ano_inicio, ano_fim=args.ano_fim,
                                        regiao=regiao, nome_exibicao=REGIOES[regiao])
        imprimir_calendario(cal, harm, e)
        if args.json_saida:
            exportar_calendario_json(cal, args.json_saida)
            print(f"Calendar JSON written to {args.json_saida}")
    print(f"[fococerto] done in {time.perf_counter() - t0:.2f} s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
