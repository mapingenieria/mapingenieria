from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from openpyxl import load_workbook
wb=load_workbook('/tmp/recalc/Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx',data_only=True)
f=lambda v:f"{v:,.0f}".replace(",",".")
fd=lambda v,n=2:f"{v:,.{n}f}".replace(",","X").replace(".",",").replace("X",".")
H4=wb['4_Homogeneizacion']; T5=wb['5_Terreno']; N6=wb['6_Renta_contraste']; C7=wb['7_Construcciones']; R0=wb['0_Resumen']; I2=wb['2_IGAC_Catastro']; O3=wb['3_Ofertas_reales']; P9=wb['9_Topografia']
BLACK=RGBColor(0,0,0)
d=Document()
sec=d.sections[0]; sec.left_margin=sec.right_margin=Cm(2.5); sec.top_margin=sec.bottom_margin=Cm(2.2)
st=d.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(10); st.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial')
for name,size in (('Title',18),('Heading 1',12),('Heading 2',11)):
    s=d.styles[name]; s.font.name='Arial'; s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=BLACK
    s.element.rPr.rFonts.set(qn('w:ascii'),'Arial'); s.element.rPr.rFonts.set(qn('w:hAnsi'),'Arial')
for sn in ('Title','Heading 1','Heading 2'):
    pPr=d.styles[sn].element.get_or_add_pPr()
    for b in pPr.findall(qn('w:pBdr')): pPr.remove(b)
d.styles['Heading 1'].paragraph_format.space_before=Pt(14); d.styles['Heading 1'].paragraph_format.space_after=Pt(4)
# número de página en el pie
fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=fp.add_run('Avalúo Lote 1-1 Tequendama · Helechal Alto · Borrador · Página '); r.font.size=Pt(8)
for t_,txt in (('begin',None),('instr',' PAGE '),('end',None)):
    run=fp.add_run(); run.font.size=Pt(8)
    if t_=='instr':
        e=OxmlElement('w:instrText'); e.set(qn('xml:space'),'preserve'); e.text=txt
    else:
        e=OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'),t_)
    run._r.append(e)
N=[0]
def H(t):
    N[0]+=1; return d.add_heading(f"{N[0]}. {t}",1)
P=d.add_paragraph
def BL(items):
    for s in items: d.add_paragraph(s,style='List Bullet')
def shade(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:color'),'auto'); sh.set(qn('w:fill'),fill); tcPr.append(sh)
def T(rows,header=True,widths=None,bold_last=False):
    t=d.add_table(rows=len(rows),cols=len(rows[0])); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,r_ in enumerate(rows):
        for j,v in enumerate(r_):
            c=t.cell(i,j); c.text=''; p=c.paragraphs[0]; run=p.add_run(str(v)); run.font.size=Pt(8.5)
            if header and i==0: run.bold=True; shade(c,'D9D9D9')
            if bold_last and i==len(rows)-1: run.bold=True
            if widths: c.width=Cm(widths[j])
    d.add_paragraph().paragraph_format.space_after=Pt(2)
def FIG(path,caption,w=16.0):
    p=d.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(path,width=Cm(w))
    c=d.add_paragraph(caption); c.alignment=WD_ALIGN_PARAGRAPH.CENTER; c.runs[0].italic=True; c.runs[0].font.size=Pt(8.5)
terr=R0['B4'].value; cons=R0['B5'].value; tot=R0['B7'].value; ref=H4['B18'].value
mean,med,sd,cv=H4['B12'].value,H4['B13'].value,H4['B14'].value,H4['B15'].value
cat=I2['F8'].value; ren=N6['L8'].value
A=19.5355
ti=d.add_heading('INFORME DE AVALÚO COMERCIAL RURAL',0); ti.alignment=WD_ALIGN_PARAGRAPH.LEFT
p=P(); r=p.add_run('LOTE 1-1 TEQUENDAMA – Vereda Helechal Alto, Los Patios (Norte de Santander)\nMatrícula inmobiliaria 260-323861 · Código catastral 54405-00-00-0009-0020-000\nFecha del informe: 8 de noviembre de 2026\nMetodología: Resolución IGAC 941 de 2026 y su Anexo Técnico\nESTADO: BORRADOR PARA AJUSTE Y FIRMA DEL PERITO'); r.bold=True
p=P(); r=p.add_run('Este borrador se elaboró con la información disponible: datos oficiales del catastro del IGAC, ofertas publicadas en internet (precios pedidos), un modelo de elevación y supuestos técnicos del elaborador. No incluye visita técnica ni certificado de tradición. Las cifras deben ser revisadas y ajustadas por el perito avaluador (RAA) antes de su firma; los supuestos están resaltados en el libro de cálculo anexo.'); r.bold=True
H('Resumen ejecutivo')
T([['Concepto','Valor'],['Valor comercial total (borrador)','$ '+f(tot)],['Valor del terreno (comparación)','$ '+f(terr)],['Vivienda, piscina y anexos (costo depreciado)','$ '+f(cons)],['Rango por sensibilidad ±10 % del terreno','$ '+f(R0['B12'].value)+' a $ '+f(R0['B13'].value)],['Valor integral por hectárea','$ '+f(R0['B8'].value)],['Valor catastral IGAC del terreno (contraste)','$ '+f(cat)],['Renta pecuaria capitalizada (contraste)','$ '+f(ren)]],widths=[9,7])
P('Advertencia estadística: el coeficiente de variación de la muestra homogeneizada es %s %%, por encima del 10 %% que el art. 21 de la Resolución 941/2026 admite para inmuebles rurales. Se adoptó la mediana ($%s/ha) con la sustentación del art. 21, parágrafo 1, pero la muestra debe depurarse y ampliarse con ofertas confirmadas antes de firmar.'%(fd(cv,1),f(ref)))
H('Información básica')
T([['Predio','LOTE 1-1 TEQUENDAMA HELECHAL ALTO'],['Municipio / vereda','Los Patios (54405) / Helechal Alto'],['Matrícula inmobiliaria','260-323861 (verificar con el certificado de tradición)'],['Código catastral','54405-00-00-0009-0020-000 (NPN 544050000000000090020000000000)'],['Destino económico catastral','D – agropecuario'],['Área de terreno catastral','195.355 m² = 19,54 ha'],['Área construida catastral','70 m² (2 habitaciones, 1 piso, tipificación 2, puntaje 16); la piscina no figura'],['Tipo de avalúo','Comercial rural'],['Solicitante / propietario / visita técnica','Por confirmar']],header=False,widths=[5.5,10.5])
H('Marco normativo y metodológico')
BL(['Resolución IGAC 941 de 2026 (31-jul-2026) y Anexo Técnico: métodos y condiciones de los avalúos. Deroga la Res. 620 de 2008 y el art. 13 e incisos 1-3 del art. 14 de la Res. 898 de 2014 (art. 60). Este avalúo se rige por la 941 (art. 59, transitoriedad).',
'Aplicación: art. 10 (visita técnica), art. 11 (parámetros, AHT, construcciones), art. 14 (informe), arts. 17-19 (comparación), art. 21 (CV rural ≤ 10 %), arts. 46-47 (rurales agropecuarios: costo, comparación y renta; terreno y construcciones por separado).',
'Decreto 1170 de 2015, arts. 2.2.2.3.19 y 2.2.2.3.20; Ley 1673 de 2013 y Decreto 556 de 2014 (RAA).',
'Métodos: comparación de mercado para el terreno; capitalización de ingresos y valor catastral como contrastes; costo de reposición depreciado (Ross-Heideck, Anexo §2.3.4) para construcciones y anexos.',
'La resolución se leyó por OCR de un PDF escaneado y el Anexo como texto: verificar los artículos citados contra el Diario Oficial.'])
H('Descripción del predio y norma de uso')
P('Datos oficiales del catastro público del IGAC (09-2026) y de las capas de Zonas Homogéneas (vigencia de zonas: 1-ene-2019):')
T([['Zona física/económica','Área (ha)','AHT','Norma de uso (IGAC)','Valor catastral $/ha']]+[[f"{I2.cell(r_,1).value}/{I2.cell(r_,2).value}",fd(I2.cell(r_,4).value),I2.cell(r_,8).value.split(' / ')[0].replace('AHT ',''),I2.cell(r_,7).value.capitalize(),f(I2.cell(r_,5).value)] for r_ in (5,6,7)])
P('En las tres zonas el IGAC registra agua escasa y vías regulares (angostas; una zona sin pavimentar). El uso actual predominante son pastos naturales (zona 014, 83 % del predio) y bosques en las zonas 008 y 021.')
P('Norma municipal: el Plan Básico de Ordenamiento Territorial de Los Patios (documento de Corponor, plantilla sin número ni fecha, probablemente del año 2000) incluye la vereda El Helechal en el suelo rural. Para zonas pecuarias, el uso principal es la ganadería extensiva; la recreación y las parcelaciones rurales son condicionadas y los usos urbanos, suburbanos e industriales están prohibidos. Conclusión preliminar: suelo rural agropecuario con uso recreativo solo condicionado. Debe confirmarse con el certificado de uso del suelo de Planeación Municipal y el POT/EOT vigente.')
H('Topografía y pendientes')
P('La pendiente se calculó sobre el polígono catastral del predio con el modelo de elevación SRTM de 30 m (525 puntos de elevación, método de Horn y remuestreo a 5 m), clasificada con los rangos agrológicos del IGAC. Los puntos de lindero en disputa aportados por el propietario no se usaron.')
T([['Clase','Pendiente','Descripción','% del predio','Área (ha)']]+[[P9.cell(r_,1).value,P9.cell(r_,2).value+' %',P9.cell(r_,3).value,fd(P9.cell(r_,4).value*100,1)+' %',fd(P9.cell(r_,5).value)] for r_ in range(5,12)]+[['','','Total','100,0 %',fd(P9['E12'].value)]],bold_last=True,widths=[1.5,2.5,6,3,3])
FIG('Mapa_Topografia_Lote_1-1.png','Figura 1. Pendientes (izquierda) y altitudes (derecha) sobre el polígono catastral del Lote 1-1, modelo SRTM de 30 m. Fuente: elaboración propia con datos del IGAC y SRTM.')
T([['Zona IGAC','Área (ha)','Pendiente media','12-25 %','25-50 %','> 50 %']]+[[P9.cell(r_,1).value,fd(P9.cell(r_,2).value),f"{P9.cell(r_,3).value:.0f} %",f"{P9.cell(r_,4).value*100:.0f} %",f"{P9.cell(r_,5).value*100:.0f} %",f"{P9.cell(r_,6).value*100:.0f} %"] for r_ in (22,23,24)])
BL(['Pendiente media de 32,5 % (percentiles 10 y 90: 20,6 % y 47,2 %). Cotas de 842 a 998 m s. n. m., desnivel de unos 156 m, con laderas orientadas al occidente y suroccidente.','Incertidumbre (error vertical de 6 m, simulación Monte Carlo): ondulado 17-27 %, quebrado 62-74 %, escarpado 6-11 % del predio.','Contraste con perfiles de Google Earth aportados por el propietario: inclinación mediana de 8,2° (14 %) y 12,4° (22 %), máxima de 22° (40 %) y 40,8° (86 %). Sus líneas cruzan las curvas de nivel en diagonal, por lo que subestiman la pendiente máxima.','Los códigos AHT del IGAC (CSe en la zona 014; CSd en la zona 008) son consistentes con estas clases, según la convención de letras de pendiente; verificar con la leyenda oficial.','Conclusión: topografía ondulada a quebrada, sin terreno plano. El modelo no distingue terrazas menores de 30 m; las áreas deben confirmarse con levantamiento topográfico, LiDAR o dron.'])
H('Estudio de mercado')
P('Se recopilaron ofertas de venta de fincas en Cúcuta, Los Patios, Villa del Rosario, El Zulia, Durania y Chinácota (portales Fincaraíz, Ciencuadras, Nuroa y Mi Plataforma de Negocios; captura del 8-nov-2026). Son precios pedidos. En Los Patios, Villa del Rosario y El Zulia casi no hay fincas agropecuarias publicadas (los 62 anuncios de Fincaraíz son lotes campestres pequeños o terrenos de expansión, no comparables). Por eso se usan fincas de Cúcuta (Aguaclara), Chinácota y Durania, con ajustes por clima, agua, topografía, acceso y área. Resumen de ofertas:')
rows=[['#','Ubicación','Tipo','Área (ha)','Precio pedido ($)','$/ha integral','Comparable']]
for r_ in range(2,O3.max_row+1):
    if not isinstance(O3.cell(r_,1).value,int): continue
    p_=O3.cell(r_,5).value; a=O3.cell(r_,4).value; c=(O3.cell(r_,14).value or '')
    rows.append([O3.cell(r_,1).value,O3.cell(r_,2).value,O3.cell(r_,3).value,a,f(p_),f(p_/a),c.split(':')[0][:14]])
T(rows)
H('Homogeneización y control estadístico (arts. 17-21)')
P('Para cada oferta se aplicó el factor de negociación (0,90, supuesto), se descontó el valor estimado de construcciones y cultivos, y se ajustó por topografía, agua, clima/ubicación, acceso y área respecto al terreno de referencia (ondulado, pastos, vía regular). Los factores son criterio del elaborador y deben calibrarse.')
T([['Oferta','Área ha','Valor terreno ($)','$/ha','Factores (topo·agua·clima·vía·área)','$/ha homogeneizado']]+[[H4.cell(r_,2).value[:34],H4.cell(r_,3).value,f(H4.cell(r_,8).value),f(H4.cell(r_,9).value),'·'.join(f"{H4.cell(r_,c).value:g}" for c in (10,11,12,13,14)),f(H4.cell(r_,15).value)] for r_ in range(5,11)])
T([['Promedio',f"$ {f(mean)}/ha"],['Mediana',f"$ {f(med)}/ha"],['Desviación estándar',f"$ {f(sd)}"],['Coeficiente de variación',f"{fd(cv,1)} % (límite rural 10 %: no cumple)"],['Valor adoptado, terreno de referencia (mediana)',f"$ {f(ref)}/ha"]],header=False,widths=[8,8])
P('Sustentación (art. 21, par. 1): al no cumplirse el CV, se adopta la mediana por la presencia de valores extremos (Chinácota 54 ha por su gran tamaño y Durania 15 ha por una vivienda de 300 m² cuyo descuento es incierto). El perito debe depurar o ampliar la muestra hasta cumplir el CV o dejar constancia razonada del criterio.')
H('Valor del terreno')
P('El terreno se valora por franjas de pendiente, con las áreas calculadas en el capítulo 5 (la franja de 12-25 % incluye la mínima fracción de 7-12 %; la franja escarpada es el saldo hasta el área catastral). Los factores respecto al terreno de referencia (ondulado) son criterio del perito.')
T([['Franja','Descripción','Pendiente','Área (ha)','Factor','$/ha','Valor ($)']]+[[T5.cell(r_,1).value,T5.cell(r_,2).value,T5.cell(r_,3).value,fd(T5.cell(r_,4).value),fd(T5.cell(r_,5).value),f(T5.cell(r_,7).value),f(T5.cell(r_,8).value)] for r_ in (5,6,7)]+[['TOTAL','','',fd(T5.cell(8,4).value),'',f(T5['H9'].value),f(terr)]],bold_last=True)
H('Contrastes del valor del terreno')
T([['Referencia','Valor terreno ($)','$/ha','Observación'],['Comparación de mercado (adoptado)',f(terr),f(terr/A),'Precios pedidos ajustados'],['Valor catastral IGAC (zonas 2019)',f(cat),f(cat/A),'Referencia oficial, no comercial; vigencia 2019'],['Capitalización de renta pecuaria',f(ren),f(ren/A),'Supuestos: carga 0,8/0,5/0,25 UGG/ha, 200 kg/UGG/año, $7.800/kg, costos 60 %, 40 % tierra, tasa 7,3 %']])
P('El valor por comparación es unas %s veces el catastral y %s veces la renta ganadera. Esa diferencia se explica por el mercado de fincas de recreo y ganadería con agua cerca de Cúcuta, pero con norma de uso agropecuaria el art. 47 exige fundamentar el valor en la capacidad de generar ingresos: el perito debe sustentar la adopción de la comparación o ponderar con la renta.'%(fd(terr/cat,1),fd(terr/ren,1)))
H('Construcciones y anexos (costo de reposición depreciado)')
P('FD = (1 − ½(x/n + x²/n²)) × E; VA = Vn × FD (Anexo §2.3.4, Tabla 6 de Heideck). Vida útil según Tabla 2 o sustentada (nota 3).')
T([['Ítem','Cant.','Costo nuevo','Edad/Vida','Estado','FD','Valor ($)']]+[[C7.cell(r_,2).value[:42],f"{C7.cell(r_,3).value:g} {C7.cell(r_,4).value}",f(C7.cell(r_,5).value),f"{C7.cell(r_,6).value}/{C7.cell(r_,7).value}",C7.cell(r_,9).value,f"{C7.cell(r_,12).value:.3f}",f(C7.cell(r_,13).value)] for r_ in range(5,10)]+[['TOTAL','','','','','',f(cons)]],bold_last=True)
P('La vivienda usa el área catastral (70 m²), que probablemente está desactualizada; la piscina (32 m²), cercas, corral y reservorio son supuestos. Medir en la visita: el valor de las construcciones puede cambiar de forma importante.')
H('Resultado')
T([['Concepto','Valor ($)'],['Terreno',f(terr)],['Construcciones y anexos',f(cons)],['VALOR COMERCIAL TOTAL',f(R0['B6'].value)],['Valor adoptado (redondeado a $1.000.000)',f(tot)],['Valor integral por hectárea',f(R0['B8'].value)]],widths=[9,7])
H('Limitaciones y pendientes')
BL(['No se realizó visita técnica (obligatoria, art. 10): medir las áreas por franja, la vivienda, la piscina y los anexos; verificar estado, potreros, agua, accesos y servidumbres.','Certificado de tradición y libertad (260-323861): propietario, título, gravámenes, limitaciones y servidumbres. Existe una disputa de lindero informada por el propietario que debe constar en el informe.','Certificado de uso del suelo expedido por Planeación Municipal y verificación del POT/EOT vigente y de determinantes ambientales (rondas hídricas, Corponor).','Ofertas confirmadas con los oferentes (fecha, % de negociación, área real, topografía y agua) y más datos de Los Patios, Villa del Rosario y El Zulia.','Los factores de ajuste, los descuentos de construcciones y cultivos, los factores por pendiente y los parámetros de renta son supuestos del elaborador.','Entrega de la información al Observatorio Inmobiliario Catastral del IGAC (art. 58) y datos del solicitante, marco jurídico del encargo, firma y RAA del avaluador (art. 14).','Verificar si la Res. 941/2026 regula la vigencia del avalúo (no se encontró en el texto leído).'])
H('Anexos')
BL(['Libro de cálculo consolidado: Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx (datos, catastro IGAC, ofertas, homogeneización, terreno, renta, construcciones, anuncios, topografía y resumen).','Fuentes: Base Catastral Pública del Gestor IGAC 09-2026; Zonas Homogéneas Gestor IGAC Vigencias 2026; Resolución IGAC 941 de 2026 y Anexo; POT de Los Patios (Corponor); modelo SRTM 30 m; portales de ofertas.'])
d.save('Avaluo_Helechal_Alto_INFORME_FINAL_BORRADOR.docx')
