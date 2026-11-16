"""Harmonização MODIS + VIIRS e motor do Fire Activity Calendar (task-agente-01/02/04). Offline, sem chaves."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from app import cli
from app.data import calendario as cal
from app.data import harmonizacao as hz

AMOSTRAS = Path(__file__).resolve().parents[1] / "data" / "samples_firms"
MODIS_CSV = AMOSTRAS / "modis_sample_c6.csv"
VIIRS_CSV = AMOSTRAS / "viirs_sample_375m.csv"


@pytest.fixture(scope="module")
def modis():
    return hz.carregar_e_padronizar_focos(MODIS_CSV, "MODIS")


@pytest.fixture(scope="module")
def viirs():
    return hz.carregar_e_padronizar_focos(VIIRS_CSV, "VIIRS")


def foco(sensor, lat, lon, dia="2024-09-15", frp=10.0, conf="nominal"):
    linha = {"latitude": str(lat), "longitude": str(lon), "acq_date": dia, "acq_time": "1330",
             "satellite": "N" if sensor == "VIIRS" else "A", "confidence": conf if sensor == "VIIRS" else "80",
             "frp": str(frp), "daynight": "D"}
    return hz.padronizar_registro(linha, sensor)


# ----------------------------------------------------------------------------- leitura e padronização

def test_leitura_dos_csvs_de_amostra(modis, viirs):
    assert len(modis) == 10 and len(viirs) == 21
    campos = {"id", "sensor", "satelite", "lat", "lon", "data_hora_utc", "ano", "mes", "semana", "dia_noite",
              "confianca_pct", "frp_mw"}
    for f in modis + viirs:
        assert campos <= f.keys()
        assert 1 <= f["semana"] <= 52 and 1 <= f["mes"] <= 12
    assert {f["sensor"] for f in modis} == {"MODIS"} and {f["sensor"] for f in viirs} == {"VIIRS"}
    assert {f["satelite"] for f in modis} == {"Aqua"}
    assert {f["satelite"] for f in viirs} == {"Suomi-NPP"}
    primeiro = modis[0]
    assert primeiro["data_hora_utc"].isoformat() == "2024-09-15T13:45:00+00:00"
    assert primeiro["id"] == "MODIS_Aqua_-10.1834_-48.3331_2024-09-15_1345"
    assert any(f["dia_noite"] == "N" for f in modis)


def test_mapeamento_de_confianca(modis, viirs):
    assert hz.mapear_confianca("low", "VIIRS") == 30.0
    assert hz.mapear_confianca("nominal", "VIIRS") == 65.0
    assert hz.mapear_confianca("HIGH", "VIIRS") == 90.0
    assert hz.mapear_confianca("85", "MODIS") == 85.0
    assert hz.mapear_confianca("150", "MODIS") == 100.0
    assert {f["confianca_pct"] for f in viirs} == {30.0, 65.0, 90.0}
    with pytest.raises(hz.ErroHarmonizacao):
        hz.mapear_confianca("talvez", "VIIRS")


def test_filtro_de_confianca_minima():
    viirs = hz.carregar_e_padronizar_focos(VIIRS_CSV, "VIIRS", confianca_minima=31)
    assert len(viirs) == 20   # só uma detecção "low" na amostra


def test_satelites_noaa_e_terra():
    assert hz._nome_satelite("1", "VIIRS") == "NOAA-20"
    assert hz._nome_satelite("N21", "VIIRS") == "NOAA-21"
    assert hz._nome_satelite("T", "MODIS") == "Terra"


def test_csv_sem_colunas_obrigatorias(tmp_path):
    ruim = tmp_path / "ruim.csv"
    ruim.write_text("latitude,longitude\n-10,-48\n", encoding="utf-8")
    with pytest.raises(hz.ErroHarmonizacao, match="colunas ausentes"):
        hz.carregar_e_padronizar_focos(ruim, "MODIS")
    with pytest.raises(hz.ErroHarmonizacao):
        hz.carregar_e_padronizar_focos(MODIS_CSV, "GOES")


# ----------------------------------------------------------------------------- grade

def test_celula_de_grade_sem_ruido_de_float():
    assert hz.obter_celula_grade(-10.1834, -48.3331) == (-10.2, -48.3)
    assert hz.obter_celula_grade(-10.25, -48.21) in {(-10.2, -48.2), (-10.3, -48.2)}
    assert hz.obter_celula_grade(0.04, 0.06) == (0.0, 0.1)
    lat, lon = hz.obter_celula_grade(-12.0510, -48.5601)
    assert repr(lat) == "-12.1" and repr(lon) == "-48.6"


def test_agregar_em_grade(modis, viirs):
    grade = hz.agregar_em_grade(modis + viirs)
    assert sum(c["n_modis"] for c in grade.values()) == 10
    assert sum(c["n_viirs"] for c in grade.values()) == 21
    c = grade[(-10.2, -48.3)]
    assert (c["n_modis"], c["n_viirs"]) == (3, 7)
    total_frp = sum(f["frp_mw"] for f in modis + viirs)
    assert sum(c["frp_modis_mw"] + c["frp_viirs_mw"] for c in grade.values()) == pytest.approx(total_frp)


# ----------------------------------------------------------------------------- equivalência e FRP

def test_formula_de_contagem_harmonizada():
    assert hz.contagem_harmonizada(10, 30, 2024) == pytest.approx(19.0)
    assert hz.contagem_harmonizada(10, 30, 2011) == 10.0         # antes do VIIRS só conta MODIS
    # Média ponderada MODIS-equivalente (ACHADOS-PARA-AGENTES.md): ½ (10 + 0.252 * 30) = 8.78
    assert hz.contagem_harmonizada(10, 30, 2024, metodo="modis_equivalente") == pytest.approx(8.78, abs=0.01)
    assert hz.contagem_harmonizada(10, 30, 2011, metodo="modis_equivalente") == 10.0
    assert hz.frp_harmonizado(100.0, 50.0, 2024) == 150.0
    assert hz.frp_harmonizado(100.0, 50.0, 2005) == 100.0


def test_harmonizacao_nao_soma_contagens_brutas(modis, viirs):
    harm = hz.harmonizar_series(modis, viirs)
    assert len(harm) == 9
    total = sum(r["focos_harmonizados"] for r in harm)
    assert total == pytest.approx(10 + 0.30 * 21)
    assert total < len(modis) + len(viirs)
    for r in harm:
        assert r["focos_harmonizados"] == pytest.approx(r["n_modis"] + 0.30 * r["n_viirs"])


def test_conservacao_de_frp(modis, viirs):
    harm = hz.harmonizar_series(modis, viirs)
    frp_m = sum(f["frp_mw"] for f in modis)
    frp_v = sum(f["frp_mw"] for f in viirs)
    assert sum(r["frp_total_mw"] for r in harm) == pytest.approx(frp_m + frp_v)
    assert sum(r["frp_modis_mw"] for r in harm) == pytest.approx(frp_m)
    assert sum(r["frp_viirs_mw"] for r in harm) == pytest.approx(frp_v)


def test_harmonizacao_independe_da_granularidade(modis, viirs):
    dia = hz.resumo_harmonizacao(hz.harmonizar_series(modis, viirs, periodo="dia"))
    mes = hz.resumo_harmonizacao(hz.harmonizar_series(modis, viirs, periodo="mes"))
    assert dia["focos_harmonizados"] == pytest.approx(mes["focos_harmonizados"])
    assert dia["frp_total_mw"] == pytest.approx(mes["frp_total_mw"])
    assert mes["registros"] <= dia["registros"]


def test_viirs_antes_de_2012_e_ignorado():
    m = [foco("MODIS", -10.0, -48.0, "2010-08-01", frp=30)]
    v = [foco("VIIRS", -10.0, -48.0, "2010-08-01", frp=12)]
    (r,) = hz.harmonizar_series(m, v)
    assert (r["n_modis"], r["n_viirs"], r["focos_harmonizados"], r["frp_total_mw"]) == (1, 0, 1.0, 30.0)


def test_listas_trocadas_sao_rejeitadas(modis, viirs):
    with pytest.raises(hz.ErroHarmonizacao):
        hz.harmonizar_series(viirs, modis)


def test_exportar_harmonizacao_csv_e_json(tmp_path, modis, viirs):
    harm = hz.harmonizar_series(modis, viirs)
    csv_path = hz.exportar_harmonizacao(harm, tmp_path / "h.csv")
    assert csv_path.read_text(encoding="utf-8").count("\n") == len(harm) + 1
    dados = json.loads(hz.exportar_harmonizacao(harm, tmp_path / "h.json").read_text(encoding="utf-8"))
    assert dados["resumo"]["registros"] == len(harm)


# ----------------------------------------------------------------------------- calendário e anomalias

def test_estatisticas_robustas():
    assert cal.mediana([3, 1, 2]) == 2 and cal.mediana([1, 2, 3, 4]) == 2.5 and cal.mediana([]) == 0.0
    assert cal.percentil([1, 2, 3, 4, 5], 50) == 3
    assert cal.percentil([0, 10], 95) == pytest.approx(9.5)
    assert cal.sigma_robusto([1, 2, 3, 4, 100], 3) == pytest.approx(1.4826)
    assert cal.sigma_robusto([5, 5, 5], 5) == 1.0


def _serie_estavel(anomalia_ano=2024, anomalia_mes=9, valor_anomalo=60):
    """10 focos MODIS por mês, 2000-2025; um mês anômalo."""
    serie = []
    for ano in range(2000, 2026):
        for mes in range(1, 13):
            n = valor_anomalo if (ano, mes) == (anomalia_ano, anomalia_mes) else 10 + (ano % 3)
            serie.append({"ano": ano, "mes": mes, "semana": date(ano, mes, 15).isocalendar()[1],
                          "n_modis": n, "n_viirs": 0, "frp_modis_mw": n * 30.0, "frp_viirs_mw": 0.0})
    return serie


def test_deteccao_de_periodo_anomalo():
    dados = cal.construir_matriz_temporal(_serie_estavel(), ano_inicio=2000, ano_fim=2025,
                                          data_corte=date(2025, 12, 31))
    assert len(dados["matriz"]) == 26 * 12
    cel = next(c for c in dados["matriz"] if (c["ano"], c["mes"]) == (2024, 9))
    assert cel["status"] == "CRITICO" and cel["z_score"] >= 2.0
    assert cel["desvio_percentual"] > 300
    assert cel["alerta"].startswith("Extreme thermal anomaly")
    normal = next(c for c in dados["matriz"] if (c["ano"], c["mes"]) == (2015, 9))
    assert normal["status"] == "NORMAL" and normal["alerta"] == ""
    assert dados["resumo_status"]["CRITICO"] == 1


def test_status_atencao_e_limiares():
    assert cal.classificar(1.5, 10, 100) == "ATENCAO"
    assert cal.classificar(0.5, 10, 100) == "NORMAL"
    assert cal.classificar(2.0, 10, 100) == "CRITICO"
    assert cal.classificar(0.5, 101, 100) == "CRITICO"     # acima do P95 da base
    assert cal.classificar(0.0, 0, 0) == "NORMAL"


def test_baseline_exclui_o_proprio_ano():
    dados = cal.construir_matriz_temporal(_serie_estavel(), ano_inicio=2000, ano_fim=2025,
                                          data_corte=date(2025, 12, 31))
    cel = next(c for c in dados["matriz"] if (c["ano"], c["mes"]) == (2024, 9))
    assert cel["mediana_historica"] < 15


def test_periodos_futuros_ficam_sem_dados():
    dados = cal.construir_matriz_temporal(_serie_estavel(), ano_inicio=2024, ano_fim=2026,
                                          data_corte=date(2026, 6, 10))
    futuros = [c for c in dados["matriz"] if c["status"] == "SEM_DADOS"]
    assert {(c["ano"], c["mes"]) for c in futuros} == {(2026, m) for m in range(7, 13)}
    assert all(c["focos_harmonizados"] is None and c["z_score"] is None for c in futuros)


def test_matriz_semanal_tem_52_colunas():
    dados = cal.construir_matriz_temporal(_serie_estavel(), ano_inicio=2020, ano_fim=2021, periodo="semana",
                                          data_corte=date(2030, 1, 1))
    assert len(dados["matriz"]) == 2 * 52
    assert {c["semana"] for c in dados["matriz"]} == set(range(1, 53))


def test_contrato_json_e_exportacao(tmp_path):
    destino = tmp_path / "dados_calendario.json"
    dados = cal.gerar_calendario_amostra(data_corte=date(2026, 11, 15), caminho_saida=destino)
    lido = json.loads(destino.read_text(encoding="utf-8"))
    for chave in ("regiao", "nome_exibicao", "ano_inicio", "ano_fim", "gerado_em_utc", "matriz", "amostra"):
        assert chave in lido
    assert lido["amostra"] is True and "SYNTHETIC" in lido["fonte_dados"]
    assert (lido["ano_inicio"], lido["ano_fim"]) == (2000, 2026)
    campos = {"ano", "mes", "semana", "focos_harmonizados", "focos_modis_bruto", "focos_viirs_bruto",
              "frp_total_mw", "mediana_historica", "desvio_percentual", "z_score", "status", "alerta"}
    assert all(campos <= c.keys() for c in lido["matriz"])
    assert {c["status"] for c in lido["matriz"]} <= set(cal.STATUS)
    assert dados["resumo_status"]["CRITICO"] > 0
    # antes de 2012 não há VIIRS na série
    assert all(c["focos_viirs_bruto"] == 0 for c in lido["matriz"] if c["ano"] < 2012)


def test_serie_sintetica_e_deterministica():
    a = cal.gerar_serie_sintetica(2010, 2012, data_corte=date(2013, 1, 1))
    b = cal.gerar_serie_sintetica(2010, 2012, data_corte=date(2013, 1, 1))
    assert a == b


def test_json_do_frontend_esta_no_contrato():
    caminho = cal.SAIDA_FRONTEND
    assert caminho.exists(), "rode: python -m app.cli --sample --calendario"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados["amostra"] is True
    assert len(dados["matriz"]) == 27 * 12 and len(dados["matriz_semanal"]) == 27 * 52


# ----------------------------------------------------------------------------- CLI

def test_cli_calendario_sample(tmp_path, capsys):
    destino = tmp_path / "cal.json"
    assert cli.main(["--sample", "--calendario", "--json", str(destino)]) == 0
    out = capsys.readouterr().out
    assert "N_harm = 16.3" in out and "AMOSTRA" in out
    assert json.loads(destino.read_text(encoding="utf-8"))["matriz"]


def test_cli_harmonizar(tmp_path, capsys):
    assert cli.main(["--sample", "--harmonizar", "--saida", str(tmp_path)]) == 0
    assert (tmp_path / "harmonizacao" / "focos_harmonizados.csv").exists()


def test_cli_calendario_com_csvs_explicitos(tmp_path, capsys):
    destino = tmp_path / "real.json"
    assert cli.main(["calendario", "--modis", str(MODIS_CSV), "--viirs", str(VIIRS_CSV), "--json", str(destino),
                     "--ano-inicio", "2020", "--ano-fim", "2024"]) == 0
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["amostra"] is False
    set24 = next(c for c in dados["matriz"] if (c["ano"], c["mes"]) == (2024, 9))
    assert set24["focos_harmonizados"] == pytest.approx(16.3)


def test_cli_cenario_inexistente(capsys):
    assert cli.main(["--sample", "--cenario", "nao-existe"]) == 2
    assert "não encontrado" in capsys.readouterr().err
