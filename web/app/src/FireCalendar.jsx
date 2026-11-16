// Fire Activity Calendar (task-agente-03): matriz ano x mês/semana da atividade de fogo harmonizada MODIS + VIIRS.
// Dados: src/assets/dados_calendario.json, gerado por `python -m app.data.calendario` (app/data/calendario.py).
// Cores: escala sequencial amarelo -> laranja -> vermelho escuro (intensidade, escala log) e magenta para CRITICO.
import { useMemo, useState } from 'react';
import { CalendarDays, Download, Flame, X, AlertTriangle } from 'lucide-react';
import dadosPadrao from './assets/dados_calendario.json';
import './fireCalendar.css';

const MESES = {
  'pt-BR': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
  en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
};

const TXT = {
  'pt-BR': {
    titulo: 'Calendário de atividade de fogo',
    sub: 'Focos harmonizados MODIS (1 km) + VIIRS (375 m) em grade de 0,1°, comparados à mediana histórica do mesmo período.',
    mes: 'Meses',
    semana: 'Semanas',
    csv: 'Baixar CSV',
    amostra: 'DADOS DE AMOSTRA',
    focos: 'Focos harmonizados',
    modis: 'MODIS bruto',
    viirs: 'VIIRS bruto',
    frp: 'FRP total',
    mediana: 'Mediana histórica',
    desvio: 'Desvio da mediana',
    z: 'Z_fire',
    p95: 'P90 / P95 da base',
    status: 'Status',
    plano: 'Gerar Plano Tático de Resposta (FocoCerto AI)',
    planoDica: 'Disponível para períodos CRÍTICOS.',
    fechar: 'Fechar',
    serie: 'Mesmo período em todos os anos',
    semDados: 'sem dados',
    escolha: 'Clique em uma célula para comparar com a mediana histórica.',
    legenda: 'Intensidade (focos harmonizados, escala log)',
    acima: 'acima da mediana',
    abaixo: 'abaixo da mediana',
    medZero: 'mediana histórica é zero',
    NORMAL: 'Normal',
    ATENCAO: 'Atenção',
    CRITICO: 'Crítico',
    SEM_DADOS: 'Sem dados',
    ano: 'Ano',
  },
  en: {
    titulo: 'Fire Activity Calendar',
    sub: 'Harmonized MODIS (1 km) + VIIRS (375 m) hot spots on a 0.1° grid, compared with the historical median for the same period.',
    mes: 'Months',
    semana: 'Weeks',
    csv: 'Download CSV',
    amostra: 'SAMPLE DATA',
    focos: 'Harmonized hot spots',
    modis: 'MODIS raw',
    viirs: 'VIIRS raw',
    frp: 'Total FRP',
    mediana: 'Historical median',
    desvio: 'Deviation from median',
    z: 'Z_fire',
    p95: 'Baseline P90 / P95',
    status: 'Status',
    plano: 'Generate Tactical Response Plan (FocoCerto AI)',
    planoDica: 'Available for CRITICAL periods.',
    fechar: 'Close',
    serie: 'Same period across all years',
    semDados: 'no data',
    escolha: 'Click a cell to compare it with the historical median.',
    legenda: 'Intensity (harmonized hot spots, log scale)',
    acima: 'above median',
    abaixo: 'below median',
    medZero: 'historical median is zero',
    NORMAL: 'Normal',
    ATENCAO: 'Watch',
    CRITICO: 'Critical',
    SEM_DADOS: 'No data',
    ano: 'Year',
  },
};

// YlOrRd (ColorBrewer, seguro para daltonismo) para intensidade; magenta para anomalia crítica.
const RAMPA = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026'];
export const COR_CRITICO = '#c51b8a';

export function corIntensidade(valor, maximo) {
  if (valor == null) return null;
  if (!maximo || valor <= 0) return RAMPA[0];
  const f = Math.log1p(valor) / Math.log1p(maximo);
  return RAMPA[Math.min(RAMPA.length - 1, Math.max(0, Math.round(f * (RAMPA.length - 1))))];
}

const fmt = (v, d = 0, locale = 'en') =>
  v == null ? '—' : Number(v).toLocaleString(locale, { minimumFractionDigits: d, maximumFractionDigits: d });

export function matrizParaCsv(matriz) {
  const cols = [
    'ano',
    'mes',
    'semana',
    'focos_harmonizados',
    'focos_modis_bruto',
    'focos_viirs_bruto',
    'frp_total_mw',
    'mediana_historica',
    'p90',
    'p95',
    'desvio_percentual',
    'z_score',
    'status',
    'alerta',
  ];
  const esc = (v) => {
    const s = v == null ? '' : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [cols.join(','), ...matriz.map((c) => cols.map((k) => esc(c[k])).join(','))].join('\n');
}

function baixarCsv(nome, texto) {
  const url = URL.createObjectURL(new Blob([texto], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = nome;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// Fallback mínimo, caso o JSON não tenha sido gerado: 1 ano vazio, marcado como amostra.
const MOCK = {
  regiao: 'demo',
  nome_exibicao: 'Demo',
  ano_inicio: 2024,
  ano_fim: 2024,
  amostra: true,
  fonte_dados: 'Fallback mock: run `python -m app.data.calendario` to generate dados_calendario.json.',
  matriz: Array.from({ length: 12 }, (_, i) => ({ ano: 2024, mes: i + 1, semana: null, status: 'SEM_DADOS' })),
};

export default function FireCalendar({ dados = dadosPadrao, locale = 'pt-BR', onGeneratePlan }) {
  const lang = locale?.startsWith('en') ? 'en' : 'pt-BR';
  const tx = TXT[lang];
  const base = dados?.matriz?.length ? dados : MOCK;
  const temSemanal = Boolean(base.matriz_semanal?.length);
  const [granularidade, setGranularidade] = useState('mes');
  const [hover, setHover] = useState(null);
  const [sel, setSel] = useState(null);

  const matriz = granularidade === 'semana' && temSemanal ? base.matriz_semanal : base.matriz;
  const nCols = granularidade === 'semana' && temSemanal ? 52 : 12;
  const colDe = (c) => (granularidade === 'semana' && temSemanal ? c.semana : c.mes);

  const { anos, porChave, maximo } = useMemo(() => {
    const porChave = new Map();
    let maximo = 0;
    const anosSet = new Set();
    for (const c of matriz) {
      porChave.set(`${c.ano}-${colDe(c)}`, c);
      anosSet.add(c.ano);
      if (c.focos_harmonizados > maximo) maximo = c.focos_harmonizados;
    }
    return { anos: [...anosSet].sort((a, b) => b - a), porChave, maximo };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [matriz]);

  const rotuloCol = (i) => (nCols === 12 ? MESES[lang][i - 1] : `W${String(i).padStart(2, '0')}`);
  const rotulo = (c) => `${rotuloCol(colDe(c))} ${c.ano}`;
  const desvioTxt = (c) =>
    c.desvio_percentual == null
      ? c.mediana_historica === 0 && c.focos_harmonizados > 0
        ? tx.medZero
        : '—'
      : `${c.desvio_percentual > 0 ? '+' : ''}${fmt(c.desvio_percentual, 0, lang)}% ${c.desvio_percentual >= 0 ? tx.acima : tx.abaixo}`;

  const serieSel = sel
    ? anos
        .slice()
        .reverse()
        .map((a) => porChave.get(`${a}-${colDe(sel)}`))
        .filter(Boolean)
    : [];
  const maxSerie = Math.max(1, ...serieSel.map((c) => c.focos_harmonizados || 0));

  return (
    <section className="panel fire-calendar">
      <div className="panel-heading fc-heading">
        <div>
          <h2>
            <CalendarDays size={18} /> {tx.titulo} — {base.nome_exibicao}
          </h2>
          <p className="fc-sub">{tx.sub}</p>
        </div>
        <div className="fc-actions">
          {temSemanal && (
            <div className="fc-toggle" role="group" aria-label="granularity">
              {['mes', 'semana'].map((g) => (
                <button
                  key={g}
                  className={granularidade === g ? 'active' : ''}
                  aria-pressed={granularidade === g}
                  onClick={() => {
                    setGranularidade(g);
                    setSel(null);
                  }}
                >
                  {tx[g]}
                </button>
              ))}
            </div>
          )}
          <button
            className="secondary"
            onClick={() => baixarCsv(`fire_calendar_${base.regiao}_${granularidade}.csv`, matrizParaCsv(matriz))}
          >
            <Download size={15} /> {tx.csv}
          </button>
        </div>
      </div>

      {base.amostra && (
        <div className="fc-sample" role="note">
          <AlertTriangle size={15} /> <strong>{tx.amostra}</strong> {base.fonte_dados}
        </div>
      )}

      <div className="fc-body">
        <div className="fc-grid-wrap">
          <div
            className={`fc-grid ${nCols === 52 ? 'weekly' : 'monthly'}`}
            style={{ gridTemplateColumns: `3.2em repeat(${nCols}, minmax(${nCols === 52 ? 9 : 22}px, 1fr))` }}
            role="grid"
            aria-label={tx.titulo}
            onMouseLeave={() => setHover(null)}
          >
            <div className="fc-corner" role="columnheader">
              {tx.ano}
            </div>
            {Array.from({ length: nCols }, (_, i) => (
              <div key={i} className="fc-colhead" role="columnheader">
                {nCols === 12 || (i + 1) % 4 === 1 ? rotuloCol(i + 1) : ''}
              </div>
            ))}
            {anos.map((ano) => (
              <div className="fc-row" role="row" key={ano} style={{ display: 'contents' }}>
                <div className="fc-rowhead" role="rowheader">
                  {ano}
                </div>
                {Array.from({ length: nCols }, (_, i) => {
                  const c = porChave.get(`${ano}-${i + 1}`);
                  if (!c || c.status === 'SEM_DADOS')
                    return <div key={i} className="fc-cell empty" role="gridcell" aria-label={tx.semDados} />;
                  const critico = c.status === 'CRITICO';
                  const ativo = sel && sel.ano === c.ano && colDe(sel) === colDe(c);
                  return (
                    <button
                      key={i}
                      role="gridcell"
                      className={`fc-cell ${c.status.toLowerCase()} ${ativo ? 'selected' : ''}`}
                      style={{ background: critico ? COR_CRITICO : corIntensidade(c.focos_harmonizados, maximo) }}
                      aria-label={`${rotulo(c)}: ${fmt(c.focos_harmonizados, 1, lang)} — ${tx[c.status]}`}
                      onMouseEnter={(e) => setHover({ c, x: e.clientX, y: e.clientY })}
                      onMouseMove={(e) => setHover({ c, x: e.clientX, y: e.clientY })}
                      onFocus={(e) => {
                        const r = e.currentTarget.getBoundingClientRect();
                        setHover({ c, x: r.right, y: r.bottom });
                      }}
                      onBlur={() => setHover(null)}
                      onClick={() => setSel(ativo ? null : c)}
                    />
                  );
                })}
              </div>
            ))}
          </div>

          <div className="fc-legend" aria-label={tx.legenda}>
            <span>{tx.legenda}:</span>
            <span className="fc-ramp">
              {RAMPA.map((cor) => (
                <i key={cor} style={{ background: cor }} />
              ))}
            </span>
            <span>0 → {fmt(maximo, 0, lang)}</span>
            <span className="fc-key">
              <i className="fc-swatch atencao" /> {tx.ATENCAO}
            </span>
            <span className="fc-key">
              <i className="fc-swatch" style={{ background: COR_CRITICO }} /> {tx.CRITICO}
            </span>
            <span className="fc-key">
              <i className="fc-swatch empty" /> {tx.SEM_DADOS}
            </span>
          </div>
        </div>

        <aside className={`fc-side ${sel ? 'open' : ''}`} aria-live="polite">
          {!sel && <p className="fc-hint">{tx.escolha}</p>}
          {sel && (
            <>
              <div className="fc-side-head">
                <h3>{rotulo(sel)}</h3>
                <span className={`fc-status ${sel.status.toLowerCase()}`}>{tx[sel.status]}</span>
                <button className="fc-close" aria-label={tx.fechar} onClick={() => setSel(null)}>
                  <X size={16} />
                </button>
              </div>
              <p className="fc-big">
                {desvioTxt(sel)}
                {sel.z_score != null && <small> (Z = {fmt(sel.z_score, 2, lang)})</small>}
              </p>
              <dl className="fc-dl">
                <dt>{tx.focos}</dt>
                <dd>{fmt(sel.focos_harmonizados, 1, lang)}</dd>
                <dt>{tx.mediana}</dt>
                <dd>{fmt(sel.mediana_historica, 1, lang)}</dd>
                <dt>{tx.p95}</dt>
                <dd>
                  {fmt(sel.p90, 1, lang)} / {fmt(sel.p95, 1, lang)}
                </dd>
                <dt>{tx.modis}</dt>
                <dd>{fmt(sel.focos_modis_bruto, 0, lang)}</dd>
                <dt>{tx.viirs}</dt>
                <dd>{fmt(sel.focos_viirs_bruto, 0, lang)}</dd>
                <dt>{tx.frp}</dt>
                <dd>{fmt(sel.frp_total_mw, 0, lang)} MW</dd>
              </dl>
              {sel.alerta && <p className="fc-alert">{sel.alerta}</p>}
              <h4>{tx.serie}</h4>
              <div className="fc-bars" role="img" aria-label={tx.serie}>
                {serieSel.map((c) => (
                  <div
                    key={c.ano}
                    className={`fc-bar ${c.ano === sel.ano ? 'current' : ''}`}
                    title={`${c.ano}: ${fmt(c.focos_harmonizados, 1, lang)}`}
                    style={{
                      height: `${Math.max(2, ((c.focos_harmonizados || 0) / maxSerie) * 100)}%`,
                      background: c.status === 'CRITICO' ? COR_CRITICO : undefined,
                    }}
                  />
                ))}
                {sel.mediana_historica > 0 && (
                  <div className="fc-median" style={{ bottom: `${(sel.mediana_historica / maxSerie) * 100}%` }} />
                )}
              </div>
              <button
                className="primary fc-plan"
                disabled={sel.status !== 'CRITICO'}
                title={sel.status !== 'CRITICO' ? tx.planoDica : ''}
                onClick={() => onGeneratePlan?.(sel)}
              >
                <Flame size={16} /> {tx.plano}
              </button>
              {sel.status !== 'CRITICO' && <p className="fc-hint">{tx.planoDica}</p>}
            </>
          )}
        </aside>
      </div>

      {hover && (
        <div
          className="fc-tooltip"
          role="tooltip"
          style={{
            left: Math.min(hover.x + 14, (typeof window !== 'undefined' ? window.innerWidth : 1200) - 250),
            top: hover.y + 14,
          }}
        >
          <strong>{rotulo(hover.c)}</strong>
          <span>
            {tx.focos}: {fmt(hover.c.focos_harmonizados, 1, lang)}
          </span>
          <span>
            {tx.frp}: {fmt(hover.c.frp_total_mw, 0, lang)} MW
          </span>
          <span>
            {tx.status}: {tx[hover.c.status]} {hover.c.z_score != null && `(Z ${fmt(hover.c.z_score, 2, lang)})`}
          </span>
        </div>
      )}
    </section>
  );
}
