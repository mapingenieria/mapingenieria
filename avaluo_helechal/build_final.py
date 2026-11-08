from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
RED=PatternFill("solid",fgColor="FFC7CE"); YEL=PatternFill("solid",fgColor="FFF2CC"); HDR=PatternFill("solid",fgColor="1F4E78"); GRN=PatternFill("solid",fgColor="E2EFDA")
B=Font(bold=True); W=Font(bold=True,color="FFFFFF"); thin=Side(style="thin",color="999999"); BR=Border(left=thin,right=thin,top=thin,bottom=thin)
MON='#,##0'
def hdr(ws,r,vals,c0=1):
    for i,v in enumerate(vals):
        c=ws.cell(r,c0+i,v); c.font=W; c.fill=HDR; c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center"); c.border=BR
def widths(ws,ws_w):
    for i,w in enumerate(ws_w,1): ws.column_dimensions[L(i)].width=w
wb=Workbook()
# ---------- 1 DATOS
ws=wb.active; ws.title="1_Datos"
ws["A1"]="AVALÚO COMERCIAL RURAL - LOTE 1-1 TEQUENDAMA, HELECHAL ALTO, LOS PATIOS - LIBRO DE CÁLCULO CONSOLIDADO"; ws["A1"].font=Font(bold=True,size=14)
ws["A2"]="Leyenda: celda ROJA = supuesto/criterio del perito a revisar y ajustar; AMARILLA = parámetro técnico; VERDE = dato oficial verificado (catastro IGAC). Todo el libro recalcula con fórmulas."
ws["A2"].alignment=Alignment(wrap_text=True); ws.merge_cells("A2:C2"); ws.row_dimensions[2].height=40
rows=[("Predio","LOTE 1-1 TEQUENDAMA HELECHAL ALTO","v"),("Vereda / Municipio / Departamento","Helechal Alto / Los Patios (54405) / Norte de Santander","v"),
("Matrícula inmobiliaria","260-323861 (verificar con certificado de tradición)","r"),("Código catastral (20 dígitos)","54405-00-00-0009-0020-000","v"),("NPN (30 dígitos)","544050000000000090020000000000","v"),
("Área de terreno catastral (ha)",19.5355,"v"),("Área construida catastral (m²)",70,"v"),("Destino económico catastral","D - agropecuario","v"),
("Solicitante","POR CONFIRMAR","r"),("Propietario","POR CONFIRMAR (certificado de tradición)","r"),("Fecha de visita técnica","POR CONFIRMAR (obligatoria, art. 10 Res. 941/2026)","r"),
("Fecha del informe","2026-11-08","y"),("Fecha de corte del estudio de mercado","2026-11-08","y"),
("Marco metodológico","Res. IGAC 941 del 31-jul-2026 y Anexo Técnico (deroga Res. 620/2008)","y"),("Objeto","Determinar el valor comercial del inmueble","y")]
for i,(a,b,t) in enumerate(rows,4):
    ws.cell(i,1,a).font=B; c=ws.cell(i,2,b); c.fill={"v":GRN,"r":RED,"y":YEL}[t]
widths(ws,[40,80,10])
AREA="'1_Datos'!B9"
# ---------- 2 IGAC
wi=wb.create_sheet("2_IGAC_Catastro")
wi["A1"]="REFERENCIA OFICIAL IGAC - ZONAS HOMOGÉNEAS Y VALOR CATASTRAL DEL PREDIO"; wi["A1"].font=Font(bold=True,size=12)
wi["A2"]="Fuentes: Base Catastral Pública del Gestor IGAC 09-2026 (Registros 1-2, R_TERRENO) y Zonas Homogéneas Gestor IGAC Vigencias 2026 (capas R_ZONA_HOMOGENEA_FISICA/GEOECONOMICA; vigencia de las zonas 01-01-2019). Valores CATASTRALES, no comerciales."
wi.merge_cells("A2:H2"); wi["A2"].alignment=Alignment(wrap_text=True); wi.row_dimensions[2].height=45
hdr(wi,4,["Zona física","Zona económica","Área (m²)","Área (ha)","Valor catastral $/ha","Valor catastral terreno ($)","Norma de uso (capa IGAC)","AHT / agua / vía / uso actual"])
zz=[("008","012",28656.79,6000000,"AGROSILVOPASTORIL-DEPORTIVA Y TURISTICA","AHT 09CSd1-38 09CSd1qL-38 / agua escasa / regular 4 (sin pavimentar, angosta) / bosques"),("014","014",162064.2,3000000,"RECREACION TURISTICA-AGROSILVOPASTORIL","AHT 10CSe1-30 10CSe1qL-30 / agua escasa / regular 3 (pavimentada, angosta) / pastos naturales"),("021","016",4633.91,1680000,"AGROSILVOPASTORIL-FORESTAL PROTECCION PRODUCCION","AHT 11MSfqp-23 / agua escasa / regular 3 / bosques")]
for i,(a,b,m,v,n,o) in enumerate(zz):
    r=5+i; wi.cell(r,1,a); wi.cell(r,2,b); wi.cell(r,3,m); wi.cell(r,4,f"=C{r}/10000"); wi.cell(r,5,v); wi.cell(r,6,f"=D{r}*E{r}"); wi.cell(r,7,n); wi.cell(r,8,o)
    for c in (3,5,6): wi.cell(r,c).number_format=MON
    wi.cell(r,4).number_format='0.0000'
wi.cell(8,1,"TOTAL").font=B; wi.cell(8,3,"=SUM(C5:C7)").number_format=MON; wi.cell(8,4,"=SUM(D5:D7)").number_format='0.0000'; wi.cell(8,6,"=SUM(F5:F7)").number_format=MON; wi.cell(8,6).font=B
wi.cell(9,1,"Valor catastral medio $/ha"); wi.cell(9,6,"=F8/D8").number_format=MON
wi["A11"]="Catastro: construcción registrada 70 m² (2 hab., 1 piso, tipificación 2, puntaje 16); no figura la piscina. Norma municipal (PBOT Los Patios, ~2000, no verificado como vigente): pecuaria = ganadería extensiva (principal); recreación y parcelación rural condicionadas; usos urbano/suburbano/industrial prohibidos."
wi["A11"].alignment=Alignment(wrap_text=True); wi.merge_cells("A11:H11"); wi.row_dimensions[11].height=50
widths(wi,[14,14,14,12,20,22,50,70])
# ---------- 3 OFERTAS (copiar)
src=load_workbook('versiones_previas/Ofertas_Reales_Fincas_Cucuta_LosPatios_2026-11-08.xlsx')
so=src['Ofertas_fincas_reales']; wo=wb.create_sheet("3_Ofertas_reales")
for row in so.iter_rows():
    for c in row:
        n=wo.cell(c.row,c.column,c.value)
        if c.row==1: n.font=W; n.fill=HDR
        n.alignment=Alignment(wrap_text=True,vertical="top")
        if c.column in (5,6) and c.row>1: n.number_format=MON
widths(wo,[4,28,22,10,16,16,34,34,16,34,14,18,50,60]); wo.freeze_panes="A2"
wo.cell(so.max_row+2,1,"Precios PEDIDOS capturados el 2026-11-08 (Fincaraíz, Ciencuadras, Nuroa, Mi Plataforma de Negocios). Falta confirmar con cada oferente: fecha, % de negociación, área real y condiciones. Las filas marcadas NO comparable no entran en la homogeneización.")
# ---------- 4 HOMOGENEIZACION
wm=wb.create_sheet("4_Homogeneizacion")
wm["A1"]="MÉTODO DE COMPARACIÓN DE MERCADO (Res. 941/2026 arts. 17-21) - TERRENO DE REFERENCIA (ondulado, pastos, vía regular)"; wm["A1"].font=Font(bold=True,size=12)
wm["A2"]="Factor >1 = la oferta es INFERIOR al terreno de referencia (se le suma valor); <1 = SUPERIOR. Valor de construcciones/cultivos descontado = estimación del perito (rojo). Todos los factores son CRITERIO DEL PERITO a calibrar con ofertas confirmadas; el art. 17 aclara que el método no es una igualación de ofertas."
wm.merge_cells("A2:P2"); wm["A2"].alignment=Alignment(wrap_text=True); wm.row_dimensions[2].height=42
hdr(wm,4,["# oferta (hoja 3)","Descripción","Área (ha)","Precio pedido ($)","F. negociación","Valor oferta negociada ($)","Descuento construcciones/cultivos ($)","Valor terreno ($)","$/ha terreno","F. topografía","F. agua","F. clima/ubicación","F. acceso vial","F. área","$/ha homogeneizado","Observación del ajuste"])
comp=[(1,"Aguaclara, Cúcuta (32 ha plana)",32,1200000000,.90,100000000,.85,.85,1.00,1.00,1.03,"Plana y con agua abundante: superior al predio -> factores a la baja"),
(12,"Chinácota ganadera (41 ha escritura)",41,1500000000,.90,150000000,1.00,.90,.90,1.00,1.05,"Clima y agua mejores; mayor tamaño"),
(13,"Chinácota 54 ha (riego, nacimiento)",54,1200000000,.90,200000000,1.00,.85,.90,1.00,1.08,"Agua abundante y riego; mucho mayor tamaño"),
(11,"Chinácota Palo Colorado (24 ha, café)",24,850000000,.90,250000000,1.00,.95,.90,1.00,1.00,"Se descuenta cultivo permanente y casa"),
(10,"Durania 8 ha (acceso por herradura)",8,230000000,.90,50000000,.95,1.00,.95,1.20,.95,"Acceso muy deficiente -> sube; área pequeña -> baja"),
(9,"Durania 15 ha (casa 300 m²)",15,1300000000,.90,600000000,1.00,1.00,.95,1.00,1.00,"Casa grande: se descuenta su costo depreciado estimado")]
for i,c in enumerate(comp):
    r=5+i; n,d,a,p,fn,desc,ft,fa,fc,fv,far,obs=c
    wm.cell(r,1,n); wm.cell(r,2,d); wm.cell(r,3,a); wm.cell(r,4,p); wm.cell(r,5,fn); wm.cell(r,6,f"=D{r}*E{r}"); wm.cell(r,7,desc); wm.cell(r,8,f"=F{r}-G{r}"); wm.cell(r,9,f"=H{r}/C{r}")
    for j,v in enumerate((ft,fa,fc,fv,far)): wm.cell(r,10+j,v)
    wm.cell(r,15,f"=I{r}*J{r}*K{r}*L{r}*M{r}*N{r}"); wm.cell(r,16,obs)
    for col in (5,7,10,11,12,13,14): wm.cell(r,col).fill=RED
    for col in (4,6,7,8,9,15): wm.cell(r,col).number_format=MON
f,l=5,4+len(comp)
st=[("Promedio ($/ha)",f"=AVERAGE(O{f}:O{l})"),("Mediana ($/ha)",f"=MEDIAN(O{f}:O{l})"),("Desviación estándar",f"=STDEV(O{f}:O{l})"),("Coeficiente de variación (%)",f"=B{l+4}/B{l+2}*100"),
("Límite rural (art. 21) %",10),("Control CV",f'=IF(B{l+5}<=B{l+6},"CUMPLE","NO CUMPLE: sustentar uso de la mediana (art. 21 par. 1) o depurar la muestra")'),
("VALOR ADOPTADO terreno de referencia $/ha",f"=ROUND(IF(B{l+5}<=B{l+6},B{l+2},B{l+3}),-5)")]
for i,(a,b) in enumerate(st):
    wm.cell(l+2+i,1,a).font=B; c=wm.cell(l+2+i,2,b); c.number_format='0.00' if ("%" in a or "Control" in a or "Desv" in a and False) else MON
wm.cell(l+5,2).number_format='0.00'; wm.cell(l+6,2).number_format='0.00'
ADOPT=f"'4_Homogeneizacion'!B{l+8}"
widths(wm,[28,40,10,18,12,18,20,18,16,12,10,14,12,10,18,60])
# ---------- 5 TERRENO
wt=wb.create_sheet("5_Terreno")
wt["A1"]="VALOR DEL TERRENO POR FRANJAS TOPOGRÁFICAS (art. 46 num. 5 Res. 941/2026)"; wt["A1"].font=Font(bold=True,size=12)
wt["A2"]="Áreas por franja = ESTIMACIÓN a medir en campo (suman el área catastral). Factores = criterio del perito respecto al terreno de referencia (ondulado). Ver en la hoja 2 las AHT y zonas oficiales del IGAC."
wt.merge_cells("A2:H2"); wt["A2"].alignment=Alignment(wrap_text=True); wt.row_dimensions[2].height=36
hdr(wt,4,["Franja","Descripción","Pendiente","Área (ha)","Factor vs. referencia","Valor ref. $/ha","Valor ajustado $/ha","Valor franja ($)"])
fr=[("F1","Plano - potrero","0-7 %",4.0,1.15),("F2","Ondulado - potrero","7-25 %",6.0,1.00),("F3","Ladera fuerte - pasto/rastrojo/bosque","> 25 %",None,0.70)]
for i,z in enumerate(fr):
    r=5+i
    for j,v in enumerate(z): wt.cell(r,1+j,v)
    if z[3] is None: wt.cell(r,4,f"={AREA}-D5-D6")
    else: wt.cell(r,4).fill=RED
    wt.cell(r,5).fill=RED; wt.cell(r,6,f"={ADOPT}"); wt.cell(r,7,f"=F{r}*E{r}"); wt.cell(r,8,f"=D{r}*G{r}")
    for c in (6,7,8): wt.cell(r,c).number_format=MON
wt.cell(8,1,"TOTAL").font=B; wt.cell(8,4,"=SUM(D5:D7)").font=B; wt.cell(8,8,"=SUM(H5:H7)").font=B; wt.cell(8,8).number_format=MON
wt.cell(9,1,"Valor promedio $/ha (terreno)"); wt.cell(9,8,"=H8/D8").number_format=MON
widths(wt,[10,42,12,12,18,16,18,20])
# ---------- 6 RENTA
wn=wb.create_sheet("6_Renta_contraste")
wn["A1"]="CONTRASTE: CAPITALIZACIÓN DE INGRESOS - ACTIVIDAD PECUARIA (arts. 46-47; Anexo 4.2, Ecs. 14-17)"; wn["A1"].font=Font(bold=True,size=12)
wn["A2"]="Parámetros SUPUESTOS (aforo, precio, costos, participación de la tierra, tasa 7,3 % tomada del ejemplo del Anexo / Res. 1912 de 2024). Valor/ha = Utilidad x % participación tierra / tasa."
wn.merge_cells("A2:L2"); wn["A2"].alignment=Alignment(wrap_text=True); wn.row_dimensions[2].height=32
hdr(wn,4,["Franja","Área (ha)","Carga (UGG/ha)","Ganancia (kg/UGG/año)","Precio kg en pie ($)","Ingreso $/ha/año","Costos (% ingreso)","Utilidad $/ha/año","% participación tierra","Tasa capitalización","Valor tierra $/ha","Valor franja ($)"])
for i,(z,cc) in enumerate((("F1",1.2),("F2",0.8),("F3",0.3))):
    r=5+i; wn.cell(r,1,z); wn.cell(r,2,f"='5_Terreno'!D{5+i}"); wn.cell(r,3,cc); wn.cell(r,4,200); wn.cell(r,5,7800); wn.cell(r,6,f"=C{r}*D{r}*E{r}"); wn.cell(r,7,.60); wn.cell(r,8,f"=F{r}*(1-G{r})"); wn.cell(r,9,.40); wn.cell(r,10,.073); wn.cell(r,11,f"=H{r}*I{r}/J{r}"); wn.cell(r,12,f"=B{r}*K{r}")
    for c in (3,4,5,7,9,10): wn.cell(r,c).fill=RED
    for c in (5,6,8,11,12): wn.cell(r,c).number_format=MON
    for c in (7,9): wn.cell(r,c).number_format='0%'
    wn.cell(r,10).number_format='0.0%'
wn.cell(8,1,"TOTAL renta").font=B; wn.cell(8,2,"=SUM(B5:B7)"); wn.cell(8,12,"=SUM(L5:L7)").number_format=MON
wn.cell(9,1,"Terreno por comparación ($)"); wn.cell(9,12,"='5_Terreno'!H8").number_format=MON
wn.cell(10,1,"Renta / comparación"); wn.cell(10,12,"=L8/L9").number_format='0.0%'
wn["A12"]="Lectura: la renta ganadera extensiva es muy inferior al mercado; el mercado de fincas cerca de Cúcuta paga ubicación, uso campestre y agua. El perito debe sustentar en el informe por qué adopta la comparación (art. 21 par. 2 y art. 46) o ponderar con la renta si la norma de uso es estrictamente agropecuaria."
wn["A12"].alignment=Alignment(wrap_text=True); wn.merge_cells("A12:L12"); wn.row_dimensions[12].height=55
widths(wn,[20,10,14,16,14,16,12,16,14,14,16,18])
# ---------- 7 CONSTRUCCIONES
wc=wb.create_sheet("7_Construcciones")
wc["A1"]="COSTO DE REPOSICIÓN DEPRECIADO - ROSS-HEIDECK (Res. 941/2026, Anexo 2.3.4, Ecs. 2-5)"; wc["A1"].font=Font(bold=True,size=12)
wc["A2"]="FD = (1 - 0,5 x (x/n + x²/n²)) x E ; E = (100 - coef. Heideck)/100 ; VA = Vn x FD. Coef. Heideck (Tabla 6): 1=0; 1,5=0,032; 2=2,52; 2,5=8,09; 3=18,10; 3,5=33,20; 4=52,60; 4,5=75,20; 5=100 (%)."
wc.merge_cells("A2:N2"); wc["A2"].alignment=Alignment(wrap_text=True); wc.row_dimensions[2].height=32
hdr(wc,4,["Ítem","Descripción","Área / cant.","Unidad","Costo reposición nuevo $/u","Edad x (años)","Vida útil n (años)","Ross","Estado Heideck","Coef. Heideck (%)","E","FD","Valor actual ($)","Sustento"])
tab=[(1,0),(1.5,.032),(2,2.52),(2.5,8.09),(3,18.10),(3.5,33.20),(4,52.60),(4.5,75.20),(5,100)]
hdr(wc,4,["Estado","Coef. (%)"],17)
for k,(a,b) in enumerate(tab): wc.cell(5+k,17,a); wc.cell(5+k,18,b)
items=[("C1","Vivienda campestre, acabados medios (1 piso) - área catastral",70,"m²",2300000,12,70,2,"Área del catastro; el propietario indica vivienda con piscina: MEDIR en campo. Tabla 2: vida larga 70 (mampostería/aporticado)"),
("C2","Piscina (vaso, enchape, equipos)",32,"m²",2000000,10,50,2,"Supuesto: 8x4 m; vida sustentada (nota 3 Tabla 2)"),
("A1","Cercas de alambre de púas, postería (4 hilos)",3500,"ml",9000,8,15,2.5,"Supuesto; no tipificado en Tabla 2"),
("A2","Corral / brete / establo básico",1,"gl",18000000,10,50,2.5,"Supuesto; Tabla 2: vida media 50"),
("A3","Reservorio / tanque y conducciones de agua",1,"gl",12000000,10,50,2.5,"Supuesto; Tabla 2: vida media 50")]
for i,it in enumerate(items):
    r=5+i
    for j,v in enumerate(it[:7]): wc.cell(r,1+j,v)
    wc.cell(r,9,it[7]); wc.cell(r,14,it[8])
    for c in (3,5,6,7,9): wc.cell(r,c).fill=RED
    wc.cell(r,8,f"=0.5*(F{r}/G{r}+(F{r}/G{r})^2)"); wc.cell(r,10,f"=VLOOKUP(I{r},$Q$5:$R$13,2,FALSE)"); wc.cell(r,11,f"=(100-J{r})/100"); wc.cell(r,12,f"=(1-H{r})*K{r}"); wc.cell(r,13,f"=C{r}*E{r}*L{r}")
    for c in (5,13): wc.cell(r,c).number_format=MON
    for c in (8,11,12): wc.cell(r,c).number_format='0.0000'
wc.cell(10,1,"TOTAL CONSTRUCCIONES Y ANEXOS").font=B; wc.cell(10,13,"=SUM(M5:M9)").number_format=MON; wc.cell(10,13).font=B
widths(wc,[6,50,10,7,16,10,10,9,10,10,8,9,16,70,2,2,8,10])
# ---------- 8 ANUNCIOS
sa=load_workbook('versiones_previas/Estudio_Mercado_Anuncios_Fincaraiz_2026-11-08.xlsx')['Anuncios_Fincaraiz']; wa=wb.create_sheet("8_Anuncios_Fincaraiz")
for row in sa.iter_rows():
    for c in row:
        n=wa.cell(c.row,c.column,c.value); n.alignment=Alignment(wrap_text=True,vertical="top")
        if c.row==1: n.font=W; n.fill=HDR
widths(wa,[11,16,22,45,16,14,12,16,12,22,12,11,11,60,14,70]); wa.freeze_panes="A2"
# ---------- 9 RESUMEN
wr=wb.create_sheet("9_Resumen",0)
wr["A1"]="RESUMEN DEL AVALÚO COMERCIAL - LOTE 1-1 TEQUENDAMA, HELECHAL ALTO (BORRADOR PARA AJUSTE DEL PERITO)"; wr["A1"].font=Font(bold=True,size=14)
hdr(wr,3,["Concepto","Valor ($)"])
data=[("Terreno (comparación de mercado, 19,54 ha)","='5_Terreno'!H8"),("Vivienda, piscina y anexos (costo depreciado)","='7_Construcciones'!M10")]
for i,(a,b) in enumerate(data): wr.cell(4+i,1,a); wr.cell(4+i,2,b).number_format=MON
wr.cell(6,1,"VALOR COMERCIAL TOTAL").font=B; wr.cell(6,2,"=B4+B5").number_format=MON; wr.cell(6,2).font=B
wr.cell(7,1,"VALOR ADOPTADO (redondeado a $1.000.000)").font=B; wr.cell(7,2,"=ROUND(B6,-6)").number_format=MON; wr.cell(7,2).font=B; wr.cell(7,2).fill=YEL
wr.cell(8,1,"Valor integral por ha"); wr.cell(8,2,f"=B7/{AREA}").number_format=MON
wr.cell(9,1,"Participación terreno / construcciones"); wr.cell(9,2,'=TEXT(B4/B6,"0%")&" / "&TEXT(B5/B6,"0%")')
wr.cell(11,1,"Sensibilidad (±10 % sobre el terreno)").font=B
wr.cell(12,1,"Límite inferior"); wr.cell(12,2,"=ROUND(B4*0.9+B5,-6)").number_format=MON
wr.cell(13,1,"Límite superior"); wr.cell(13,2,"=ROUND(B4*1.1+B5,-6)").number_format=MON
wr.cell(15,1,"Contrastes del terreno").font=B
wr.cell(16,1,"Valor catastral IGAC del terreno (zonas 2019)"); wr.cell(16,2,"='2_IGAC_Catastro'!F8").number_format=MON
wr.cell(17,1,"Capitalización de renta pecuaria (supuestos)"); wr.cell(17,2,"='6_Renta_contraste'!L8").number_format=MON
wr.cell(18,1,"Terreno por comparación (adoptado)"); wr.cell(18,2,"=B4").number_format=MON
wr.cell(19,1,"CV de la muestra de mercado (%) / límite 10 %"); wr.cell(19,2,f"='4_Homogeneizacion'!B{l+5}").number_format='0.0'
wr.cell(20,1,"Control estadístico"); wr.cell(20,2,f"='4_Homogeneizacion'!B{l+7}")
wr.cell(22,1,"AVISO: borrador con precios PEDIDOS, factores de ajuste y áreas por franja estimados. Reemplazar las celdas rojas con datos verificados (visita técnica, certificado de tradición, uso del suelo, ofertas confirmadas) antes de firmar. El valor del terreno por comparación es muy superior al catastral y a la renta: sustentar en el informe.").font=Font(bold=True,color="C00000")
wr["A22"].alignment=Alignment(wrap_text=True); wr.merge_cells("A22:B22"); wr.row_dimensions[22].height=75
widths(wr,[64,34])
wb.save("Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx")
print("ok",l)
