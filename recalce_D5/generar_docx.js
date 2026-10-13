// Genera Solucion_recalce_D5.docx (Letter). Uso: node generar_docx.js
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Header, Footer,
  AlignmentType, PageOrientation, LevelFormat, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak,
} = require("docx");

const FONT = "Arial";
const W = 9360; // ancho útil retrato (DXA)
const p = (text, opts = {}) => new Paragraph({
  spacing: { after: 120, line: 276 }, ...opts.para,
  children: Array.isArray(text) ? text : [new TextRun({ text, font: FONT, size: 21, ...opts.run })],
});
const b = (t) => new TextRun({ text: t, bold: true, font: FONT, size: 21 });
const r = (t) => new TextRun({ text: t, font: FONT, size: 21 });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 280, after: 120 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 26 })] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 180, after: 80 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 22 })] });
const bullet = (children) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60, line: 276 },
  children: Array.isArray(children) ? children : [r(children)] });
const step = (children, ref = "n3") => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80, line: 276 },
  children });

const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, header, rows) {
  const total = widths.reduce((a, c) => a + c, 0);
  const cell = (t, w, head) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: head ? { fill: "D9D9D9", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: t, bold: !!head, font: FONT, size: 19 })] })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((t, i) => cell(t, widths[i], true)) }),
           ...rows.map((row) => new TableRow({ children: row.map((t, i) => cell(t, widths[i], false)) }))],
  });
}

const portrait = [
  new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 60 },
    children: [new TextRun({ text: "RECALCE DE LA ZAPATA D5 POR INTERFERENCIA CON EL FOSO DEL ASCENSOR", bold: true, font: FONT, size: 32 })] }),
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Propuesta de solución – documento preliminar", font: FONT, size: 24 })] }),
  new Paragraph({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "000000", space: 4 } },
    children: [new TextRun({ text: "Edificio multifamiliar, Cúcuta · Fecha: 13 de octubre de 2026 · ESQUEMA PRELIMINAR – NO PARA CONSTRUCCIÓN",
      font: FONT, size: 18 })] }),

  h1("1. Resumen"),
  p([r("La cimentación existente de la columna D5 (0,30 × 1,00 m, al ras del lindero) interfiere con el foso del ascensor, cuyo fondo terminado debe quedar a "),
     b("1,50 m"), r(" bajo el piso del sótano y cuyo pozo debe tener "), b("1,70 × 2,50 m libres"),
     r(". Se propone "), b("recortar la zapata Z1 de D5, integrar el foso como un cajón estructural y peraltar la viga de enlace del eje 5"),
     r(". La solución mantiene la base de la nueva losa-zapata en la cota original (−2,00 m, en la arcilla), no excava en la grava, respeta la escalera ya construida y conserva la ubicación del ascensor. Requiere un proyecto de apuntalamiento y transferencia de carga antes de demoler.")]),

  h1("2. Datos considerados"),
  bullet([b("Proyecto: "), r("seis pisos (tres de uso clínico y tres habitacionales); en ejecución del tercero. Micropilotes descartados.")]),
  bullet([b("D5: "), r("sección 0,30 × 1,00 m con la cara exterior al ras del lindero. Zapata Z1 de 2,0 × 2,0 m (excentricidad respecto a la columna ≈ 0,85 m). Carga de D5: 85 t (supuesta de servicio).")]),
  bullet([b("Foso y escalera: "), r("el hueco del ascensor queda pegado al lindero, al sur de D5; la escalera existente arranca unos 2,1 m al sur del eje de D5. Pozo libre de 1,70 × 2,50 m con muros de 0,20 m por fuera (huella exterior 2,90 × 2,10 m).")]),
  bullet([b("Suelo (estudio de suelos, enero de 2026): "), r("arcilla arenosa firme de 0 a 2,00 m; grava arenosa de densidad media a suelta de 2,00 a 6,00 m (sin parámetros en el estudio). Cimentación recomendada a 2,00 m con q_adm = 33 t/m² (323,65 kPa). El sótano está al nivel del terreno de los sondeos.")]),
  bullet([b("Cimentación existente: "), r("zapatas Z1 aisladas unidas por vigas VC.S‑55×40 (ejes 1, 3, 5 y 6) y una viga longitudinal VC.S‑6 en el eje C; contrapiso no estructural de 0,11 m.")]),

  h1("3. Solución propuesta"),
  p("La solución tiene cuatro componentes (ver lámina en la última página):"),
  step([b("Zapata Z1 recortada: "), r("se conserva la parte norte (hasta el eje 5) y se demuelen 1,0 m del lado sur, que chocan con el foso.")]),
  step([b("Cajón del foso: "), r("losa-zapata de 0,45 m como máximo y muros de 0,20 m, en concreto nuevo, con pozo libre de 1,70 × 2,50 m. Su base queda en −2,00 m (contacto arcilla/grava), la misma de la zapata original. En el modelo toma cerca del 48 % de la carga de D5.")]),
  step([b("Viga de enlace del eje 5: "), r("0,40 × 1,00 m (nueva o reforzada) hacia A5, para controlar el giro de la zapata excéntrica.")]),
  step([b("Escalera existente: "), r("no se interviene. La holgura estimada con el cajón es de unos 0,03 m (a medir en obra).")]),
  h2("Cotas (m bajo el piso terminado del sótano = terreno de los sondeos)"),
  table([5200, 4160], ["Elemento", "Cota"], [
    ["Fondo terminado del foso", "−1,50"],
    ["Base de la zapata existente Z1 (estudio de suelos)", "−2,00"],
    ["Base del cajón (losa-zapata ≤ 0,45 m)", "≈ −2,00 (contacto arcilla/grava)"],
    ["Zapata nueva profunda bajo la placa (opción descartada)", "−2,35 a −2,55 (0,35–0,55 m dentro de la grava)"],
  ]),
  p("", { para: { spacing: { after: 60 } } }),
  p([b("Condición: "), r("la losa-zapata no debe pasar de unos 0,45 m de espesor para que su base no entre en la grava; con los 10 cm de concreto de saneamiento que recomienda el estudio, una losa de 0,40 m ya llegaría a −2,05 m.")]),

  h1("4. Verificación con un modelo preliminar"),
  p("Se usó un modelo de parrilla de vigas sobre resortes de suelo, sin tracciones, con la carga de D5 en 85 t y cargas vecinas por reparto tributario (supuesto). No incluye sismo. Con viga de enlace de 0,40 × 1,00 m y restricción rotacional de la superestructura ×3 (supuesto), la presión máxima de contacto / q_adm es:"),
  table([2400, 2320, 2320, 2320], ["Zapata", "Original (sin foso)", "Solución propuesta", "Observación"], [
    ["D5", "1,27", "1,33", "cajón: 48 % de la carga"],
    ["D3", "1,44", "1,47", "gobierna el sistema*"],
    ["A3", "1,43", "1,44", "gobierna el sistema*"],
    ["A5", "1,26", "1,27", ""],
    ["D6", "0,89", "0,81", ""],
  ]),
  p("* Depende de cargas de D3 y A3 que son supuestas (≈ 836 kN); se requieren las reales.", { run: { size: 17, italics: true }, para: { spacing: { before: 60, after: 120 } } }),
  p("Lectura: la solución mantiene el desempeño de la zapata original (+3 a 5 % en D5) sin excavar en la grava. El modelo muestra además que, con 85 t, la zapata original ya está por encima de q_adm si la restricción al giro es baja (1,85 veces con ×1); una viga de enlace más peraltada reduce esa presión (≈ 23 % con 0,40 × 1,00 m y ≈ 31 % con 0,40 × 1,20 m). Que presiones de borde por encima de q_adm sean aceptables debe dictaminarlo el geotecnista (el estudio usa Fs = 5,27)."),
  h2("Alternativas descartadas"),
  table([2900, 6460], ["Alternativa", "Motivo"], [
    ["Zapata nueva profunda bajo la placa del foso", "La base queda 0,35–0,55 m dentro de la grava media-suelta, sin parámetros de resistencia; excavación inestable junto al lindero; sube la presión de las zapatas vecinas (≈ +12 %)."],
    ["Recortar y prolongar la zapata hacia el norte, o corrida angosta hacia el norte", "Saca el centroide del eje de la columna: aumenta la excentricidad a lo largo del lindero y empeora la presión (2,4–2,5 veces q_adm con restricción ×1)."],
    ["Colgar D5 de la viga de lindero", "Sobrecarga las zapatas D3 y D6 (1,5 a 2,0 veces su presión original) aun ampliándolas."],
    ["Micropilotes", "Descartados por el proyecto."],
  ]),

  h1("5. Procedimiento de ejecución"),
  step([b("Levantamiento en obra: "), r("dimensiones y refuerzo reales de Z1 en D5 y A5 y de la viga del eje 5; posición construida del hueco del ascensor y holgura con la escalera.")], "n5"),
  step([b("Proyecto de apuntalamiento y transferencia de carga: "), r("apuntalar la columna D5 y transferir su carga a un soporte temporal (puntales y gatos), con monitoreo de asentamientos y fisuras en D5, zapatas vecinas, lindero y escalera.")], "n5"),
  step([b("Protección y excavación: "), r("entibado, protección del lindero y de la escalera; excavación por tramos.")], "n5"),
  step([b("Demolición controlada: "), r("1,0 m de la zapata Z1 (lado sur), sin afectar la parte que se conserva ni el acero que se reutilice.")], "n5"),
  step([b("Cajón del foso: "), r("concreto de saneamiento de 10 cm, armado y vaciado de la losa-zapata (≤ 0,45 m) y de los muros de 0,20 m; anclajes químicos a la zapata existente; juntas e impermeabilización. Pozo libre de 1,70 × 2,50 m.")], "n5"),
  step([b("Viga de enlace del eje 5: "), r("construir o reforzar la viga de 0,40 × 1,00 m hacia A5.")], "n5"),
  step([b("Curado y transferencia: "), r("al alcanzar la resistencia de diseño, transferir la carga de D5 al nuevo conjunto y retirar el apuntalamiento, con monitoreo activo.")], "n5"),
  step([b("Entrega del pozo: "), r("verificar las dimensiones libres (1,70 × 2,50 m) y las tolerancias con el proveedor del ascensor.")], "n5"),

  h1("6. Condiciones, supuestos y pendientes"),
  bullet("Cargas reales de D3, A3, A5 y D6 (las del modelo son supuestas) y la carga de D5 (85 t) confirmada como de servicio o mayorada."),
  bullet("Restricción real al giro de la superestructura en los nodos (modelo completo del edificio) y verificación sísmica; el modelo preliminar no incluye sismo."),
  bullet("Consulta formal al geotecnista: parámetros de la grava, aclaración del estrato bajo 2,00 m (la tabla resumen habla de arcilla y el registro del Sondeo 1 muestra grava), peso unitario (1,90 t/m³ en la tabla contra 15,48 kN/m³ en el cálculo), presión de borde aceptable y recomendaciones de excavación junto al lindero."),
  bullet("Tolerancia del pozo según el proveedor del ascensor y holgura real con la escalera (si los 1,70 × 2,50 m deben quedar libres después de acabados, la estructura necesita unos 0,05 m más por lado)."),
  bullet("Cuadro de elementos de fundación (dimensiones y refuerzo reales de Z1, VC.S‑55×40 y VC.S‑6)."),
  bullet("Diseño definitivo firmado por el ingeniero estructural responsable, con revisión independiente, y verificación de si se requiere modificación de la licencia ante la curaduría."),
];

const landscape = [
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Lámina: planta y corte de la solución propuesta", bold: true, font: FONT, size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new ImageRun({ type: "png", data: fs.readFileSync("solucion_plano.png"),
      transformation: { width: 900, height: 556 },
      altText: { title: "Solución D5", description: "Planta y corte B-B del cajón del foso y la zapata recortada de D5", name: "solucion" } })] }),
  new Paragraph({ children: [new TextRun({ text: "Esquema preliminar; dimensiones en metros. Sujeto a las condiciones del numeral 6.", font: FONT, size: 17, italics: true })] }),
];

const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "Documento preliminar – no para construcción · Página ", font: FONT, size: 16 }),
  new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16 })] })] });

const doc = new Document({
  creator: "Claude", title: "Recalce de D5 – propuesta de solución",
  styles: { default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: FONT }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, font: FONT }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 1 } },
    ] },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "n3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
    { reference: "n5", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [
    { properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, bottom: 1200, left: 1440, right: 1440 } } },
      footers: { default: footer }, children: portrait },
    { properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 900, bottom: 900, left: 1080, right: 1080 } } },
      footers: { default: footer }, children: landscape },
  ],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync("Solucion_recalce_D5.docx", buf); console.log("ok"); });
