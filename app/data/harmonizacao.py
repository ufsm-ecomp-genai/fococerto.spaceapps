"""
Pipeline de Harmonização Científica MODIS (1 km) + VIIRS (375 m).
NASA International Space Apps Challenge 2026 - Harmonization of MODIS and VIIRS Hot Spots.

Equipe ECOMP - UFSM (Universidade Federal de Santa Maria, RS, Brasil).
Distribuído sob licença Apache-2.0.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


# Mapeamento oficial de identificadores de satélites NASA/NOAA
MAPA_SATELITES: Dict[str, str] = {
    "T": "Terra",
    "A": "Aqua",
    "N": "Suomi-NPP",
    "1": "NOAA-20",
    "2": "NOAA-21",
}

# Fator empírico de conversão de resolução espacial (VIIRS 375m para escala equivalente MODIS 1km)
# Fundamentação: Giglio et al. (2016) e Schroeder et al. (2014)
# O pixel VIIRS cobre ~0.14 km² vs 1.0-9.6 km² do MODIS, detectando ~3.3x mais focos para a mesma queimada.
FATOR_ESCALA_VIIRS_MODIS: float = 0.30


def normalizar_confianca(valor: Any, sensor: str) -> float:
    """
    Padroniza a métrica de confiança para uma escala contínua float entre 0.0 e 1.0.

    - MODIS Collection 6.1: valor percentual numérico (0 a 100) -> 0.0 a 1.0.
    - VIIRS 375m: classes categóricas ('low' -> 0.3, 'nominal' -> 0.7, 'high' -> 1.0).
    """
    if valor is None:
        return 0.50

    sensor_upper = sensor.strip().upper()

    if sensor_upper == "VIIRS":
        s_val = str(valor).strip().lower()
        if "low" in s_val or s_val == "l":
            return 0.30
        if "nom" in s_val or s_val == "n":
            return 0.70
        if "high" in s_val or s_val == "h":
            return 1.00
        try:
            num = float(valor)
            return min(1.0, max(0.0, num / 100.0 if num > 1.0 else num))
        except (ValueError, TypeError):
            return 0.70

    # Sensor MODIS ou padrão
    try:
        num = float(valor)
        if num > 1.0:
            return round(min(1.0, max(0.0, num / 100.0)), 2)
        return round(min(1.0, max(0.0, num)), 2)
    except (ValueError, TypeError):
        return 0.50


def obter_celula_grade(lat: float, lon: float, step: float = 0.1) -> Tuple[float, float]:
    """
    Discretiza coordenadas geográficas contínuas em uma grade espacial uniforme.
    
    Por padrão utiliza passo de 0.1° (~11.1 km no equador), neutralizando as variações
    angulares de footprint causadas pelo efeito bow-tie nas bordas da varredura ótica.
    """
    celula_lat = round(round(lat / step) * step, 4)
    celula_lon = round(round(lon / step) * step, 4)
    return (celula_lat, celula_lon)


def carregar_e_padronizar_focos(caminho_csv: Union[Path, str], sensor: str = "MODIS") -> List[Dict[str, Any]]:
    """
    Ingere arquivos brutos de focos térmicos do NASA FIRMS (MODIS C6.1 ou VIIRS 375m)
    e os converte para uma lista de registros padronizados na memória.

    Colunas suportadas:
    - MODIS: latitude, longitude, brightness, scan, track, acq_date, acq_time, satellite, confidence, version, bright_t31, frp, daynight
    - VIIRS: latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, confidence, version, bright_ti5, frp, daynight
    """
    caminho = Path(caminho_csv)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {caminho}")

    sensor_clean = sensor.strip().upper()
    focos_padronizados: List[Dict[str, Any]] = []

    with open(caminho, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            scan = float(row.get("scan", 1.0) or 1.0)
            track = float(row.get("track", 1.0) or 1.0)
            acq_date = row.get("acq_date", "").strip()
            acq_time_raw = row.get("acq_time", "0000").strip()
            acq_time = acq_time_raw.zfill(4)

            sat_code = row.get("satellite", "").strip()
            sat_nome = MAPA_SATELITES.get(sat_code, sat_code or "Unknown")

            # Mapeamento do canal primário de temperatura de brilho (Kelvin)
            if "brightness" in row and row["brightness"]:
                brilho_k = float(row["brightness"])
            elif "bright_ti4" in row and row["bright_ti4"]:
                brilho_k = float(row["bright_ti4"])
            else:
                brilho_k = 0.0

            # Mapeamento do canal secundário de fundo térmico (Kelvin)
            if "bright_t31" in row and row["bright_t31"]:
                brilho_bg_k = float(row["bright_t31"])
            elif "bright_ti5" in row and row["bright_ti5"]:
                brilho_bg_k = float(row["bright_ti5"])
            else:
                brilho_bg_k = 0.0

            frp = float(row.get("frp", 0.0) or 0.0)
            daynight = row.get("daynight", "D").strip().upper()
            versao = row.get("version", "").strip()

            conf_bruta = row.get("confidence")
            conf_norm = normalizar_confianca(conf_bruta, sensor_clean)

            # Decomposição temporal
            try:
                dt = datetime.strptime(f"{acq_date} {acq_time}", "%Y-%m-%d %H%M")
                ano = dt.year
                mes = dt.month
                dia = dt.day
                semana = dt.isocalendar()[1]
                dt_iso = dt.strftime("%Y-%m-%dT%H:%M:00Z")
            except (ValueError, TypeError):
                dt_iso = f"{acq_date}T{acq_time[:2]}:{acq_time[2:]}:00Z"
                ano = int(acq_date.split("-")[0]) if "-" in acq_date else 2024
                mes = int(acq_date.split("-")[1]) if "-" in acq_date else 1
                dia = int(acq_date.split("-")[2]) if "-" in acq_date else 1
                semana = 1

            cel_lat, cel_lon = obter_celula_grade(lat, lon, step=0.1)

            registro = {
                "id": f"{sensor_clean}_{sat_nome}_{lat:.4f}_{lon:.4f}_{acq_date}_{acq_time}_{idx}",
                "sensor": sensor_clean,
                "satelite": sat_nome,
                "codigo_satelite": sat_code,
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "celula_lat": cel_lat,
                "celula_lon": cel_lon,
                "data_hora_utc": dt_iso,
                "data": acq_date,
                "hora": acq_time,
                "ano": ano,
                "mes": mes,
                "dia": dia,
                "semana": semana,
                "dia_noite": daynight,
                "confianca": conf_norm,
                "confianca_pct": round(conf_norm * 100.0, 1),
                "frp_mw": round(frp, 2),
                "scan": scan,
                "track": track,
                "brilho_k": brilho_k,
                "brilho_bg_k": brilho_bg_k,
                "versao": versao,
            }
            focos_padronizados.append(registro)

    return focos_padronizados


def agregar_em_grade(focos: List[Dict[str, Any]], step: float = 0.1) -> Dict[Tuple[float, float], Dict[str, Any]]:
    """
    Agrega uma coleção de focos térmicos em células de uma grade regular.

    Retorna um dicionário indexado por (celula_lat, celula_lon) contendo métricas agregadas
    como contagem total, contagem por sensor, FRP acumulado, FRP médio e lista de ocorrências.
    """
    grade: Dict[Tuple[float, float], Dict[str, Any]] = {}

    for foco in focos:
        celula = obter_celula_grade(foco["lat"], foco["lon"], step=step)

        if celula not in grade:
            grade[celula] = {
                "celula_lat": celula[0],
                "celula_lon": celula[1],
                "total_focos": 0,
                "focos_modis": 0,
                "focos_viirs": 0,
                "frp_total_mw": 0.0,
                "frp_medio_mw": 0.0,
                "confianca_media": 0.0,
                "focos": [],
            }

        bloco = grade[celula]
        bloco["total_focos"] += 1
        if foco["sensor"] == "MODIS":
            bloco["focos_modis"] += 1
        elif foco["sensor"] == "VIIRS":
            bloco["focos_viirs"] += 1

        bloco["frp_total_mw"] += foco["frp_mw"]
        bloco["focos"].append(foco)

    # Cálculo de médias finais por célula
    for celula, bloco in grade.items():
        total = bloco["total_focos"]
        if total > 0:
            bloco["frp_total_mw"] = round(bloco["frp_total_mw"], 2)
            bloco["frp_medio_mw"] = round(bloco["frp_total_mw"] / total, 2)
            soma_conf = sum(f["confianca"] for f in bloco["focos"])
            bloco["confianca_media"] = round(soma_conf / total, 3)

    return grade


def harmonizar_series(
    focos_modis: List[Dict[str, Any]],
    focos_viirs: List[Dict[str, Any]],
    step: float = 0.1,
) -> List[Dict[str, Any]]:
    """
    Executa a reconciliação e fusão de dados entre as séries temporais do MODIS e do VIIRS.

    Formulação de Harmonização:
    1. Agrupamento espaço-temporal por célula de grade (0.1°) e intervalo semanal/mensal.
    2. Para a era pré-VIIRS (< 2012):
       N_harmonizado = N_MODIS
       FRP_harmonizado = sum(FRP_MODIS)
    3. Para a era de sobreposição (>= 2012):
       N_harmonizado = N_MODIS + 0.30 * N_VIIRS
       FRP_harmonizado = sum(FRP_MODIS) + sum(FRP_VIIRS)
       (Em células onde apenas o VIIRS detectou fogo, N_harm = 0.30 * N_VIIRS).
    """
    # Mapeamento chave espaço-temporal -> {'modis': [...], 'viirs': [...]}
    agrupamento: Dict[Tuple[int, int, int, float, float], Dict[str, List[Dict[str, Any]]]] = {}

    for foco in focos_modis:
        cel = obter_celula_grade(foco["lat"], foco["lon"], step=step)
        chave = (foco["ano"], foco["mes"], foco["semana"], cel[0], cel[1])
        if chave not in agrupamento:
            agrupamento[chave] = {"modis": [], "viirs": []}
        agrupamento[chave]["modis"].append(foco)

    for foco in focos_viirs:
        cel = obter_celula_grade(foco["lat"], foco["lon"], step=step)
        chave = (foco["ano"], foco["mes"], foco["semana"], cel[0], cel[1])
        if chave not in agrupamento:
            agrupamento[chave] = {"modis": [], "viirs": []}
        agrupamento[chave]["viirs"].append(foco)

    resultados_harmonizados: List[Dict[str, Any]] = []

    for (ano, mes, semana, cel_lat, cel_lon), grupos in agrupamento.items():
        lista_modis = grupos["modis"]
        lista_viirs = grupos["viirs"]

        n_modis = len(lista_modis)
        n_viirs = len(lista_viirs)

        frp_modis = sum(f["frp_mw"] for f in lista_modis)
        frp_viirs = sum(f["frp_mw"] for f in lista_viirs)

        frp_harmonizado = round(frp_modis + frp_viirs, 2)

        if ano >= 2012:
            era = "SOBREPOSICAO_MODIS_VIIRS"
            fator_viirs = FATOR_ESCALA_VIIRS_MODIS
            if n_modis > 0 and n_viirs > 0:
                n_harmonizado = round(n_modis + (fator_viirs * n_viirs), 2)
            elif n_modis > 0:
                n_harmonizado = float(n_modis)
            else:
                n_harmonizado = round(fator_viirs * n_viirs, 2)
        else:
            era = "HISTORICO_MODIS_EXCLUSIVO"
            fator_viirs = 0.0
            n_harmonizado = float(n_modis)

        confiancas = [f["confianca"] for f in lista_modis + lista_viirs]
        conf_media = round(sum(confiancas) / len(confiancas), 2) if confiancas else 0.5

        registro_harm = {
            "ano": ano,
            "mes": mes,
            "semana": semana,
            "celula_lat": cel_lat,
            "celula_lon": cel_lon,
            "focos_harmonizados": n_harmonizado,
            "focos_modis": n_modis,
            "focos_viirs": n_viirs,
            "frp_harmonizado_mw": frp_harmonizado,
            "frp_modis_mw": round(frp_modis, 2),
            "frp_viirs_mw": round(frp_viirs, 2),
            "confianca_media": conf_media,
            "era": era,
            "fator_escala_viirs": fator_viirs,
            "total_registros_brutos": n_modis + n_viirs,
        }
        resultados_harmonizados.append(registro_harm)

    # Ordena por ano, semana, latitude, longitude
    resultados_harmonizados.sort(key=lambda r: (r["ano"], r["semana"], r["celula_lat"], r["celula_lon"]))
    return resultados_harmonizados
