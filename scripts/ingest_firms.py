"""Ingestão do NASA FIRMS (MODIS C6.1 e VIIRS 375 m) no Postgres. Idempotente (INSERT … ON CONFLICT DO NOTHING).

Cada sensor é baixado para um arquivo próprio em data/raw/ e os focos são consolidados (dedup pelo id, que
inclui o satélite) no Postgres e/ou no --saida-csv. O padrão continua sendo só o VIIRS S-NPP, que é o feed do
motor de despacho: misturar MODIS na tabela `focos` contaria o mesmo incêndio duas vezes. Para a harmonização,
use --sensor todos (ou modis_c6) com --saida-csv.

Uso:
  python scripts/ingest_firms.py --regiao tocantins --janela 7d
  python scripts/ingest_firms.py --regiao tocantins --janela 7d --sensor todos --sem-postgres --saida-csv data/raw/tocantins/focos_todos.csv
  python scripts/ingest_firms.py --sem-postgres --arquivo data/samples_firms/modis_sample_c6.csv data/samples_firms/viirs_sample_375m.csv
  python scripts/ingest_firms.py --regiao tocantins --arquivo data/raw/firms_7d.csv --saida-csv data/raw/tocantins/focos.csv
  python scripts/ingest_firms.py --aplicar-schema            # só cria as tabelas (sql/postgres.sql)
DSN: --dsn ou a variável POSTGRES_DSN (ex.: postgresql://postgres:dev@localhost:55432/postgres).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ingest_comum import RAIZ, RAW, bbox_da_regiao, dsn_postgres

from app.data.fontes import COLUNAS_FOCOS, FIRMS_URLS, JANELAS_FIRMS, baixar, escrever_csv, ler_firms


def aplicar_schema(conn) -> None:
    sql = (RAIZ / "sql" / "postgres.sql").read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def gravar_postgres(focos: list[dict], dsn: str) -> tuple[int, int]:
    """Grava os focos. Devolve (inseridos, já existentes)."""
    import psycopg

    with psycopg.connect(dsn) as conn:
        aplicar_schema(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM focos")
            antes = cur.fetchone()[0]
            cur.executemany(
                "INSERT INTO focos (id, lat, lon, data_hora_utc, satelite, confianca, frp, dia_noite, dia) "
                "VALUES (%(id)s, %(lat)s, %(lon)s, %(data_hora_utc)s, %(satelite)s, %(confianca)s, %(frp)s, "
                "%(dia_noite)s, %(dia)s) ON CONFLICT (id) DO NOTHING",
                focos,
            )
            cur.execute("SELECT count(*) FROM focos")
            depois = cur.fetchone()[0]
        conn.commit()
    return depois - antes, len(focos) - (depois - antes)


def consolidar(arquivos: list[Path], bbox=None) -> list[dict]:
    """Lê vários CSVs do FIRMS (MODIS e/ou VIIRS) e junta os focos, sem repetir ids."""
    vistos: set[str] = set()
    focos = []
    for arquivo in arquivos:
        lidos = ler_firms(arquivo, bbox)
        novos = [f for f in lidos if f["id"] not in vistos]
        vistos.update(f["id"] for f in novos)
        focos.extend(novos)
        print(f"  {arquivo.name}: {len(lidos)} focos")
    return focos


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--regiao", help="nome de config/regioes/<regiao>.yaml (recorta pela bbox)")
    p.add_argument("--janela", choices=JANELAS_FIRMS, default="24h")
    p.add_argument("--sensor", choices=[*FIRMS_URLS, "todos"], default="viirs_snpp",
                   help="feed(s) do FIRMS a baixar (padrão: viirs_snpp, o feed do motor de despacho)")
    p.add_argument("--arquivo", type=Path, nargs="+",
                   help="CSV(s) do FIRMS já baixado(s), MODIS e/ou VIIRS (não baixa nada; ignora --sensor)")
    p.add_argument("--dsn", help="DSN do Postgres (padrão: POSTGRES_DSN)")
    p.add_argument("--saida-csv", type=Path, help="também grava o recorte neste CSV")
    p.add_argument("--sem-postgres", action="store_true", help="não grava no Postgres")
    p.add_argument("--aplicar-schema", action="store_true", help="só cria as tabelas e sai")
    a = p.parse_args(argv)

    dsn = a.dsn or dsn_postgres()
    if a.aplicar_schema:
        import psycopg
        if not dsn:
            sys.exit("Defina POSTGRES_DSN ou passe --dsn")
        with psycopg.connect(dsn) as conn:
            aplicar_schema(conn)
        print("schema aplicado")
        return 0

    arquivos = list(a.arquivo or [])
    if not arquivos:
        sensores = list(FIRMS_URLS) if a.sensor == "todos" else [a.sensor]
        for sensor in sensores:
            url = FIRMS_URLS[sensor].format(janela=a.janela)
            # viirs_snpp mantém o nome antigo (firms_<janela>.csv) para não quebrar quem já o usa
            nome = f"firms_{a.janela}.csv" if sensor == "viirs_snpp" else f"firms_{sensor}_{a.janela}.csv"
            print(f"baixando {url} -> {RAW / nome}")
            arquivos.append(baixar(url, RAW / nome))
    focos = consolidar(arquivos, bbox_da_regiao(a.regiao) if a.regiao else None)
    dias = sorted({f["dia"] for f in focos})
    print(f"focos lidos (recorte {a.regiao or 'global'}, deduplicados): {len(focos)}; dias: {dias[0] if dias else '-'} a {dias[-1] if dias else '-'}")
    if a.saida_csv:
        n = escrever_csv(a.saida_csv, focos, COLUNAS_FOCOS)
        print(f"csv: {a.saida_csv} ({n} linhas)")
    if not a.sem_postgres:
        if not dsn:
            sys.exit("Defina POSTGRES_DSN ou passe --dsn (ou use --sem-postgres)")
        novos, repetidos = gravar_postgres(focos, dsn)
        print(f"postgres: {novos} inseridos, {repetidos} já existiam")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
