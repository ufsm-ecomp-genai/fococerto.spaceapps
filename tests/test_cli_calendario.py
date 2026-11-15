"""Testes da CLI de harmonização e Fire Activity Calendar (task A-07): --harmonizar, --calendario, subcomando."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from app import cli, cli_calendario

RAIZ = Path(__file__).resolve().parent.parent


def rodar(capsys, *argv) -> tuple[int, str]:
    rc = cli.main(list(argv))
    return rc, capsys.readouterr().out


def test_deve_tratar_nao_captura_comandos_existentes():
    assert cli_calendario.deve_tratar(["--sample", "--calendario"])
    assert cli_calendario.deve_tratar(["--sample", "--harmonizar"])
    assert cli_calendario.deve_tratar(["calendario", "--sample"])
    assert not cli_calendario.deve_tratar(["--sample", "--cenario", "tocantins-escasso"])
    assert not cli_calendario.deve_tratar(["run", "--sample", "--regiao", "tocantins"])
    assert not cli_calendario.deve_tratar(["nota", "--regiao", "tocantins", "--calendario"])
    assert not cli_calendario.deve_tratar([])


def test_harmonizar_imprime_formula(capsys):
    rc, out = rodar(capsys, "--sample", "--harmonizar")
    assert rc == 0
    assert "MODIS detections (N_MODIS)       : 10" in out
    assert "VIIRS detections (N_VIIRS)       : 21" in out
    # N_harm = 10 + 0.30 * 21 = 16.30, nunca a soma ingênua 31
    assert "Harmonized count N_harm          : 16.30" in out
    assert "FRP harmonized (sum)             : 670.90 MW" in out  # 338.30 + 332.60
    assert "0.1 deg grid cells with fire" in out


def test_estatisticas_conservam_frp_e_contagem():
    args = cli_calendario.montar_parser().parse_args(["--sample"])
    modis, viirs, harm = cli_calendario.carregar_e_harmonizar(args)
    e = cli_calendario.estatisticas(modis, viirs, harm)
    assert e["frp_harmonizado"] == pytest.approx(e["frp_modis"] + e["frp_viirs"], abs=0.01)
    assert e["n_harmonizado"] == pytest.approx(e["n_modis"] + 0.30 * e["n_viirs"], abs=0.01)
    assert e["celulas"] >= 1


@pytest.mark.parametrize("extra", [[], ["--regiao", "tocantins"]])
def test_calendario_tabela_e_aviso_sintetico(capsys, extra):
    rc, out = rodar(capsys, "--sample", "--calendario", *extra)
    assert rc == 0
    linhas_ano = [l for l in out.splitlines() if l[:4].isdigit() and l[4:7] == " | "]
    assert [int(l[:4]) for l in linhas_ano] == list(range(2026, 1999, -1))
    assert "Jan  Feb  Mar" in out and "Legend:" in out and "Status: most anomalous month" in out
    assert "SYNTHETIC / ILLUSTRATIVE" in out and "estimar_linha_base_sazonal_cerrado" in out
    assert "python3 -m app.cli --sample --cenario tocantins-escasso" in out
    # nada de resultado de despacho inventado na saída do calendário
    assert "Brigades Assigned" not in out
    # a célula vinda da amostra FIRMS fica marcada
    assert "*" in next(l for l in linhas_ano if l.startswith("2024"))


def test_calendario_subcomando_e_json_mesmo_schema(capsys, tmp_path):
    saida = tmp_path / "cal.json"
    rc, out = rodar(capsys, "calendario", "--sample", "--json-saida", str(saida))
    assert rc == 0 and "FIRE ACTIVITY CALENDAR" in out
    novo = json.loads(saida.read_text(encoding="utf-8"))
    ref = RAIZ / "web/app/src/assets/dados_calendario.json"
    if ref.exists():
        antigo = json.loads(ref.read_text(encoding="utf-8"))
        assert novo.keys() == antigo.keys()
        assert novo["matriz"][0].keys() == antigo["matriz"][0].keys()
    assert novo["total_periodos"] == 27 * 12


def test_regiao_sem_amostra_falha_com_erro(capsys):
    rc = cli.main(["--sample", "--calendario", "--regiao", "amazonia"])
    assert rc == 2
    assert "no FIRMS sample" in capsys.readouterr().err


def test_cenario_vira_recursos():
    """--cenario X é atalho para --recursos cenarios/X.yaml (comando do CLAUDE.md/README)."""
    args = cli.montar_parser().parse_args(["run", "--sample", "--cenario", "tocantins-escasso"])
    assert args.cenario == "tocantins-escasso" and args.recursos is None


def test_calendario_subprocess_rapido():
    """Forma exata prometida aos jurados, como processo separado; meta < 5 s."""
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, "-m", "app.cli", "--sample", "--calendario"], cwd=RAIZ,
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    assert "FIRE ACTIVITY CALENDAR" in r.stdout
    assert time.perf_counter() - t0 < 5.0
