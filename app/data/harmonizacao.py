"""Harmonização MODIS C6.1 (1 km) + VIIRS 375 m do NASA FIRMS (task-agente-01, CONTEXT.md §2-3).

O VIIRS tem pixel ~7x menor que o MODIS e detecta 3-4x mais focos pontuais para o mesmo fogo, então as contagens
brutas NUNCA são somadas. Em vez disso:

* Os focos de ambos os sensores são padronizados num dicionário único (contrato CONTEXT.md §2).
* São agregados numa grade regular de 0.1° x 0.1° (~11 km), que neutraliza a geometria do pixel.
* Por célula e intervalo de tempo ``t``:

      FRP_harm(t) = soma FRP_MODIS + soma FRP_VIIRS
      N_harm(t)   = N_MODIS                      se t < 2012 (antes do VIIRS)
      N_harm(t)   = N_MODIS + 0.30 * N_VIIRS     se t >= 2012

Sem dependências externas (só biblioteca padrão), para rodar no modo ``--sample`` e nos testes offline.

Esta versão junta duas implementações da equipe: a lógica e o contrato do CONTEXT.md (confianca_pct 0-100,
série por dia/semana/mês, VIIRS ignorado antes de 2012) e a API da primeira versão em ``main``
(``normalizar_confianca`` 0-1, ``FATOR_ESCALA_VIIRS_MODIS``, campos ``celula_lat``/``focos_modis``/``era``/
``frp_harmonizado_mw``/``confianca_media``, brilho e geometria do pixel). Os dois conjuntos de nomes coexistem.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

SENSORES = ("MODIS", "VIIRS")
PASSO_GRADE_GRAUS = 0.1
BETA_VIIRS = 0.30            # peso de contagem do VIIRS em equivalência "MODIS-like"
FATOR_ESCALA_VIIRS_MODIS = BETA_VIIRS   # nome usado na primeira versão (Giglio 2016; Schroeder 2014)
ANO_INICIO_VIIRS = 2012      # Suomi-NPP VIIRS 375 m disponível no FIRMS a partir de 2012-01-20

# Confiança VIIRS (categórica) -> percentual equivalente (CONTEXT.md §2)
CONFIANCA_VIIRS = {"low": 30.0, "l": 30.0, "nominal": 65.0, "n": 65.0, "high": 90.0, "h": 90.0}

SATELITES = {
    "MODIS": {"T": "Terra", "TERRA": "Terra", "A": "Aqua", "AQUA": "Aqua"},
    "VIIRS": {"N": "Suomi-NPP", "NPP": "Suomi-NPP", "SUOMI-NPP": "Suomi-NPP", "SUOMI NPP": "Suomi-NPP",
              "1": "NOAA-20", "J1": "NOAA-20", "N20": "NOAA-20", "NOAA-20": "NOAA-20", "NOAA20": "NOAA-20",
              "2": "NOAA-21", "J2": "NOAA-21", "N21": "NOAA-21", "NOAA-21": "NOAA-21", "NOAA21": "NOAA-21"},
}


class ErroHarmonizacao(ValueError):
    """CSV fora do formato FIRMS esperado."""


# ----------------------------------------------------------------------------- padronização

def _normalizar_sensor(sensor: str) -> str:
    s = (sensor or "").strip().upper()
    if s.startswith("MODIS"):
        return "MODIS"
    if s.startswith("VIIRS"):
        return "VIIRS"
    raise ErroHarmonizacao(f"Sensor desconhecido: {sensor!r} (use 'MODIS' ou 'VIIRS').")


def mapear_confianca(valor, sensor: str) -> float:
    """Confiança em 0-100. MODIS já é numérico; VIIRS é low/nominal/high (-> 30/65/90)."""
    sensor = _normalizar_sensor(sensor)
    texto = str(valor).strip().lower()
    if sensor == "VIIRS" and texto in CONFIANCA_VIIRS:
        return CONFIANCA_VIIRS[texto]
    try:
        num = float(texto)
    except ValueError as e:
        raise ErroHarmonizacao(f"Confiança inválida para {sensor}: {valor!r}") from e
    return max(0.0, min(100.0, num))


def normalizar_confianca(valor, sensor: str) -> float:
    """Confiança em 0.0-1.0 (``mapear_confianca`` / 100). Aceita MODIS já em 0-1. Valor ausente ou inválido: 0.5."""
    if valor is None or str(valor).strip() == "":
        return 0.5
    try:
        num = float(str(valor).strip())
        if num <= 1.0:
            return round(max(0.0, num), 2)
    except ValueError:
        pass
    try:
        return round(mapear_confianca(valor, sensor) / 100.0, 2)
    except ErroHarmonizacao:
        return 0.5


def _float(linha: dict, *colunas: str) -> float:
    for c in colunas:
        v = (linha.get(c) or "").strip() if isinstance(linha.get(c), str) else linha.get(c)
        if v not in (None, ""):
            try:
                return float(v)
            except ValueError:
                continue
    return 0.0


def _nome_satelite(codigo: str, sensor: str) -> str:
    c = (codigo or "").strip()
    return SATELITES[sensor].get(c.upper(), c or "?")


def _parse_data_hora(acq_date: str, acq_time: str) -> datetime:
    d = date.fromisoformat(acq_date.strip())
    hhmm = str(acq_time).strip().zfill(4)
    return datetime(d.year, d.month, d.day, int(hhmm[:2]), int(hhmm[2:4]), tzinfo=timezone.utc)


def semana_do_ano(d: date) -> int:
    """Semana ISO limitada a 1..52 (a rara semana 53 é somada à 52, para a grade anual ter 52 colunas)."""
    return min(d.isocalendar()[1], 52)


def padronizar_registro(linha: dict, sensor: str) -> dict:
    """Uma linha do CSV FIRMS -> dicionário do contrato unificado (CONTEXT.md §2)."""
    sensor = _normalizar_sensor(sensor)
    try:
        lat = float(linha["latitude"])
        lon = float(linha["longitude"])
        dt = _parse_data_hora(linha["acq_date"], linha["acq_time"])
        frp = float(linha.get("frp") or 0.0)
    except (KeyError, ValueError) as e:
        raise ErroHarmonizacao(f"Linha {sensor} inválida ({e}): {linha}") from e
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise ErroHarmonizacao(f"Coordenada fora do intervalo WGS84: {lat}, {lon}")
    sat = _nome_satelite(linha.get("satellite", ""), sensor)
    hora = dt.strftime("%H%M")
    conf_pct = mapear_confianca(linha.get("confidence", ""), sensor)
    cel_lat, cel_lon = obter_celula_grade(lat, lon)
    return {
        "id": f"{sensor}_{sat}_{lat:.4f}_{lon:.4f}_{dt.date().isoformat()}_{hora}",
        "sensor": sensor,
        "satelite": sat,
        "lat": lat,
        "lon": lon,
        "data_hora_utc": dt,
        "ano": dt.year,
        "mes": dt.month,
        "semana": semana_do_ano(dt.date()),
        "dia_noite": (linha.get("daynight") or "").strip().upper()[:1] or "D",
        "confianca_pct": conf_pct,
        "frp_mw": max(0.0, frp),
        # campos da primeira versão (main)
        "confianca": round(conf_pct / 100.0, 2),
        "codigo_satelite": (linha.get("satellite") or "").strip(),
        "celula_lat": cel_lat,
        "celula_lon": cel_lon,
        "data": dt.date().isoformat(),
        "hora": hora,
        "dia": dt.day,
        "scan": _float(linha, "scan"),
        "track": _float(linha, "track"),
        "brilho_k": _float(linha, "brightness", "bright_ti4"),        # T21/22 (MODIS) ou I4 (VIIRS)
        "brilho_bg_k": _float(linha, "bright_t31", "bright_ti5"),     # T31 (MODIS) ou I5 (VIIRS)
        "versao": (linha.get("version") or "").strip(),
    }


def carregar_e_padronizar_focos(caminho_csv: Path, sensor: str, confianca_minima: float = 0.0) -> list[dict]:
    """Lê um CSV do NASA FIRMS (MODIS C6.1 ou VIIRS 375 m) e devolve a lista padronizada.

    ``confianca_minima`` (0-100) descarta detecções de baixa confiança (ex.: 30 remove VIIRS ``low``).
    Linhas duplicadas (mesmo id) são contadas uma vez só.
    """
    sensor = _normalizar_sensor(sensor)
    caminho_csv = Path(caminho_csv)
    if not caminho_csv.exists():
        raise FileNotFoundError(caminho_csv)
    focos: dict[str, dict] = {}
    with caminho_csv.open(newline="", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)
        faltando = {"latitude", "longitude", "acq_date", "acq_time", "frp", "confidence"} - set(leitor.fieldnames or [])
        if faltando:
            raise ErroHarmonizacao(f"{caminho_csv.name}: colunas ausentes {sorted(faltando)}")
        for linha in leitor:
            if not any((v or "").strip() for v in linha.values()):
                continue
            reg = padronizar_registro(linha, sensor)
            if reg["confianca_pct"] >= confianca_minima:
                focos.setdefault(reg["id"], reg)
    return list(focos.values())


# ----------------------------------------------------------------------------- grade espacial

def obter_celula_grade(lat: float, lon: float, step: float = PASSO_GRADE_GRAUS) -> tuple[float, float]:
    """Centro da célula de ``step`` graus que contém o ponto (arredondado para evitar ruído de float)."""
    casas = max(0, len(f"{step:.10f}".rstrip("0").split(".")[1]))
    return (round(round(lat / step) * step, casas + 1), round(round(lon / step) * step, casas + 1))


def agregar_em_grade(focos: Iterable[dict], step: float = PASSO_GRADE_GRAUS) -> dict:
    """Agrupa focos padronizados por célula de grade.

    Retorna ``{(lat_c, lon_c): {...}}`` com ``n_modis``/``n_viirs``, ``frp_modis_mw``/``frp_viirs_mw``, ``ids`` e,
    da primeira versão, ``celula_lat``/``celula_lon``, ``total_focos``, ``focos_modis``/``focos_viirs``,
    ``frp_total_mw``, ``frp_medio_mw``, ``confianca_media`` (0-1) e ``focos``. ``total_focos`` é a soma BRUTA,
    só para inspeção: para comparar períodos use ``harmonizar_series``.
    """
    grade: dict[tuple[float, float], dict] = {}
    for f in focos:
        chave = obter_celula_grade(f["lat"], f["lon"], step)
        c = grade.setdefault(chave, {"lat": chave[0], "lon": chave[1], "celula_lat": chave[0],
                                     "celula_lon": chave[1], "n_modis": 0, "n_viirs": 0, "frp_modis_mw": 0.0,
                                     "frp_viirs_mw": 0.0, "ids": [], "focos": []})
        s = f["sensor"].lower()
        c[f"n_{s}"] += 1
        c[f"frp_{s}_mw"] += f["frp_mw"]
        c["ids"].append(f["id"])
        c["focos"].append(f)
    for c in grade.values():
        total = c["n_modis"] + c["n_viirs"]
        c.update(total_focos=total, focos_modis=c["n_modis"], focos_viirs=c["n_viirs"],
                 frp_total_mw=round(c["frp_modis_mw"] + c["frp_viirs_mw"], 2),
                 frp_medio_mw=round((c["frp_modis_mw"] + c["frp_viirs_mw"]) / total, 2),
                 confianca_media=round(sum(_confianca_01(f) for f in c["focos"]) / total, 3))
    return grade


def _confianca_01(f: dict) -> float:
    if "confianca" in f:
        return float(f["confianca"])
    return float(f.get("confianca_pct", 50.0)) / 100.0


# ----------------------------------------------------------------------------- harmonização

def contagem_harmonizada(n_modis: float, n_viirs: float, ano: int, beta: float = BETA_VIIRS) -> float:
    """N_harm = N_MODIS (t < 2012) ou N_MODIS + beta * N_VIIRS (t >= 2012)."""
    if ano < ANO_INICIO_VIIRS:
        return float(n_modis)
    return float(n_modis) + beta * float(n_viirs)


def frp_harmonizado(frp_modis: float, frp_viirs: float, ano: int) -> float:
    """FRP_harm = soma FRP MODIS + soma FRP VIIRS (VIIRS só entra a partir de 2012)."""
    return float(frp_modis) + (float(frp_viirs) if ano >= ANO_INICIO_VIIRS else 0.0)


def _data_do_foco(f: dict) -> date | None:
    """Data do foco: ``data_hora_utc`` (datetime ou ISO), ``data`` (ISO) ou None (registro só com ano/semana)."""
    v = f.get("data_hora_utc") or f.get("data")
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, str) and v:
        try:
            return date.fromisoformat(v[:10])
        except ValueError:
            return None
    return None


def _chave_tempo(f: dict, periodo: str):
    d = _data_do_foco(f)
    if periodo == "dia" and d is None:
        periodo = "semana"   # registro sem data: agrupa pela semana informada
    if periodo == "dia":
        return d.isoformat()
    if periodo == "semana":
        return f"{f['ano']}-W{f['semana']:02d}"
    if periodo == "mes":
        return f"{f['ano']}-{f['mes']:02d}"
    raise ValueError(f"periodo inválido: {periodo!r} (use dia, semana ou mes)")


def harmonizar_series(focos_modis: list[dict], focos_viirs: list[dict], step: float = PASSO_GRADE_GRAUS,
                      beta: float = BETA_VIIRS, periodo: str = "dia") -> list[dict]:
    """Funde MODIS e VIIRS por (célula de grade, intervalo de tempo) aplicando a equivalência de contagem e a
    conservação de FRP. Retorna uma lista ordenada por (tempo, lat, lon) com um registro por célula ativa:

    ``{"celula_id", "lat", "lon", "periodo", "chave_tempo", "data", "ano", "mes", "semana", "n_modis", "n_viirs",
    "focos_harmonizados", "frp_modis_mw", "frp_viirs_mw", "frp_total_mw"}``

    Também inclui os campos da primeira versão: ``celula_lat``/``celula_lon``, ``focos_modis``/``focos_viirs``,
    ``frp_harmonizado_mw`` (= ``frp_total_mw``), ``era`` (``HISTORICO_MODIS_EXCLUSIVO`` ou
    ``SOBREPOSICAO_MODIS_VIIRS``), ``fator_escala_viirs``, ``confianca_media`` (0-1) e ``total_registros_brutos``.

    ``data``/``mes``/``semana`` vêm da primeira detecção do grupo (em ``periodo="dia"`` são exatos). Como
    N_harm e FRP_harm são lineares, o calendário pode somar registros diários em semanas ou meses sem viés.
    Focos VIIRS anteriores a 2012 (não deveriam existir) são ignorados.
    """
    for f in focos_modis:
        if f["sensor"] != "MODIS":
            raise ErroHarmonizacao(f"Foco não-MODIS na lista MODIS: {f['id']}")
    for f in focos_viirs:
        if f["sensor"] != "VIIRS":
            raise ErroHarmonizacao(f"Foco não-VIIRS na lista VIIRS: {f['id']}")

    grupos: dict[tuple, list[dict]] = defaultdict(list)
    for f in [*focos_modis, *focos_viirs]:
        if f["sensor"] == "VIIRS" and f["ano"] < ANO_INICIO_VIIRS:
            continue
        grupos[(_chave_tempo(f, periodo), *obter_celula_grade(f["lat"], f["lon"], step))].append(f)

    saida: list[dict] = []
    for (chave_t, lat_c, lon_c), focos in grupos.items():
        primeiro = min(focos, key=lambda x: (_data_do_foco(x) or date.max, str(x.get("data_hora_utc", ""))))
        d0 = _data_do_foco(primeiro)
        ano = primeiro["ano"]
        n_m = sum(1 for f in focos if f["sensor"] == "MODIS")
        n_v = sum(1 for f in focos if f["sensor"] == "VIIRS")
        frp_m = sum(f["frp_mw"] for f in focos if f["sensor"] == "MODIS")
        frp_v = sum(f["frp_mw"] for f in focos if f["sensor"] == "VIIRS")
        saida.append({
            "celula_id": f"{lat_c:+.2f}_{lon_c:+.2f}",
            "lat": lat_c,
            "lon": lon_c,
            "periodo": periodo,
            "chave_tempo": chave_t,
            "data": d0.isoformat() if d0 else None,
            "ano": ano,
            "mes": primeiro["mes"],
            "semana": primeiro["semana"],
            "n_modis": n_m,
            "n_viirs": n_v,
            "focos_harmonizados": round(contagem_harmonizada(n_m, n_v, ano, beta), 4),
            "frp_modis_mw": round(frp_m, 4),
            "frp_viirs_mw": round(frp_v, 4),
            "frp_total_mw": round(frp_harmonizado(frp_m, frp_v, ano), 4),
            # campos da primeira versão (main)
            "celula_lat": lat_c,
            "celula_lon": lon_c,
            "focos_modis": n_m,
            "focos_viirs": n_v,
            "frp_harmonizado_mw": round(frp_harmonizado(frp_m, frp_v, ano), 4),
            "era": "SOBREPOSICAO_MODIS_VIIRS" if ano >= ANO_INICIO_VIIRS else "HISTORICO_MODIS_EXCLUSIVO",
            "fator_escala_viirs": beta if ano >= ANO_INICIO_VIIRS else 0.0,
            "confianca_media": round(sum(_confianca_01(f) for f in focos) / len(focos), 2),
            "total_registros_brutos": n_m + n_v,
        })
    saida.sort(key=lambda r: (r["chave_tempo"], r["lat"], r["lon"]))
    return saida


def resumo_harmonizacao(harm: list[dict]) -> dict:
    """Totais da série harmonizada (para log/CLI)."""
    return {
        "registros": len(harm),
        "celulas": len({r["celula_id"] for r in harm}),
        "n_modis": sum(r["n_modis"] for r in harm),
        "n_viirs": sum(r["n_viirs"] for r in harm),
        "focos_harmonizados": round(sum(r["focos_harmonizados"] for r in harm), 4),
        "frp_total_mw": round(sum(r["frp_total_mw"] for r in harm), 4),
    }


def exportar_harmonizacao(harm: list[dict], caminho_saida: Path) -> Path:
    """Grava a série harmonizada em ``.csv`` ou ``.json`` (decidido pela extensão)."""
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    if caminho_saida.suffix.lower() == ".json":
        caminho_saida.write_text(json.dumps({"resumo": resumo_harmonizacao(harm), "registros": harm},
                                            ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        campos = list(harm[0].keys()) if harm else ["celula_id"]
        with caminho_saida.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(harm)
    return caminho_saida


AMOSTRA_MODIS = Path(__file__).resolve().parents[2] / "data" / "samples_firms" / "modis_sample_c6.csv"
AMOSTRA_VIIRS = Path(__file__).resolve().parents[2] / "data" / "samples_firms" / "viirs_sample_375m.csv"


def harmonizar_amostra(periodo: str = "dia") -> list[dict]:
    """Atalho: harmoniza os CSVs de AMOSTRA em ``data/samples_firms/`` (dados de amostra, não observações reais)."""
    return harmonizar_series(carregar_e_padronizar_focos(AMOSTRA_MODIS, "MODIS"),
                             carregar_e_padronizar_focos(AMOSTRA_VIIRS, "VIIRS"), periodo=periodo)


if __name__ == "__main__":
    h = harmonizar_amostra()
    print(json.dumps(resumo_harmonizacao(h), indent=2))
