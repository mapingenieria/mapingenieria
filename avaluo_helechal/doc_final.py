from docx import Document
from docx.shared import Pt
from openpyxl import load_workbook
wb=load_workbook('/tmp/recalc/Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx',data_only=True)
f=lambda v:f"{v:,.0f}".replace(",",".")
fm=lambda v:f"{v/1e6:,.1f}".replace(",","X").replace(".",",").replace("X",".")
H4=wb['4_Homogeneizacion']; T5=wb['5_Terreno']; N6=wb['6_Renta_contraste']; C7=wb['7_Construcciones']; R9=wb['9_Resumen']; I2=wb['2_IGAC_Catastro']; O3=wb['3_Ofertas_reales']
d=Document(); d.styles['Normal'].font.name='Arial'; d.styles['Normal'].font.size=Pt(10)
H=lambda t,l=1:d.add_heading(t,l); P=d.add_paragraph
def BL(items):
    for s in items: d.add_paragraph(s,style='List Bullet')
def T(rows):
    t=d.add_table(rows=len(rows),cols=len(rows[0])); t.style='Light Grid Accent 1'
    for i,r in enumerate(rows):
        for j,v in enumerate(r): t.cell(i,j).text=str(v)
    d.add_paragraph()
terr=R9['B4'].value; cons=R9['B5'].value; tot=R9['B7'].value; ref=H4['B18'].value
mean,med,sd,cv=H4['B12'].value,H4['B13'].value,H4['B14'].value,H4['B15'].value
cat=I2['F8'].value; ren=N6['L8'].value
d.add_heading('INFORME DE AVALÚO COMERCIAL RURAL',0)
P('LOTE 1-1 TEQUENDAMA – Vereda Helechal Alto, Los Patios (Norte de Santander)\nMatrícula inmobiliaria 260-323861 · Código catastral 54405-00-00-0009-0020-000\nFecha del informe: 8 de noviembre de 2026\nMetodología: Resolución IGAC 941 de 2026 y su Anexo Técnico\nESTADO: BORRADOR PARA AJUSTE Y FIRMA DEL PERITO').runs[0].bold=True
p=P('Este borrador se elaboró con la información disponible: datos oficiales del catastro del IGAC, ofertas publicadas en internet (precios pedidos) y supuestos técnicos del elaborador. No incluye visita técnica ni certificado de tradición. Las cifras deben ser revisadas y ajustadas por el perito avaluador (RAA) antes de su firma; los supuestos están marcados en rojo en el libro de cálculo anexo.'); p.runs[0].bold=True
H('1. Resumen ejecutivo')
T([['Valor comercial total (borrador)','$ '+f(tot)],['Valor del terreno (comparación)','$ '+f(terr)],['Vivienda, piscina y anexos (costo depreciado)','$ '+f(cons)],['Rango por sensibilidad ±10 % del terreno','$ '+f(R9['B12'].value)+' a $ '+f(R9['B13'].value)],['Valor integral por hectárea','$ '+f(R9['B8'].value)],['Valor catastral IGAC del terreno (contraste)','$ '+f(cat)],['Renta pecuaria capitalizada (contraste)','$ '+f(ren)]])
P('Advertencia estadística: el coeficiente de variación de la muestra homogeneizada es %s %%, por encima del 10 %% que el art. 21 de la Resolución 941/2026 admite para inmuebles rurales. Se adoptó la mediana ($%s/ha) con la sustentación del art. 21, parágrafo 1, pero la muestra debe depurarse y ampliarse con ofertas confirmadas antes de firmar.'%(f"{cv:,.1f}".replace(".",","),f(ref)))
H('2. Información básica')
T([['Predio','LOTE 1-1 TEQUENDAMA HELECHAL ALTO'],['Municipio / vereda','Los Patios (54405) / Helechal Alto'],['Matrícula inmobiliaria','260-323861 (verificar con el certificado de tradición)'],['Código catastral','54405-00-00-0009-0020-000 (NPN 544050000000000090020000000000)'],['Destino económico catastral','D – agropecuario'],['Área de terreno catastral','195.355 m² = 19,54 ha'],['Área construida catastral','70 m² (2 habitaciones, 1 piso, tipificación 2, puntaje 16); la piscina no figura'],['Tipo de avalúo','Comercial rural'],['Solicitante / propietario / visita técnica','Por confirmar']])
H('3. Marco normativo y metodológico')
BL(['Resolución IGAC 941 de 2026 (31-jul-2026) y Anexo Técnico: métodos y condiciones de los avalúos. Deroga la Res. 620 de 2008 y el art. 13 e incisos 1-3 del art. 14 de la Res. 898 de 2014 (art. 60). Este avalúo se rige por la 941 (art. 59, transitoriedad).',
'Aplicación: art. 10 (visita técnica), art. 11 (parámetros, AHT, construcciones), art. 14 (informe), arts. 17-19 (comparación), art. 21 (CV rural ≤ 10 %), arts. 46-47 (rurales agropecuarios: costo, comparación y renta; terreno y construcciones por separado).',
'Decreto 1170 de 2015, arts. 2.2.2.3.19 y 2.2.2.3.20; Ley 1673 de 2013 y Decreto 556 de 2014 (RAA).',
'Métodos: comparación de mercado para el terreno; capitalización de ingresos y valor catastral como contrastes; costo de reposición depreciado (Ross-Heideck, Anexo §2.3.4) para construcciones y anexos.',
'La resolución se leyó por OCR de un PDF escaneado y el Anexo como texto: verificar los artículos citados contra el Diario Oficial.'])
H('4. Descripción del predio y norma de uso')
P('Datos oficiales del catastro público del IGAC (09-2026) y de las capas de Zonas Homogéneas (vigencia de zonas: 1-ene-2019):')
T([['Zona física/económica','Área (ha)','AHT','Norma de uso (IGAC)','Valor catastral $/ha']]+[[f"{I2.cell(r,1).value}/{I2.cell(r,2).value}",f"{I2.cell(r,4).value:.2f}",I2.cell(r,8).value.split(' / ')[0].replace('AHT ',''),I2.cell(r,7).value.capitalize(),f(I2.cell(r,5).value)] for r in (5,6,7)])
P('En las tres zonas el IGAC registra agua escasa y vías regulares (angostas; una zona sin pavimentar). El uso actual predominante son pastos naturales (zona 014, 83 % del predio) y bosques en las zonas 008 y 021.')
P('Norma municipal: el Plan Básico de Ordenamiento Territorial de Los Patios (documento de Corponor, plantilla sin número ni fecha, probablemente del año 2000) incluye la vereda El Helechal en el suelo rural. Para zonas pecuarias, el uso principal es la ganadería extensiva; la recreación y las parcelaciones rurales son condicionadas y los usos urbanos, suburbanos e industriales están prohibidos. Conclusión preliminar: suelo rural agropecuario con uso recreativo solo condicionado. Debe confirmarse con el certificado de uso del suelo de Planeación Municipal y el POT/EOT vigente.')
H('5. Estudio de mercado')
P('Se recopilaron ofertas de venta de fincas en Cúcuta, Los Patios, Villa del Rosario, El Zulia, Durania y Chinácota (portales Fincaraíz, Ciencuadras, Nuroa y Mi Plataforma de Negocios; captura del 8-nov-2026). Son precios pedidos. En Los Patios, Villa del Rosario y El Zulia casi no hay fincas agropecuarias publicadas (los 62 anuncios de Fincaraíz son lotes campestres pequeños o terrenos de expansión, no comparables). Por eso se usan fincas de Cúcuta (Aguaclara), Chinácota y Durania, con ajustes por clima, agua, topografía, acceso y área. Resumen de ofertas:')
rows=[['#','Ubicación','Tipo','Área (ha)','Precio pedido ($)','$/ha integral','Comparable']]
for r in range(2,O3.max_row+1):
    if O3.cell(r,1).value is None or not isinstance(O3.cell(r,1).value,int): continue
    p_=O3.cell(r,5).value; a=O3.cell(r,4).value; c=(O3.cell(r,14).value or '')
    rows.append([O3.cell(r,1).value,O3.cell(r,2).value,O3.cell(r,3).value,a,f(p_),f(p_/a),c.split(':')[0][:14]])
T(rows)
H('6. Homogeneización y control estadístico (arts. 17-21)')
P('Para cada oferta se aplicó el factor de negociación (0,90, supuesto), se descontó el valor estimado de construcciones y cultivos, y se ajustó por topografía, agua, clima/ubicación, acceso y área respecto al terreno de referencia (ondulado, pastos, vía regular). Los factores son criterio del elaborador y deben calibrarse.')
T([['Oferta','Área ha','Valor terreno ($)','$/ha','Factores (topo·agua·clima·vía·área)','$/ha homogeneizado']]+[[H4.cell(r,2).value[:34],H4.cell(r,3).value,f(H4.cell(r,8).value),f(H4.cell(r,9).value),'·'.join(f"{H4.cell(r,c).value:g}" for c in (10,11,12,13,14)),f(H4.cell(r,15).value)] for r in range(5,11)])
T([['Promedio',f"$ {f(mean)}/ha"],['Mediana',f"$ {f(med)}/ha"],['Desviación estándar',f"$ {f(sd)}"],['Coeficiente de variación',f"{cv:.1f} % (límite rural 10 %: NO CUMPLE)"],['Valor adoptado, terreno de referencia (mediana)',f"$ {f(ref)}/ha"]])
P('Sustentación (art. 21, par. 1): al no cumplirse el CV, se adopta la mediana por la presencia de valores extremos (Chinácota 54 ha por su gran tamaño y Durania 15 ha por una vivienda de 300 m² cuyo descuento es incierto). El perito debe depurar o ampliar la muestra hasta cumplir el CV o dejar constancia razonada del criterio.')
H('7. Valor del terreno')
T([['Franja','Descripción','Área (ha)','Factor','$/ha','Valor ($)']]+[[T5.cell(r,1).value,T5.cell(r,2).value,f"{T5.cell(r,4).value:.2f}",T5.cell(r,5).value,f(T5.cell(r,7).value),f(T5.cell(r,8).value)] for r in (5,6,7)]+[['TOTAL','',f"{T5.cell(8,4).value:.2f}",'',f(T5['H9'].value),f(terr)]])
P('Las franjas (4 ha planas, 6 ha onduladas, resto en ladera fuerte) son estimaciones según la descripción del predio y deben medirse en campo; sus factores (1,15 / 1,00 / 0,70) son criterio del perito.')
H('8. Contrastes del valor del terreno')
T([['Referencia','Valor terreno ($)','$/ha','Observación'],['Comparación de mercado (adoptado)',f(terr),f(terr/19.5355),'Precios pedidos ajustados'],['Valor catastral IGAC (zonas 2019)',f(cat),f(cat/19.5355),'Referencia oficial, no comercial; vigencia 2019'],['Capitalización de renta pecuaria',f(ren),f(ren/19.5355),'Supuestos: carga 1,2/0,8/0,3 UGG/ha, 200 kg/UGG/año, $7.800/kg, costos 60 %, 40 % tierra, tasa 7,3 %']])
P('El valor por comparación es unas %s veces el catastral y %s veces la renta ganadera. Esa diferencia se explica por el mercado de fincas de recreo y ganadería con agua cerca de Cúcuta, pero con norma de uso agropecuaria el art. 47 exige fundamentar el valor en la capacidad de generar ingresos: el perito debe sustentar la adopción de la comparación o ponderar con la renta.'%(f"{terr/cat:.1f}".replace(".",","),f"{terr/ren:.1f}".replace(".",",")))
H('9. Construcciones y anexos (costo de reposición depreciado)')
P('FD = (1 − ½(x/n + x²/n²)) × E; VA = Vn × FD (Anexo §2.3.4, Tabla 6 de Heideck). Vida útil según Tabla 2 o sustentada (nota 3).')
T([['Ítem','Cant.','Costo nuevo','Edad/Vida','Estado','FD','Valor ($)']]+[[C7.cell(r,2).value[:42],f"{C7.cell(r,3).value:g} {C7.cell(r,4).value}",f(C7.cell(r,5).value),f"{C7.cell(r,6).value}/{C7.cell(r,7).value}",C7.cell(r,9).value,f"{C7.cell(r,12).value:.3f}",f(C7.cell(r,13).value)] for r in range(5,10)]+[['TOTAL','','','','','',f(cons)]])
P('La vivienda usa el área catastral (70 m²), que probablemente está desactualizada; la piscina (32 m²), cercas, corral y reservorio son supuestos. Medir en la visita: el valor de las construcciones puede cambiar de forma importante.')
H('10. Resultado')
T([['Concepto','Valor ($)'],['Terreno',f(terr)],['Construcciones y anexos',f(cons)],['VALOR COMERCIAL TOTAL',f(R9['B6'].value)],['Valor adoptado (redondeado a $1.000.000)',f(tot)],['Valor integral por hectárea',f(R9['B8'].value)]])
H('11. Limitaciones y pendientes')
BL(['No se realizó visita técnica (obligatoria, art. 10): medir áreas por franja, vivienda, piscina y anexos; verificar estado, potreros, agua, accesos y servidumbres.','Certificado de tradición y libertad (260-323861): propietario, título, gravámenes, limitaciones y servidumbres.','Certificado de uso del suelo expedido por Planeación Municipal y verificación del POT/EOT vigente y de determinantes ambientales (rondas hídricas, Corponor).','Ofertas confirmadas con los oferentes (fecha, % de negociación, área real, topografía y agua) y más datos de Los Patios, Villa del Rosario y El Zulia; verificar la área escriturada vs. medida de cada oferta.','Los factores de ajuste, los descuentos de construcciones/cultivos y los parámetros de renta son supuestos del elaborador.','Entrega de la información al Observatorio Inmobiliario Catastral del IGAC (art. 58) y datos del solicitante, marco jurídico del encargo, firma y RAA del avaluador (art. 14).','Verificar si la Res. 941/2026 regula la vigencia del avalúo (no se encontró en el texto leído).'])
H('12. Anexos')
BL(['Libro de cálculo consolidado: Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx (datos, catastro IGAC, ofertas, homogeneización, terreno, renta, construcciones, anuncios y resumen).','Fuentes: Base Catastral Pública del Gestor IGAC 09-2026; Zonas Homogéneas Gestor IGAC Vigencias 2026; Resolución IGAC 941 de 2026 y Anexo; POT de Los Patios (Corponor); portales de ofertas.'])
d.save('Avaluo_Helechal_Alto_INFORME_FINAL_BORRADOR.docx')
