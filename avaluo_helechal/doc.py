from docx import Document
from docx.shared import Pt
d=Document(); d.styles['Normal'].font.name='Arial'; d.styles['Normal'].font.size=Pt(10)
H=lambda t,l=1:d.add_heading(t,l); P=d.add_paragraph
def T(rows,hdr=True):
    t=d.add_table(rows=len(rows),cols=len(rows[0])); t.style='Light Grid Accent 1'
    for i,r in enumerate(rows):
        for j,v in enumerate(r): t.cell(i,j).text=str(v)
    d.add_paragraph()
d.add_heading('INFORME DE AVALÚO COMERCIAL RURAL – MEMORIAS DE CÁLCULO',0)
P('Predio rural, vereda Helechal Alto, municipio de Los Patios (Norte de Santander)\nFecha del informe: 8 de noviembre de 2026\nESTADO: PRELIMINAR – pendiente de visita técnica y verificación documental').runs[0].bold=True
p=P('ADVERTENCIA: las cifras de este documento se calculan con datos supuestos o de ejemplo (marcados en rojo en el Excel anexo) porque no se contó con matrícula, ficha catastral, visita de campo ni ofertas verificadas. No constituye avalúo definitivo ni debe usarse ante terceros hasta reemplazar la muestra de mercado y firmar el perito con RAA vigente.'); p.runs[0].bold=True
H('1. Información básica')
T([['Solicitante','Por confirmar'],['Objeto','Determinar el valor comercial del inmueble'],['Predio','Finca, vereda Helechal Alto, Los Patios (N. de S.)'],['Área','≈ 18 ha (declarada; verificar con certificado y levantamiento)'],['Matrícula / cédula catastral','Por confirmar'],['Tipo de inmueble','Rural, uso agropecuario (ganadería en potreros) con vivienda campestre y piscina'],['Fecha de visita','Por confirmar']])
H('2. Marco normativo y metodológico')
for s in ['Ley 388 de 1997 y Decreto 1170 de 2015 (único reglamentario del sector Información Estadística), sección de avalúos IGAC.',
'Resolución IGAC 620 de 2008: métodos de comparación o de mercado, costo de reposición, capitalización de rentas y residual; control estadístico de la muestra (CV ≤ 7,5 %).',
'Resolución IGAC 1044 de 2014 y demás resoluciones complementarias del IGAC vigentes.',
'Ley 1673 de 2013 y Decreto 556 de 2014 (actividad del avaluador; RAA). Normas técnicas sectoriales NTS I 01 y NTS S 01.',
'VERIFICAR: este informe se basó en la Res. 620/2008 y sus modificaciones conocidas. No pude consultar el portal del IGAC en esta sesión; el perito debe confirmar si existe una resolución posterior que actualice la metodología y ajustar el informe.']:
    d.add_paragraph(s,style='List Bullet')
P('Métodos aplicados: (i) Comparación de mercado para el terreno, con homogeneización y control estadístico; (ii) Costo de reposición depreciado (Ross-Heidecke) para vivienda, piscina y anexos. Capitalización de rentas se usa solo como contraste (ver §8). Valor total = terreno + construcciones y anexos.')
H('3. Descripción del sector y del predio')
for s in ['Ubicación: Helechal Alto, zona rural del municipio de Los Patios, área metropolitana de Cúcuta; influencia urbana moderada que favorece demanda recreativa/campestre. (Verificar vías, distancia al casco urbano, POT/EOT, normas de uso del suelo y restricciones ambientales, rondas hídricas, amenaza por remoción en masa.)',
'Topografía: mixta: parte plana, parte ondulada y parte de ladera fuerte (>25 %).',
'Uso actual: potreros; vivienda con piscina, acabados medios.',
'Servicios: por verificar (acueducto veredal/pozo, energía, vías de acceso, conectividad).']:
    d.add_paragraph(s,style='List Bullet')
H('4. Zonas homogéneas físicas del terreno (supuestos)')
T([['Zona','Descripción','Pendiente','Área (ha)','Factor vs. referencia'],['Z1','Plano – potrero mejorado','0–7 %','4,0','1,20'],['Z2','Ondulado – potrero','7–25 %','6,0','1,00'],['Z3','Ladera fuerte – pastos/rastrojo','>25 %','8,0','0,70']])
P('La distribución de áreas (4/6/8 ha) es un supuesto; debe medirse con GPS/plano. Los factores relativos se sustentan en la relación de mercado plano–ondulado–ladera y deben calibrarse con ofertas reales.')
H('5. Investigación de mercado y homogeneización')
P('Muestra de seis ofertas de ejemplo (a reemplazar). Del valor de oferta se descuentan las construcciones, se aplican factores de negociación, topografía, acceso, aguas/servicios y área, y se obtiene el valor homogéneo por hectárea del terreno de referencia (ondulado, acceso bueno).')
T([['#','Área ha','$/ha bruto (terreno)','Factores aplicados','$/ha homogeneizado'],['1','15','60.000.000','0,94','56.400.000'],['2','20','55.000.000','0,92·1,10·1,03','57.329.800'],['3','8','68.750.000','0,95·0,96','62.700.000'],['4','25','50.000.000','0,90·1,12·1,03·1,05','54.507.600'],['5','10','70.000.000','0,93·0,95','61.845.000'],['6','18','54.444.444','0,92·1,05','52.593.333']])
T([['Promedio','$57.562.622/ha'],['Desviación estándar','$4.004.105'],['Coeficiente de variación','6,96 % (≤ 7,5 %: CUMPLE)'],['Valor adoptado terreno de referencia','$57.600.000/ha']])
H('6. Valor del terreno')
T([['Zona','Área (ha)','$/ha ajustado','Valor ($)'],['Z1 plano','4,0','69.120.000','276.480.000'],['Z2 ondulado','6,0','57.600.000','345.600.000'],['Z3 ladera fuerte','8,0','40.320.000','322.560.000'],['TOTAL TERRENO','18,0','52.480.000 (prom.)','944.640.000']])
H('7. Construcciones y anexos – costo de reposición depreciado')
P('Fórmula: Valor = Cantidad × Costo nuevo × (1 – D); D = Ross + (1 – Ross)·C(Heidecke); Ross = 0,5·(t/n + (t/n)²).')
T([['Ítem','Cant.','Costo nuevo','Edad/Vida','Estado','Depreciación','Valor ($)'],['Vivienda, acabados medios','180 m²','2.300.000/m²','12/70','2','12,31 %','363.045.759'],['Piscina','32 m²','2.000.000/m²','10/40','2','17,75 %','52.639.200'],['Cercas (4 hilos)','3.500 ml','9.000/ml','8/15','2,5','45,67 %','17.113.642'],['Corral/brete','1 gl','18.000.000','10/30','2,5','28,51 %','12.867.400'],['Reservorio/conducciones','1 gl','12.000.000','10/30','2,5','28,51 %','8.578.267'],['TOTAL','','','','','','454.244.267']])
P('Áreas, edades, estado y costos son supuestos: confirmar con la visita, licencia/planos y presupuesto actualizado (p. ej., Construdata).')
H('8. Resultado')
T([['Concepto','Valor ($)'],['Terreno','944.640.000'],['Vivienda, piscina y anexos','454.244.267'],['VALOR COMERCIAL TOTAL (PRELIMINAR)','1.398.884.267'],['Adoptado (redondeado)','1.399.000.000'],['Valor integral por ha','≈ 77.700.000']])
P('Contraste: el valor por hectárea de ~$52 millones para el terreno solo es coherente con la muestra; verificar frente a rentas de ganadería (capitalización) que normalmente arrojan valores menores y justifican que el mercado pague por ubicación y uso campestre.')
H('9. Consideraciones y limitaciones')
for s in ['Datos de mercado, áreas por zona, medidas de construcciones, edad y costos son ejemplos/supuestos hasta visita y documentos.',
'Verificar: certificado de tradición (gravámenes, servidumbres, limitaciones, falsa tradición), uso del suelo y normativa ambiental, acceso legal, fuentes de agua, licencias de construcción y de la piscina.',
'Vigencia: el avalúo comercial tiene vigencia de un año si las condiciones no cambian (art. 19 Decreto 422 de 2000).',
'Respetar declaración de independencia, ausencia de conflicto de intereses y firma con número de RAA, requisitos que debe aportar el perito titular.']:
    d.add_paragraph(s,style='List Bullet')
H('10. Anexos requeridos para el informe definitivo')
for s in ['Registro fotográfico, plano/levantamiento y coordenadas.','Certificado de tradición y libertad, ficha predial, certificado de uso del suelo.','Soportes de ofertas (fuente, contacto, fecha) y tablas de homogeneización.','Libro de cálculo: Memoria_Calculo_Avaluo_Rural_Helechal_Alto.xlsx (fórmulas vivas).']:
    d.add_paragraph(s,style='List Bullet')
d.save('Informe_Avaluo_Rural_Helechal_Alto_PRELIMINAR.docx')
