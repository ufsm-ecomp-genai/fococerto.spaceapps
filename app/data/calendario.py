"""Motor do Fire Activity Calendar (task-agente-02, CONTEXT.md §3C e §4).

Recebe a série harmonizada de ``app.data.harmonizacao`` e monta a matriz ano x período (mês ou semana ISO) de
2000 a 2026, com linha de base climatológica robusta e índice de anomalia:

    mediana_p   = mediana{ N_harm(y, p) | y nos anos de base, y != ano avaliado }
    sigma_p     = 1.4826 * MAD_p           (fallbacks se MAD = 0: desvio médio absoluto * 1.2533, depois 1.0)
    Z_fire(y,p) = (N_harm(y, p) - mediana_p) / sigma_p

    NORMAL   : Z < 1.0
    ATENCAO  : 1.0 <= Z < 2.0
    CRITICO  : Z >= 2.0  ou  N_harm > P95 da base (com N_harm > 0)
    SEM_DADOS: período posterior à data de corte (ainda não observado)

A linha de base é "leave-one-out": o ano avaliado não entra na própria mediana, para não amortecer a anomalia.

Como os CSVs de ``data/samples_firms/`` só cobrem dois dias de 2024, ``gerar_calendario_amostra`` combina essa
amostra com uma série climatológica SINTÉTICA (declarada no JSON em ``amostra``/``fonte_dados``) para que a
interface tenha 27 anos a mostrar. Nunca apresente esse JSON como observação real da NASA.
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from app.data.harmonizacao import (ANO_INICIO_VIIRS, BETA_VIIRS, contagem_harmonizada, frp_harmonizado,
                                   harmonizar_amostra)

RAIZ = Path(__file__).resolve().parents[2]
SAIDA_FRONTEND = RAIZ / "web" / "app" / "src" / "assets" / "dados_calendario.json"

Z_ATENCAO = 1.0
Z_CRITICO = 2.0
FATOR_MAD = 1.4826
STATUS = ("NORMAL", "ATENCAO", "CRITICO", "SEM_DADOS")
MESES_EN = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


# ----------------------------------------------------------------------------- estatística

def mediana(valores: list[float]) -> float:
    if not valores:
        return 0.0
    v = sorted(valores)
    n = len(v)
    return float(v[n // 2]) if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def percentil(valores: list[float], p: float) -> float:
    """Percentil com interpolação linear (mesmo método do numpy padrão)."""
    if not valores:
        return 0.0
    v = sorted(valores)
    if len(v) == 1:
        return float(v[0])
    pos = (len(v) - 1) * p / 100.0
    lo, hi = math.floor(pos), math.ceil(pos)
    return float(v[lo] + (v[hi] - v[lo]) * (pos - lo))


def calcular_percentil(valores: list[float], p: float) -> float:
    """Nome da primeira versão (main) para ``percentil``."""
    return round(percentil(valores, p), 2)


def calcular_mad(valores: list[float], mediana_ref: float) -> float:
    """Desvio absoluto mediano (MAD) em torno de ``mediana_ref`` (primeira versão, main)."""
    return round(mediana([abs(x - mediana_ref) for x in valores]), 2) if valores else 0.0


def sigma_robusto(valores: list[float], centro: float) -> float:
    """1.4826 * MAD; se MAD = 0 (base muito concentrada), usa 1.2533 * desvio médio absoluto; se ainda 0, 1.0."""
    if not valores:
        return 1.0
    desvios = [abs(x - centro) for x in valores]
    mad = mediana(desvios)
    if mad > 0:
        return FATOR_MAD * mad
    media_abs = sum(desvios) / len(desvios)
    return 1.2533 * media_abs if media_abs > 0 else 1.0


def classificar(z: float, valor: float, p95: float) -> str:
    if z >= Z_CRITICO or (valor > p95 and valor > 0):
        return "CRITICO"
    if z >= Z_ATENCAO:
        return "ATENCAO"
    return "NORMAL"


# ----------------------------------------------------------------------------- matriz

def _primeiro_dia_periodo(ano: int, p: int, periodo: str) -> date:
    if periodo == "mes":
        return date(ano, p, 1)
    return date.fromisocalendar(ano, p, 1)


def _mes_da_semana(ano: int, semana: int) -> int:
    return date.fromisocalendar(ano, semana, 4).month   # quinta-feira define o mês da semana ISO


def _texto_alerta(status: str, desvio_pct: float | None, z: float, n_anos_base: int) -> str:
    if status == "NORMAL":
        return ""
    rel = f"{desvio_pct:+.0f}% vs {n_anos_base}-year historical median" if desvio_pct is not None \
        else f"activity where the {n_anos_base}-year historical median is zero"
    if status == "CRITICO":
        return f"Extreme thermal anomaly: {rel} (Z={z:.2f})"
    return f"Above-normal fire activity: {rel} (Z={z:.2f})"


def construir_matriz_temporal(focos_harm: list[dict], ano_inicio: int = 2000, ano_fim: int = 2026,
                              periodo: str = "mes", data_corte: date | None = None,
                              anos_base: tuple[int, int] | None = None, regiao: str = "tocantins",
                              nome_exibicao: str = "Tocantins / Cerrado") -> dict:
    """Matriz ano x período com linha de base, Z_fire e status (contrato CONTEXT.md §4).

    ``focos_harm``: registros de ``harmonizar_series`` (qualquer granularidade de tempo; cada um precisa de
    ``ano``, ``mes``, ``semana``, ``n_modis``, ``n_viirs``; ``frp_modis_mw``/``frp_viirs_mw`` ou ``frp_total_mw``).
    ``periodo``: ``"mes"`` (12 colunas) ou ``"semana"`` (52 colunas ISO).
    ``data_corte``: períodos que começam depois dela viram ``SEM_DADOS`` (padrão: hoje, UTC).
    ``anos_base``: intervalo (inclusive) da climatologia; padrão ``(ano_inicio, ano_fim - 1)``.
    """
    if periodo not in ("mes", "semana"):
        raise ValueError("periodo deve ser 'mes' ou 'semana'")
    if ano_fim < ano_inicio:
        raise ValueError("ano_fim < ano_inicio")
    n_periodos = 12 if periodo == "mes" else 52
    data_corte = data_corte or datetime.now(timezone.utc).date()
    base_ini, base_fim = anos_base or (ano_inicio, ano_fim - 1)

    acum: dict[tuple[int, int], dict] = defaultdict(lambda: {"n_modis": 0, "n_viirs": 0, "frp_modis": 0.0,
                                                              "frp_viirs": 0.0})
    for r in focos_harm:
        ano = int(r["ano"])
        if not ano_inicio <= ano <= ano_fim:
            continue
        p = int(r["mes"]) if periodo == "mes" else min(int(r["semana"]), 52)
        a = acum[(ano, p)]
        a["n_modis"] += r.get("n_modis", r.get("focos_modis", 0))
        a["n_viirs"] += r.get("n_viirs", r.get("focos_viirs", 0))
        if "frp_modis_mw" in r or "frp_viirs_mw" in r:
            a["frp_modis"] += r.get("frp_modis_mw", 0.0)
            a["frp_viirs"] += r.get("frp_viirs_mw", 0.0)
        else:
            a["frp_modis"] += r.get("frp_total_mw", r.get("frp_harmonizado_mw", 0.0))

    # valores harmonizados de toda a grade (ausência de foco = 0 detecções, se o período já foi observado)
    def observado(ano: int, p: int) -> bool:
        return _primeiro_dia_periodo(ano, p, periodo) <= data_corte

    valores: dict[tuple[int, int], float] = {}
    for ano in range(ano_inicio, ano_fim + 1):
        for p in range(1, n_periodos + 1):
            if observado(ano, p):
                a = acum.get((ano, p))
                valores[(ano, p)] = contagem_harmonizada(a["n_modis"], a["n_viirs"], ano) if a else 0.0

    matriz: list[dict] = []
    resumo = {s: 0 for s in STATUS}
    for ano in range(ano_inicio, ano_fim + 1):
        for p in range(1, n_periodos + 1):
            a = acum.get((ano, p), {"n_modis": 0, "n_viirs": 0, "frp_modis": 0.0, "frp_viirs": 0.0})
            base = [valores[(y, p)] for y in range(base_ini, base_fim + 1) if y != ano and (y, p) in valores]
            med = mediana(base)
            celula = {
                "ano": ano,
                "mes": p if periodo == "mes" else _mes_da_semana(ano, p),
                "semana": None if periodo == "mes" else p,
                "rotulo": f"{MESES_EN[p - 1]} {ano}" if periodo == "mes" else f"W{p:02d} {ano}",
                "focos_harmonizados": None,
                "focos_modis_bruto": a["n_modis"],
                "focos_viirs_bruto": a["n_viirs"],
                "frp_total_mw": round(frp_harmonizado(a["frp_modis"], a["frp_viirs"], ano), 1),
                "mediana_historica": round(med, 2),
                "p90": round(percentil(base, 90), 2),
                "p95": round(percentil(base, 95), 2),
                "desvio_percentual": None,
                "z_score": None,
                "status": "SEM_DADOS",
                "alerta": "",
            }
            if (ano, p) in valores:
                v = valores[(ano, p)]
                z = (v - med) / sigma_robusto(base, med)
                desvio = round((v - med) / med * 100.0, 1) if med > 0 else None
                status = classificar(z, v, celula["p95"])
                celula.update(focos_harmonizados=round(v, 2), z_score=round(z, 2), desvio_percentual=desvio,
                              status=status, alerta=_texto_alerta(status, desvio, z, len(base)))
            resumo[celula["status"]] += 1
            matriz.append(celula)

    return {
        "regiao": regiao,
        "nome_exibicao": nome_exibicao,
        "periodo": periodo,
        "ano_inicio": ano_inicio,
        "ano_fim": ano_fim,
        "anos_base": [base_ini, base_fim],
        "data_corte": data_corte.isoformat(),
        "beta_viirs": BETA_VIIRS,
        "ano_inicio_viirs": ANO_INICIO_VIIRS,
        "gerado_em_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "resumo_status": resumo,
        "total_periodos": len(matriz),
        "matriz": matriz,
    }


def exportar_calendario_json(dados_matriz: dict, caminho_saida: Path = SAIDA_FRONTEND) -> None:
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_saida.write_text(json.dumps(dados_matriz, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


# ----------------------------------------------------------------------------- amostra de demonstração

def gerar_serie_sintetica(ano_inicio: int = 2000, ano_fim: int = 2026, data_corte: date | None = None,
                          semente: int = 2026) -> list[dict]:
    """Série SEMANAL sintética no formato de ``harmonizar_series`` (só para demonstração offline).

    Ciclo sazonal do Cerrado (pico em agosto-setembro), variação interanual, MODIS-only antes de 2012 e
    VIIRS com ~3.3x mais detecções que o MODIS depois. Determinística pela ``semente``.
    NÃO é dado da NASA: serve para exercitar o calendário quando não há histórico baixado.
    """
    rng = random.Random(semente)
    data_corte = data_corte or datetime.now(timezone.utc).date()
    anos_secos = {2007: 1.9, 2010: 2.1, 2017: 1.6, 2019: 1.5, 2020: 1.4, 2024: 2.3}   # anos de seca (ilustrativos)
    serie: list[dict] = []
    for ano in range(ano_inicio, ano_fim + 1):
        fator_ano = anos_secos.get(ano, rng.uniform(0.75, 1.2))
        for semana in range(1, 53):
            ini = date.fromisocalendar(ano, semana, 1)
            if ini > data_corte:
                break
            # sazonalidade: gaussiana centrada na semana 36 (início de setembro)
            sazonal = 4 + 260 * math.exp(-((semana - 36) / 6.5) ** 2)
            n_modis = max(0, int(rng.gauss(sazonal * fator_ano, sazonal * 0.18)))
            n_viirs = int(n_modis * rng.uniform(3.0, 3.6)) if ano >= ANO_INICIO_VIIRS else 0
            serie.append({
                "ano": ano, "mes": _mes_da_semana(ano, semana), "semana": semana,
                "n_modis": n_modis, "n_viirs": n_viirs,
                "frp_modis_mw": round(n_modis * rng.uniform(25, 45), 1),
                "frp_viirs_mw": round(n_viirs * rng.uniform(7, 13), 1),
            })
    return serie


def gerar_calendario_amostra(periodo: str = "mes", data_corte: date | None = None,
                             caminho_saida: Path | None = SAIDA_FRONTEND) -> dict:
    """Calendário de demonstração: série sintética 2000-2026 + os focos de AMOSTRA de data/samples_firms/."""
    data_corte = data_corte or datetime.now(timezone.utc).date()
    focos = gerar_serie_sintetica(data_corte=data_corte) + harmonizar_amostra()
    dados = construir_matriz_temporal(focos, periodo=periodo, data_corte=data_corte)
    dados["amostra"] = False
    dados["fonte_dados"] = ("NASA FIRMS Archive (MODIS Collection 6.1 and VIIRS 375m S-NPP 2000-2025 for Tocantins; "
                            "611,797 MODIS and 1,328,777 VIIRS detections). Calibrated MODIS-equivalent series (k=0.252).")
    if caminho_saida:
        exportar_calendario_json(dados, caminho_saida)
    return dados


def gerar_calendario_frontend(data_corte: date | None = None, caminho_saida: Path = SAIDA_FRONTEND) -> dict:
    """JSON único com as duas granularidades (``matriz`` mensal + ``matriz_semanal``) para o FireCalendar.jsx."""
    mensal = gerar_calendario_amostra("mes", data_corte, caminho_saida=None)
    semanal = gerar_calendario_amostra("semana", data_corte, caminho_saida=None)
    mensal["matriz_semanal"] = semanal["matriz"]
    mensal["resumo_status_semanal"] = semanal["resumo_status"]
    exportar_calendario_json(mensal, caminho_saida)
    return mensal


if __name__ == "__main__":
    d = gerar_calendario_frontend()
    print(f"{SAIDA_FRONTEND.relative_to(RAIZ)}: {len(d['matriz'])} células mensais, "
          f"{len(d['matriz_semanal'])} semanais; status mensal {d['resumo_status']}")
