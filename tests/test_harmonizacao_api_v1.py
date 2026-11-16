"""
Testes Unitários para os Módulos de Harmonização e Calendário Histórico.
NASA Space Apps Challenge 2026 - ECOMP UFSM.

Testes da primeira versão (main, c6caf88), mantidos depois da junção das duas implementações: garantem que a
API original (normalizar_confianca, celula_lat, focos_modis, era, frp_harmonizado_mw...) continua funcionando.
Ajustes: VIIRS nominal = 0.65 e high = 0.90 (CONTEXT.md §2) e períodos futuros podem ser SEM_DADOS.
"""

from pathlib import Path
import json
import pytest

from app.data.harmonizacao import (
    carregar_e_padronizar_focos,
    normalizar_confianca,
    obter_celula_grade,
    agregar_em_grade,
    harmonizar_series,
    FATOR_ESCALA_VIIRS_MODIS,
)
from app.data.calendario import (
    calcular_percentil,
    calcular_mad,
    construir_matriz_temporal,
    exportar_calendario_json,
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODIS_SAMPLE = BASE_DIR / "data/samples_firms/modis_sample_c6.csv"
VIIRS_SAMPLE = BASE_DIR / "data/samples_firms/viirs_sample_375m.csv"


def test_normalizar_confianca():
    # MODIS numérico
    assert normalizar_confianca("100", "MODIS") == 1.0
    assert normalizar_confianca("50", "MODIS") == 0.5
    assert normalizar_confianca(85, "MODIS") == 0.85
    assert normalizar_confianca(0.75, "MODIS") == 0.75

    # VIIRS categórico
    assert normalizar_confianca("low", "VIIRS") == 0.30
    assert normalizar_confianca("nominal", "VIIRS") == 0.65   # CONTEXT.md §2: nominal = 65 %
    assert normalizar_confianca("high", "VIIRS") == 0.90   # CONTEXT.md §2: high = 90 %


def test_obter_celula_grade():
    lat, lon = -10.1834, -48.3331
    cel_lat, cel_lon = obter_celula_grade(lat, lon, step=0.1)
    assert cel_lat == -10.2
    assert cel_lon == -48.3


def test_carregar_focos_modis():
    focos = carregar_e_padronizar_focos(MODIS_SAMPLE, "MODIS")
    assert len(focos) == 10
    primeiro = focos[0]
    assert primeiro["sensor"] == "MODIS"
    assert primeiro["satelite"] == "Aqua"
    assert primeiro["ano"] == 2024
    assert primeiro["mes"] == 9
    assert 0.0 <= primeiro["confianca"] <= 1.0
    assert primeiro["frp_mw"] > 0


def test_carregar_focos_viirs():
    focos = carregar_e_padronizar_focos(VIIRS_SAMPLE, "VIIRS")
    assert len(focos) == 21
    primeiro = focos[0]
    assert primeiro["sensor"] == "VIIRS"
    assert primeiro["satelite"] == "Suomi-NPP"
    assert primeiro["confianca"] in (0.30, 0.65, 0.90)   # low / nominal / high (CONTEXT.md §2)
    assert primeiro["frp_mw"] > 0


def test_agregar_em_grade():
    modis = carregar_e_padronizar_focos(MODIS_SAMPLE, "MODIS")
    grade = agregar_em_grade(modis, step=0.1)
    assert len(grade) > 0
    total_somado = sum(c["total_focos"] for c in grade.values())
    assert total_somado == len(modis)


def test_harmonizacao_overlap_e_conservacao_frp():
    modis = carregar_e_padronizar_focos(MODIS_SAMPLE, "MODIS")
    viirs = carregar_e_padronizar_focos(VIIRS_SAMPLE, "VIIRS")
    harm = harmonizar_series(modis, viirs, step=0.1)

    assert len(harm) > 0
    for registro in harm:
        assert registro["ano"] == 2024
        assert registro["era"] == "SOBREPOSICAO_MODIS_VIIRS"
        assert registro["fator_escala_viirs"] == FATOR_ESCALA_VIIRS_MODIS
        # Conservação física da energia radiativa total
        assert round(registro["frp_harmonizado_mw"], 1) == round(
            registro["frp_modis_mw"] + registro["frp_viirs_mw"], 1
        )
        # Equivalência de contagem ponderada
        if registro["focos_modis"] > 0 and registro["focos_viirs"] > 0:
            esperado = round(registro["focos_modis"] + 0.30 * registro["focos_viirs"], 2)
            assert registro["focos_harmonizados"] == esperado


def test_harmonizacao_pre_2012():
    foco_antigo = [
        {
            "id": "teste_2005",
            "sensor": "MODIS",
            "satelite": "Terra",
            "lat": -10.2,
            "lon": -48.3,
            "ano": 2005,
            "mes": 8,
            "semana": 33,
            "confianca": 0.8,
            "frp_mw": 50.0,
        }
    ]
    harm = harmonizar_series(foco_antigo, [], step=0.1)
    assert len(harm) == 1
    assert harm[0]["era"] == "HISTORICO_MODIS_EXCLUSIVO"
    assert harm[0]["focos_harmonizados"] == 1.0
    assert harm[0]["fator_escala_viirs"] == 0.0


def test_motor_calendario_e_anomalias():
    modis = carregar_e_padronizar_focos(MODIS_SAMPLE, "MODIS")
    viirs = carregar_e_padronizar_focos(VIIRS_SAMPLE, "VIIRS")
    harm = harmonizar_series(modis, viirs)

    cal = construir_matriz_temporal(harm, ano_inicio=2000, ano_fim=2026)
    assert cal["total_periodos"] == 27 * 12  # 324 meses
    assert cal["ano_inicio"] == 2000
    assert cal["ano_fim"] == 2026
    assert len(cal["matriz"]) == 324

    # Verifica integridade dos campos de cada registro
    for celula in cal["matriz"]:
        assert celula["status"] in ("NORMAL", "ATENCAO", "CRITICO", "SEM_DADOS")   # SEM_DADOS: período ainda não observado
        assert "z_score" in celula
        assert "mediana_historica" in celula
        assert "desvio_percentual" in celula
        assert "alerta" in celula


def test_exportar_calendario_json(tmp_path):
    saida = tmp_path / "teste_calendario.json"
    dados = {"teste": True, "ano": 2026, "matriz": []}
    exportar_calendario_json(dados, saida)
    assert saida.exists()

    with open(saida, "r", encoding="utf-8") as f:
        carregado = json.load(f)
    assert carregado["teste"] is True
    assert carregado["ano"] == 2026
