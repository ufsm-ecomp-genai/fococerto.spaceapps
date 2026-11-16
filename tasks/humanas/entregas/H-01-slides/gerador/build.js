// Gera o deck de 7 slides (H-01) a partir dos resultados reais da análise H-08.
// Uso: node build.js <pasta_analise> <pasta_imagens_worldview> <overview.jpg> <saida.pptx> <dados_extra.json>
const path = require("path");
const fs = require("fs");
const TOOLS = path.join(__dirname, "..", "tools", "node_modules");
const pptxgen = require(path.join(TOOLS, "pptxgenjs"));
const React = require(path.join(TOOLS, "react"));
const ReactDOMServer = require(path.join(TOOLS, "react-dom", "server"));
const sharp = require(path.join(TOOLS, "sharp"));
const fa = require(path.join(TOOLS, "react-icons", "fa"));
const SKILL = process.env.PPTX_SKILL;
const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js"));

const [ANALISE, WV, OVERVIEW, SAIDA, EXTRA] = process.argv.slice(2);
const extra = JSON.parse(fs.readFileSync(EXTRA, "utf8"));
const resumo = JSON.parse(fs.readFileSync(path.join(ANALISE, "resumo.json"), "utf8"));

// --- dados do calendário (série MODIS-equivalente) ---
const linhas = fs.readFileSync(path.join(ANALISE, "calendario_semanal.csv"), "utf8").trim().split(/\r?\n/);
const cab = linhas[0].split(",");
const rows = linhas.slice(1).map((l) => Object.fromEntries(l.split(",").map((v, i) => [cab[i], v])));
const SERIE = extra.serie; // "modis_equivalente" ou "formula_projeto"
const ANO = extra.ano_destaque;
const doAno = rows.filter((r) => +r.ano === ANO).sort((a, b) => a.semana - b.semana);
const semanas = doAno.map((r) => String(r.semana));
const valAno = doAno.map((r) => Math.round(+r[SERIE]));
const valMed = doAno.map((r) => Math.round(+r[`${SERIE}_mediana`]));

const THEME = {
  name: "FocoCerto Night",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0B132B", lt1: "FFFFFF", dk2: "1E293B", lt2: "CBD5E1",
    accent1: "F97316", accent2: "F59E0B", accent3: "E11D48", accent4: "38BDF8",
    accent5: "64748B", accent6: "22C55E", hlink: "F59E0B", folHlink: "FBBF24",
  },
};

async function icone(Comp, cor) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + cor, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9"; // 10 x 5.625
  pres.title = "FocoCerto Harmonizer";
  pres.author = "Team ECOMP-UFSM";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  pres.defineSlideMaster({
    title: "CAPA",
    background: { color: THEME.colors.dk1 },
    objects: [],
  });
  pres.defineSlideMaster({
    title: "CONTEUDO",
    background: { color: THEME.colors.dk1 },
    margin: [0.5, 0.5, 0.5, 0.5],
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9.0, h: 0.75,
          fontSize: 30, bold: true, color: C.background1, valign: "middle", margin: 0 }, text: "" } },
      { text: { text: "Team ECOMP-UFSM · NASA Space Apps Challenge 2026",
          options: { x: 0.5, y: 5.2, w: 6, h: 0.25, fontSize: 9, color: C.accent5, margin: 0 } } },
    ],
    slideNumber: { x: 9.1, y: 5.2, w: 0.4, h: 0.25, fontSize: 9, color: "64748B", align: "right" },
  });

  const ic = {
    sat: await icone(fa.FaSatellite, THEME.colors.dk1),
    grid: await icone(fa.FaThLarge, THEME.colors.dk1),
    cal: await icone(fa.FaCalendarAlt, THEME.colors.dk1),
    crew: await icone(fa.FaTruck, THEME.colors.dk1),
    bolt: await icone(fa.FaBolt, THEME.colors.dk1),
    chart: await icone(fa.FaChartLine, THEME.colors.dk1),
    code: await icone(fa.FaCodeBranch, THEME.colors.dk1),
    globe: await icone(fa.FaGlobeAmericas, THEME.colors.dk1),
    user: await icone(fa.FaUserCheck, THEME.colors.dk1),
  };
  const circulo = (s, x, y, d, img, cor, nome) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: cor }, line: { color: cor }, objectName: nome + "-circ" });
    const p = d * 0.26;
    s.addImage({ data: img, x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: nome + "-icone" });
  };
  const cartao = (s, x, y, w, h, nome) =>
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.text2 },
      line: { color: C.text2 }, objectName: nome });

  // ---------- 1. Capa ----------
  pres.addSection({ title: "Abertura" });
  let s = pres.addSlide({ masterName: "CAPA", sectionTitle: "Abertura" });
  s.addImage({ path: path.join(WV, "worldview_2024-09-15_jalapao_VIIRS.png"), x: 5.6, y: 0, w: 4.4, h: 5.625,
    sizing: { type: "cover", w: 4.4, h: 5.625 }, objectName: "capa-imagem",
    altText: "NASA Worldview, Aqua true color with VIIRS 375 m fire detections, eastern Tocantins, 15 Sep 2024" });
  s.addText("FocoCerto Harmonizer", { x: 0.5, y: 0.55, w: 4.9, h: 1.4, fontSize: 38, bold: true, valign: "bottom",
    color: C.background1, margin: 0, isTextBox: true, objectName: "capa-titulo" });
  s.addText("A fire activity calendar from harmonized MODIS and VIIRS hot spots, linked to crew dispatch",
    { x: 0.5, y: 2.1, w: 4.9, h: 0.75, fontSize: 16, color: C.accent2, margin: 0, isTextBox: true, objectName: "capa-subtitulo" });
  s.addText([
    { text: "Team ECOMP-UFSM", options: { bold: true, color: C.background1, breakLine: true } },
    { text: "Universidade Federal de Santa Maria, Brazil", options: { color: C.background2, breakLine: true } },
    { text: extra.integrantes, options: { color: extra.integrantes.startsWith("[") ? C.accent3 : C.background2 } },
  ], { x: 0.5, y: 3.05, w: 4.9, h: 1.0, fontSize: 14, margin: 0, isTextBox: true, objectName: "capa-equipe", paraSpaceAfter: 3 });
  s.addText("NASA Space Apps Challenge 2026 · Harmonization of MODIS and VIIRS Hot Spots",
    { x: 0.5, y: 4.55, w: 4.9, h: 0.5, fontSize: 11, color: C.accent5, margin: 0, isTextBox: true, objectName: "capa-desafio" });
  s.addText("Imagery: NASA Worldview", { x: 5.7, y: 5.3, w: 4.2, h: 0.25, fontSize: 9, color: C.background1,
    align: "right", margin: 0, isTextBox: true, objectName: "capa-credito" });
  s.addNotes("Team ECOMP-UFSM, FocoCerto Harmonizer. The image is a real fire front in eastern Tocantins on 15 Sep 2024, seen by VIIRS.");

  // ---------- 2. Problema ----------
  pres.addSection({ title: "Problema e solução" });
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Problema e solução" });
  s.addText("One fire, two sensors, two different counts", { placeholder: "title" });
  const lado = 2.85, yImg = 1.3;
  [["MODIS", "1 km pixels", extra.n_modis_caixa, "worldview_2024-09-15_jalapao_zoom_MODIS.png", 0.5],
   ["VIIRS", "375 m pixels", extra.n_viirs_caixa, "worldview_2024-09-15_jalapao_zoom_VIIRS.png", 0.5 + lado + 0.3]]
    .forEach(([nome, pix, n, arq, x]) => {
      s.addImage({ path: path.join(WV, arq), x, y: yImg, w: lado, h: lado, objectName: `prob-${nome}`,
        altText: `${nome} fire detections over Aqua true color, eastern Tocantins, 15 Sep 2024` });
      s.addText([
        { text: nome + " ", options: { bold: true, color: C.background1 } },
        { text: `${pix} · ${n} detections`, options: { color: C.background2 } },
      ], { x, y: yImg + lado + 0.08, w: lado, h: 0.3, fontSize: 13, margin: 0, isTextBox: true, objectName: `prob-${nome}-rotulo` });
    });
  const xr = 0.5 + 2 * lado + 0.6;
  s.addText(`${extra.razao_viirs_modis}×`, { x: xr, y: 1.25, w: 9.5 - xr, h: 0.95, fontSize: 60, bold: true,
    color: C.accent1, margin: 0, isTextBox: true, objectName: "prob-stat" });
  s.addText(`more VIIRS than MODIS detections, Tocantins ${extra.periodo_razao}`,
    { x: xr, y: 2.2, w: 9.5 - xr, h: 0.55, fontSize: 14, color: C.background2, margin: 0, isTextBox: true, objectName: "prob-stat-rotulo" });
  s.addText("MODIS since 2000, VIIRS since 2012. Counted raw, the record jumps at the sensor change, and a normal season looks extreme.",
    { x: xr, y: 2.95, w: 9.5 - xr, h: 1.25, fontSize: 14, color: C.background1, margin: 0, isTextBox: true, objectName: "prob-texto" });
  s.addText("Imagery: NASA Worldview, Aqua true color, 15 Sep 2024, eastern Tocantins (Brazil)",
    { x: xr, y: 4.35, w: 9.5 - xr, h: 0.45, fontSize: 10, color: C.accent5, margin: 0, isTextBox: true, objectName: "prob-credito" });
  s.addNotes("Same place, same day, same smoke plumes. VIIRS draws the fire lines; MODIS sees a few points. That is why raw counts cannot be compared across years.");

  // ---------- 3. Solução ----------
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Problema e solução" });
  s.addText("From space to action", { placeholder: "title" });
  const passos = [
    [ic.sat, "NASA FIRMS", "MODIS and VIIRS active fire detections", C.accent4],
    [ic.grid, "Harmonize", "One grid, one scale, one comparable record", C.accent2],
    [ic.cal, "Fire Activity Calendar", "Is this week unusual for this place?", C.accent1],
    [ic.crew, "Dispatch plan", "Which fires first, which crew, and why", C.accent3],
  ];
  const wc = 1.95, gap = 0.4, x0 = (10 - (4 * wc + 3 * gap)) / 2, yc = 1.55, hc = 2.75;
  passos.forEach(([img, tit, txt, cor], i) => {
    const x = x0 + i * (wc + gap);
    cartao(s, x, yc, wc, hc, `sol-cartao-${i + 1}`);
    circulo(s, x + (wc - 0.8) / 2, yc + 0.3, 0.8, img, cor, `sol-${i + 1}`);
    s.addText(tit, { x: x + 0.15, y: yc + 1.25, w: wc - 0.3, h: 0.45, fontSize: 16, bold: true, color: C.background1,
      align: "center", margin: 0, isTextBox: true, objectName: `sol-titulo-${i + 1}` });
    s.addText(txt, { x: x + 0.15, y: yc + 1.75, w: wc - 0.3, h: 0.8, fontSize: 13, color: C.background2,
      align: "center", margin: 0, isTextBox: true, objectName: `sol-texto-${i + 1}` });
    if (i < 3) s.addText("→", { x: x + wc, y: yc + 0.4, w: gap, h: 0.5, fontSize: 22, bold: true, color: C.accent5,
      align: "center", margin: 0, isTextBox: true, objectName: `sol-seta-${i + 1}` });
  });
  s.addText("A human coordinator approves every dispatch.", { x: 0.5, y: 4.55, w: 9, h: 0.35, fontSize: 14,
    italic: true, color: C.accent2, align: "center", margin: 0, isTextBox: true, objectName: "sol-rodape" });
  s.addNotes("Four steps: data, harmonization, calendar, dispatch. The calendar answers whether a week is unusual; the dispatch step answers what to do about it.");

  // ---------- 4. Método ----------
  pres.addSection({ title: "Método e resultados" });
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Método e resultados" });
  s.addText("How we make the sensors comparable", { placeholder: "title" });
  const metodo = [
    [ic.grid, "Common grid", "0.1° × 0.1° cells (~11 km) absorb the 1 km vs 375 m footprint and the MODIS bow-tie effect.", C.accent4],
    [ic.bolt, "One scale", extra.texto_escala, C.accent2],
    [ic.chart, "Anomaly", "Weekly multi-year median and MAD. Z ≥ 2 or above the 95th percentile marks a critical week.", C.accent3],
  ];
  metodo.forEach(([img, tit, txt, cor], i) => {
    const y = 1.3 + i * 1.2;
    circulo(s, 0.5, y + 0.1, 0.7, img, cor, `met-${i + 1}`);
    s.addText(tit, { x: 1.4, y, w: 4.6, h: 0.38, fontSize: 17, bold: true, color: C.background1, margin: 0,
      isTextBox: true, objectName: `met-titulo-${i + 1}` });
    s.addText(txt, { x: 1.4, y: y + 0.4, w: 4.6, h: 0.65, fontSize: 13, color: C.background2, margin: 0,
      isTextBox: true, objectName: `met-texto-${i + 1}` });
  });
  cartao(s, 6.4, 1.3, 3.1, 3.4, "met-formula-cartao");
  s.addText("Robust anomaly score", { x: 6.6, y: 1.5, w: 2.7, h: 0.35, fontSize: 14, bold: true, color: C.accent2,
    margin: 0, isTextBox: true, objectName: "met-formula-titulo" });
  s.addText("Z = (N − median) / (1.48 · MAD)", { x: 6.6, y: 1.95, w: 2.7, h: 0.8, fontSize: 15, bold: true,
    color: C.background1, margin: 0, isTextBox: true, objectName: "met-formula" });
  s.addText(extra.texto_formula_n, { x: 6.6, y: 2.85, w: 2.7, h: 1.0, fontSize: 13, color: C.background2,
    margin: 0, isTextBox: true, objectName: "met-formula-n" });
  s.addText("Giglio et al. 2016 · Schroeder et al. 2014 · Wooster et al. 2005", { x: 6.6, y: 4.05, w: 2.7, h: 0.5,
    fontSize: 10, color: C.accent5, margin: 0, isTextBox: true, objectName: "met-refs" });
  s.addNotes("Pixel counts differ by sensor; the grid and the scaling put them on one scale. Median and MAD are robust to the extreme years we want to detect.");

  // ---------- 5. Calendário ----------
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Método e resultados" });
  s.addText(`Is this week normal? Tocantins, ${ANO}`, { placeholder: "title" });
  s.addChart(pres.charts.LINE, [
    { name: `Median ${extra.periodo_base}`, labels: semanas, values: valMed },
    { name: String(ANO), labels: semanas, values: valAno },
  ], {
    x: 0.5, y: 1.25, w: 6.1, h: 3.75, chartColors: ["94A3B8", THEME.colors.accent1], lineSize: 2.5, lineDataSymbol: "none",
    showLegend: true, legendPos: "t", legendColor: "CBD5E1", legendFontSize: 11, legendFontFace: "+mn-lt",
    catAxisLabelColor: "94A3B8", valAxisLabelColor: "94A3B8", catAxisLabelFontSize: 10, valAxisLabelFontSize: 10,
    catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFrequency: 4,
    catAxisTitle: "Week of the year", showCatAxisTitle: true, catAxisTitleColor: "94A3B8", catAxisTitleFontSize: 10,
    valAxisTitle: "Detections per week (MODIS-equivalent)", showValAxisTitle: true, valAxisTitleColor: "94A3B8", valAxisTitleFontSize: 10,
    valGridLine: { color: "1E293B", size: 0.75 }, catGridLine: { style: "none" }, catAxisLineShow: false, valAxisLineShow: false,
    objectName: "cal-grafico",
  });
  cartao(s, 6.9, 1.25, 2.6, 3.75, "cal-cartao");
  s.addText(extra.destaque_valor, { x: 7.05, y: 1.45, w: 2.3, h: 0.9, fontSize: 48, bold: true, color: C.accent3,
    margin: 0, isTextBox: true, objectName: "cal-stat" });
  s.addText(extra.destaque_rotulo, { x: 7.05, y: 2.35, w: 2.3, h: 1.0, fontSize: 13, color: C.background1,
    margin: 0, isTextBox: true, objectName: "cal-stat-rotulo" });
  s.addText(extra.destaque_2, { x: 7.05, y: 3.45, w: 2.3, h: 1.1, fontSize: 13, color: C.background2,
    margin: 0, isTextBox: true, objectName: "cal-stat-2" });
  s.addText("Data: NASA FIRMS archive, MODIS C6.1 + VIIRS S-NPP 375 m", { x: 7.05, y: 4.55, w: 2.3, h: 0.4,
    fontSize: 9, color: C.accent5, margin: 0, isTextBox: true, objectName: "cal-fonte" });
  s.addNotes("Real FIRMS archive for Tocantins. Grey: the typical week. Orange: the highlighted year. Critical weeks are the ones far above the grey line.");

  // ---------- 6. Despacho ----------
  pres.addSection({ title: "Impacto" });
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Impacto" });
  s.addText("When a week turns critical, crews need a plan", { placeholder: "title" });
  s.addImage({ path: OVERVIEW, x: 0.5, y: 1.3, w: 5.6, h: 3.5, objectName: "desp-imagem",
    altText: "FocoCerto web app: operations map with incidents by priority, crews on their way, and the incidents awaiting the coordinator's decision" });
  const desp = [
    [ic.crew, "Planner", "Proposes which fires to attend first, and with which crew", C.accent1],
    [ic.chart, "Critic", "Challenges trade-offs; distances and exposed people come from code, not from the model", C.accent2],
    [ic.user, "Coordinator", "Approves every dispatch, with the evidence on screen", C.accent6],
  ];
  desp.forEach(([img, tit, txt, cor], i) => {
    const y = 1.3 + i * 1.18;
    circulo(s, 6.4, y + 0.05, 0.55, img, cor, `desp-${i + 1}`);
    s.addText(tit, { x: 7.1, y, w: 2.4, h: 0.32, fontSize: 15, bold: true, color: C.background1, margin: 0,
      isTextBox: true, objectName: `desp-titulo-${i + 1}` });
    s.addText(txt, { x: 7.1, y: y + 0.34, w: 2.4, h: 0.75, fontSize: 12, color: C.background2, margin: 0,
      isTextBox: true, objectName: `desp-texto-${i + 1}` });
  });
  s.addText("Real run, Tocantins, 23 Oct 2026: 179 fire occurrences, 6 crews at real stations (crew counts simulated)",
    { x: 0.5, y: 4.85, w: 9, h: 0.3, fontSize: 10, color: C.accent5, margin: 0, isTextBox: true, objectName: "desp-rodape" });
  s.addNotes("The dispatch engine existed before Space Apps; what is new is that the calendar tells it when a period is critical.");

  // ---------- 7. Fecho ----------
  s = pres.addSlide({ masterName: "CAPA", sectionTitle: "Impacto" });
  s.addText("Open data, open code", { x: 0.5, y: 0.45, w: 9, h: 0.75, fontSize: 32, bold: true, color: C.background1,
    margin: 0, isTextBox: true, objectName: "fim-titulo" });
  const fim = [
    [ic.sat, "NASA data", "FIRMS MODIS C6.1\nFIRMS VIIRS 375 m\nNASA Worldview", C.accent4],
    [ic.code, "Open source", "Code, data pipeline and tests on GitHub, Apache 2.0", C.accent2],
    [ic.globe, "Next", "Pantanal and Gran Chaco, with AEB/INPE (Brazil) and CONAE (Argentina) data", C.accent1],
  ];
  const wf = 2.8, gf = 0.3;
  fim.forEach(([img, tit, txt, cor], i) => {
    const x = 0.5 + i * (wf + gf);
    cartao(s, x, 1.45, wf, 2.45, `fim-cartao-${i + 1}`);
    circulo(s, x + 0.25, 1.7, 0.6, img, cor, `fim-${i + 1}`);
    s.addText(tit, { x: x + 1.0, y: 1.75, w: wf - 1.2, h: 0.5, fontSize: 17, bold: true, color: C.background1,
      margin: 0, valign: "middle", isTextBox: true, objectName: `fim-titulo-${i + 1}` });
    s.addText(txt, { x: x + 0.25, y: 2.5, w: wf - 0.5, h: 1.25, fontSize: 13, color: C.background2, margin: 0,
      isTextBox: true, objectName: `fim-texto-${i + 1}` });
  });
  s.addText("From NASA data to crews on the ground.", { x: 0.5, y: 4.2, w: 9, h: 0.6, fontSize: 24, bold: true,
    italic: true, color: C.accent1, align: "center", margin: 0, isTextBox: true, objectName: "fim-frase" });
  s.addText([
    { text: "github.com/ufsm-ecomp-genai/fococerto.spaceapps",
      options: { hyperlink: { url: "https://github.com/ufsm-ecomp-genai/fococerto.spaceapps" }, color: C.accent2 } },
    { text: extra.video ? `   ·   Video: ${extra.video}` : "", options: { color: C.background2 } },
  ], { x: 0.5, y: 4.95, w: 9, h: 0.3, fontSize: 12, align: "center", margin: 0, isTextBox: true, objectName: "fim-rodape" });
  s.addNotes("NASA FIRMS and Worldview make this possible for free, for any region. Next: the Pantanal and the Gran Chaco.");

  await pres.writeFile({ fileName: SAIDA });
  await applyTheme(SAIDA, THEME);
  console.log("ok", SAIDA);
})().catch((e) => { console.error(e); process.exit(1); });
