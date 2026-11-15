"""Ingestão de múltiplos sensores do FIRMS (task A-06), sempre offline com data/samples_firms/."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))

import ingest_firms  # noqa: E402

from app.data.fontes import FIRMS_URL, FIRMS_URLS, SENSOR_FIRMS  # noqa: E402

AMOSTRAS = RAIZ / "data" / "samples_firms"
MODIS = AMOSTRAS / "modis_sample_c6.csv"
VIIRS = AMOSTRAS / "viirs_sample_375m.csv"


def test_urls_cobrem_modis_e_viirs():
    assert set(FIRMS_URLS) == {"viirs_snpp", "modis_c6", "viirs_noaa20", "viirs_noaa21"}
    assert FIRMS_URL == FIRMS_URLS["viirs_snpp"]
    assert "modis-c6.1" in FIRMS_URLS["modis_c6"]
    assert all("{janela}" in u for u in FIRMS_URLS.values())
    assert SENSOR_FIRMS["modis_c6"] == "MODIS"
    assert {SENSOR_FIRMS[k] for k in FIRMS_URLS if k != "modis_c6"} == {"VIIRS"}


def test_consolidar_junta_modis_e_viirs_sem_repetir():
    focos = ingest_firms.consolidar([MODIS, VIIRS])
    assert len(focos) == 10 + 21
    assert len({f["id"] for f in focos}) == len(focos)
    # passar o mesmo arquivo de novo não duplica
    assert len(ingest_firms.consolidar([MODIS, VIIRS, VIIRS])) == 31


def test_main_offline_grava_csv_consolidado(tmp_path, monkeypatch):
    def sem_rede(*_a, **_k):
        raise AssertionError("não deveria baixar nada com --arquivo")

    monkeypatch.setattr(ingest_firms, "baixar", sem_rede)
    saida = tmp_path / "focos.csv"
    rc = ingest_firms.main(["--sem-postgres", "--sensor", "todos",
                            "--arquivo", str(MODIS), str(VIIRS), "--saida-csv", str(saida)])
    assert rc == 0
    with saida.open(newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 31
    assert {r["satelite"] for r in linhas} == {"A", "N"}


@pytest.mark.parametrize("sensor,esperados", [
    ("viirs_snpp", ["firms_24h.csv"]),
    ("todos", ["firms_24h.csv", "firms_modis_c6_24h.csv", "firms_viirs_noaa20_24h.csv",
               "firms_viirs_noaa21_24h.csv"]),
])
def test_main_baixa_um_arquivo_por_sensor(tmp_path, monkeypatch, sensor, esperados):
    baixados = []

    def falso_baixar(url, destino):
        baixados.append((url, destino.name))
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(VIIRS.read_bytes())
        return destino

    monkeypatch.setattr(ingest_firms, "baixar", falso_baixar)
    monkeypatch.setattr(ingest_firms, "RAW", tmp_path)
    assert ingest_firms.main(["--sem-postgres", "--sensor", sensor]) == 0
    assert [nome for _, nome in baixados] == esperados
    assert all(url.startswith("https://firms.modaps.eosdis.nasa.gov/") for url, _ in baixados)
