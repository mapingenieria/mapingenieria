from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
RED=PatternFill("solid",fgColor="FFF2CC"); YEL=PatternFill("solid",fgColor="D9D9D9"); HDR=PatternFill("solid",fgColor="404040"); GRN=PatternFill("solid",fgColor="EDEDED")
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
wi.cell(10,1,"Perímetro del polígono catastral (m)").font=B; wi.cell(10,6,2162.5).number_format='#,##0.0'
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
wt["A2"]="Áreas por franja = pendientes calculadas con el modelo SRTM sobre el polígono catastral (hoja 9_Topografia; la franja escarpada es el saldo hasta el área catastral). Factores = criterio del perito respecto al terreno de referencia (ondulado); a calibrar con ofertas. Ver en la hoja 2 las AHT y zonas oficiales del IGAC."
wt.merge_cells("A2:H2"); wt["A2"].alignment=Alignment(wrap_text=True); wt.row_dimensions[2].height=36
hdr(wt,4,["Franja","Descripción","Pendiente","Área (ha)","Factor vs. referencia","Valor ref. $/ha","Valor ajustado $/ha","Valor franja ($)"])
fr=[("F1","Ondulado - pastos","12-25 %",4.81,1.00),("F2","Quebrado - pastos y rastrojo","25-50 %",13.19,0.80),("F3","Escarpado - rastrojo y bosque","> 50 %",None,0.60)]
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
for i,(z,cc) in enumerate((("F1",0.8),("F2",0.5),("F3",0.25))):
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
items=[("C1","Casa principal (cubierta azul), acabados medios; el catastro registra solo 70 m² en total",145,"m²",2300000,12,70,2,"Total de construcciones ≈ 300 m² (rango 285-320 m², dato aportado), repartido según la imagen aérea; piscina aparte. MEDIR en campo. Tabla 2: vida larga 70"),
("C2","Piscina (vaso, enchape, equipos)",32,"m²",2000000,10,50,2,"Estimado de la imagen (8x4 m); vida sustentada (nota 3 Tabla 2)"),
("C3","Bodega / galpón de cubierta metálica gris",95,"m²",900000,8,50,2.5,"Reparto según la imagen (≈ 32 % del área construida); estructura metálica liviana, Tabla 2: vida media 50"),
("C4","Casa o anexo menor (parte baja, cubierta clara)",32,"m²",1500000,15,50,2.5,"Reparto según la imagen; confirmar uso y materiales"),
("C5","Construcciones menores (cubiertas rojas junto a la casa)",28,"m²",1200000,12,50,2.5,"Reparto según la imagen; confirmar uso y materiales"),
("A1","Cercas de alambre de púas, postería (4 hilos) = 85 % del perímetro catastral",None,"ml",9000,8,15,2.5,"Perímetro del polígono IGAC 2.162 m (hoja 2) x 85 % cercado (supuesto: sin cerca en quebradas/vía/lindero en disputa); sin cercas internas"),
("A2","Corral / brete / establo básico",1,"gl",18000000,10,50,2.5,"Supuesto; Tabla 2: vida media 50"),
("A3","Estanques / reservorios (2 visibles en la imagen) y conducciones de agua",1,"gl",12000000,10,50,2.5,"Fotointerpretación: 2 espejos de agua; supuesto de costo global")]
for i,it in enumerate(items):
    r=5+i
    for j,v in enumerate(it[:7]): wc.cell(r,1+j,v)
    if it[0]=="A1": wc.cell(r,3,"=ROUND('2_IGAC_Catastro'!F10*0.85,0)")
    wc.cell(r,9,it[7]); wc.cell(r,14,it[8])
    for c in (3,5,6,7,9): wc.cell(r,c).fill=RED
    wc.cell(r,8,f"=0.5*(F{r}/G{r}+(F{r}/G{r})^2)"); wc.cell(r,10,f"=VLOOKUP(I{r},$Q$5:$R$13,2,FALSE)"); wc.cell(r,11,f"=(100-J{r})/100"); wc.cell(r,12,f"=(1-H{r})*K{r}"); wc.cell(r,13,f"=C{r}*E{r}*L{r}")
    for c in (5,13): wc.cell(r,c).number_format=MON
    for c in (8,11,12): wc.cell(r,c).number_format='0.0000'
wc.cell(13,1,"TOTAL CONSTRUCCIONES Y ANEXOS").font=B; wc.cell(13,13,"=SUM(M5:M12)").number_format=MON; wc.cell(13,13).font=B
widths(wc,[6,50,10,7,16,10,10,9,10,10,8,9,16,70,2,2,8,10])
# ---------- 8 ANUNCIOS
sa=load_workbook('versiones_previas/Estudio_Mercado_Anuncios_Fincaraiz_2026-11-08.xlsx')['Anuncios_Fincaraiz']; wa=wb.create_sheet("8_Anuncios_Fincaraiz")
for row in sa.iter_rows():
    for c in row:
        n=wa.cell(c.row,c.column,c.value); n.alignment=Alignment(wrap_text=True,vertical="top")
        if c.row==1: n.font=W; n.fill=HDR
widths(wa,[11,16,22,45,16,14,12,16,12,22,12,11,11,60,14,70]); wa.freeze_panes="A2"
# ---------- 9 RESUMEN

# ---------- 9 TOPOGRAFIA
wp=wb.create_sheet("9_Topografia")
wp["A1"]="TOPOGRAFÍA DEL PREDIO - PENDIENTES CALCULADAS SOBRE EL POLÍGONO CATASTRAL (SRTM 30 m)"; wp["A1"].font=Font(bold=True,size=12)
wp["A2"]="Método: 525 elevaciones SRTM de 30 m (api.opentopodata.org) sobre el polígono del catastro IGAC; pendiente por el método de Horn (3x3); remuestreo a 5 m; clases agrológicas del IGAC. Es una estimación orientativa: confirmar con levantamiento topográfico, LiDAR o dron. Los puntos de lindero en disputa del propietario no se usan."
hdr(wp,4,["Clase","Rango de pendiente (%)","Descripción","% del predio","Área (ha)"])
cls=[("a","0 - 3","Plano",0.0),("b","3 - 7","Ligeramente inclinado",0.0),("c","7 - 12","Moderadamente inclinado",0.001),("d","12 - 25","Ondulado (fuertemente inclinado)",0.245),("e","25 - 50","Quebrado",0.675),("f","50 - 75","Escarpado",0.079),("g","> 75","Muy escarpado",0.0)]
for i,(a,b,c,p) in enumerate(cls):
    r=5+i; wp.cell(r,1,a); wp.cell(r,2,b); wp.cell(r,3,c); wp.cell(r,4,p); wp.cell(r,5,f"=D{r}*{AREA}")
    wp.cell(r,4).number_format='0.0%'; wp.cell(r,5).number_format='0.00'
wp.cell(12,1,"TOTAL").font=B; wp.cell(12,4,"=SUM(D5:D11)").number_format='0.0%'; wp.cell(12,5,"=SUM(E5:E11)").number_format='0.00'
for i,(a,b) in enumerate((("Pendiente media / mediana (%)","32,5 / 32,2"),("Percentiles 10 y 90 de la pendiente (%)","20,6 / 47,2"),("Cota mínima / máxima (m s.n.m.)","842 / 998"),("Desnivel (m)","≈ 156"),("Orientación predominante de las laderas","Occidente y suroccidente (≈ 90 %)"),("Incertidumbre (error vertical 6 m, Monte Carlo, p5-p95)","12-25 %: 17-27 % | 25-50 %: 62-74 % | >50 %: 6-11 %"))):
    wp.cell(14+i,1,a).font=B; wp.cell(14+i,2,b)
hdr(wp,21,["Zona IGAC (física)","Área (ha)","Pendiente media (%)","12-25 %","25-50 %","> 50 %","Norma de uso"])
for i,z in enumerate((("008",2.86,23,.76,.24,0,"Agrosilvopastoril, deportiva y turística"),("014",16.20,34,.15,.75,.10,"Recreación turística-agrosilvopastoril"),("021",0.48,29,.23,.77,0,"Agrosilvopastoril-forestal protección-producción"))):
    r=22+i
    for j,v in enumerate(z): wp.cell(r,1+j,v)
    for j in (4,5,6): wp.cell(r,j).number_format='0%'
wp["A26"]="Contraste: perfiles en Google Earth (usuario): inclinación mediana 8,2° (14 %) y 12,4° (22 %), máxima 22° (40 %) y 40,8° (86 %). Sus líneas cruzan las curvas de nivel en diagonal, por lo que subestiman la pendiente máxima. Conclusión: topografía ondulada a quebrada, sin terreno plano; valuación por franjas ondulado / quebrado / escarpado."
wp["A27"]="La hoja 5_Terreno usa estas áreas: ondulado 4,81 ha (clases c y d), quebrado 13,19 ha y escarpado el saldo (1,54 ha), con factores 1,00 / 0,80 / 0,60 (criterio del perito)."
widths(wp,[36,24,36,14,14,14,50])

wr=wb.create_sheet("0_Resumen",0)
wr["A1"]="RESUMEN DEL AVALÚO COMERCIAL - LOTE 1-1 TEQUENDAMA, HELECHAL ALTO (BORRADOR PARA AJUSTE DEL PERITO)"; wr["A1"].font=Font(bold=True,size=14)
hdr(wr,3,["Concepto","Valor ($)"])
data=[("Terreno (comparación de mercado, 19,54 ha)","='5_Terreno'!H8"),("Vivienda, piscina y anexos (costo depreciado)","='7_Construcciones'!M13")]
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
wr.cell(22,1,"AVISO: borrador con precios PEDIDOS, factores de ajuste y áreas por franja estimados. Reemplazar las celdas rojas con datos verificados (visita técnica, certificado de tradición, uso del suelo, ofertas confirmadas) antes de firmar. El valor del terreno por comparación es muy superior al catastral y a la renta: sustentar en el informe.").font=Font(bold=True,color="000000")
wr["A22"].alignment=Alignment(wrap_text=True); wr.merge_cells("A22:B22"); wr.row_dimensions[22].height=75
widths(wr,[64,34])

# ================= PRESENTACIÓN =================
from openpyxl.worksheet.properties import PageSetupProperties
from openpyxl.styles import Font as F2
NAVY="262626"; LIGHT=PatternFill("solid",fgColor="EDEDED"); GREY=PatternFill("solid",fgColor="F2F2F2"); TOT=PatternFill("solid",fgColor="D9D9D9")
BODY=F2(name="Calibri",size=10)
def box(ws,rng):
    for row in ws[rng]:
        for c in row:
            c.border=BR
            if c.font is None or (not c.font.b and c.font.color is None): c.font=BODY
            if c.alignment is None or not c.alignment.wrap_text:
                c.alignment=Alignment(vertical="center",wrap_text=True,horizontal=c.alignment.horizontal if c.alignment else None)
def title(ws,cell,span,h=30):
    ws[cell].font=F2(name="Calibri",size=14,bold=True,color="FFFFFF"); ws[cell].fill=PatternFill("solid",fgColor=NAVY)
    ws[cell].alignment=Alignment(vertical="center",wrap_text=True)
    r=ws[cell].row; ws.merge_cells(f"{cell}:{span}{r}") if span else None
    ws.row_dimensions[r].height=h
    if span:
        for c in ws[f"{cell}:{span}{r}"][0]: c.fill=PatternFill("solid",fgColor=NAVY)
def note(ws,cell,span,h):
    r=ws[cell].row
    try: ws.merge_cells(f"{cell}:{span}{r}")
    except Exception: pass
    ws[cell].font=F2(name="Calibri",size=9,italic=True,color="404040"); ws[cell].alignment=Alignment(wrap_text=True,vertical="top")
    ws[cell].fill=GREY; ws.row_dimensions[r].height=h
def page(ws,titles=None,landscape=True):
    ws.page_setup.orientation="landscape" if landscape else "portrait"; ws.page_setup.paperSize=9
    ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0
    ws.sheet_properties.pageSetUpPr=PageSetupProperties(fitToPage=True)
    ws.page_margins.left=ws.page_margins.right=0.4; ws.page_margins.top=ws.page_margins.bottom=0.5
    ws.print_options.horizontalCentered=True
    if titles: ws.print_title_rows=titles
    ws.oddFooter.center.text="Avalúo Lote 1-1 Tequendama - Helechal Alto - Borrador  |  Pág. &P de &N"
    ws.sheet_view.zoomScale=90
def hh(ws,r,h=42): ws.row_dimensions[r].height=h
# --- Resumen
ws=wb["0_Resumen"]; ws.sheet_view.showGridLines=False
ws.unmerge_cells("A22:B22") if "A22:B22" in [str(m) for m in ws.merged_cells.ranges] else None
for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))
ws["A1"].value="RESUMEN DEL AVALÚO COMERCIAL - LOTE 1-1 TEQUENDAMA, HELECHAL ALTO"; title(ws,"A1","D",34)
ws["A2"].value="Los Patios (Norte de Santander) · Matrícula 260-323861 · Código catastral 54405-00-00-0009-0020-000 · Res. IGAC 941/2026 · Borrador del 8-nov-2026 para ajuste del perito"
note(ws,"A2","D",30)
for r in (3,): 
    for c in ws[f"A{r}:B{r}"][0]: c.font=W; c.fill=HDR
ws["B3"].alignment=Alignment(horizontal="center")
box(ws,"A3:B9"); box(ws,"A11:B13"); box(ws,"A15:B20")
for r in (4,5,8,12,13,16,17,18):
    ws.cell(r,2).number_format='"$" #,##0'
for r in (6,7):
    for c in (1,2): ws.cell(r,c).font=F2(name="Calibri",size=11,bold=True); ws.cell(r,c).fill=LIGHT
ws.cell(7,2).number_format='"$" #,##0'; ws.cell(6,2).number_format='"$" #,##0'; ws.cell(7,1).fill=TOT; ws.cell(7,2).fill=TOT; ws.cell(7,2).font=F2(name="Calibri",size=12,bold=True,color="000000")
for r in (11,15):
    ws.cell(r,1).font=F2(name="Calibri",size=10,bold=True,color="FFFFFF"); ws.cell(r,1).fill=PatternFill("solid",fgColor="595959"); ws.cell(r,2).fill=PatternFill("solid",fgColor="595959")
ws.cell(19,2).number_format='0.0" %"'; ws.cell(19,2).alignment=Alignment(horizontal="right",vertical="center")
ws.cell(20,2).alignment=Alignment(wrap_text=True,vertical="center"); ws.row_dimensions[20].height=44
ws.cell(9,2).alignment=Alignment(horizontal="right",vertical="center")
ws.column_dimensions["A"].width=60; ws.column_dimensions["B"].width=38; ws.column_dimensions["C"].width=4; ws.column_dimensions["D"].width=4
ws["A22"].value="AVISO: borrador con precios PEDIDOS, factores de ajuste y áreas por franja estimados. Reemplazar las celdas rojas con datos verificados (visita técnica, certificado de tradición, uso del suelo, ofertas confirmadas) antes de firmar. El valor del terreno por comparación es muy superior al catastral y a la renta: sustentar en el informe."
ws.merge_cells("A22:B22"); ws["A22"].font=F2(name="Calibri",size=10,bold=True,color="000000"); ws["A22"].alignment=Alignment(wrap_text=True,vertical="top"); ws["A22"].fill=PatternFill("solid",fgColor="F2F2F2"); ws.row_dimensions[22].height=62
ws["A24"].value="CONTENIDO DEL LIBRO (clic para ir a la hoja)"; ws["A24"].font=F2(name="Calibri",size=10,bold=True,color="FFFFFF"); ws["A24"].fill=PatternFill("solid",fgColor="595959"); ws["B24"].fill=PatternFill("solid",fgColor="595959")
idx=[("1_Datos","Identificación del predio y datos del encargo"),("2_IGAC_Catastro","Catastro IGAC: zonas, norma de uso y valor catastral"),("3_Ofertas_reales","15 ofertas de fincas capturadas en internet"),("4_Homogeneizacion","Comparación de mercado, factores y control del CV"),("5_Terreno","Valor del terreno por franjas"),("6_Renta_contraste","Contraste por capitalización de rentas"),("7_Construcciones","Vivienda, piscina y anexos (Ross-Heideck)"),("8_Anuncios_Fincaraiz","62 anuncios de Fincaraíz clasificados"),("9_Topografia","Pendientes y altitudes del predio (SRTM)")]
for i,(n,d) in enumerate(idx):
    r=25+i; c=ws.cell(r,1,f"{n}"); c.hyperlink=f"#'{n}'!A1"; c.font=F2(name="Calibri",size=10,color="000000",underline="single"); ws.cell(r,2,d).font=BODY
    ws.cell(r,1).border=BR; ws.cell(r,2).border=BR; ws.cell(r,2).alignment=Alignment(wrap_text=True,vertical="center")
ws.cell(34,1,"Leyenda de colores").font=F2(name="Calibri",size=10,bold=True)
for i,(fill,t) in enumerate(((RED,"Supuesto / criterio del perito: revisar y ajustar"),(YEL,"Parámetro técnico o valor adoptado"),(GRN,"Dato oficial verificado (catastro IGAC)"))):
    ws.cell(35+i,1,t).fill=fill; ws.cell(35+i,1).border=BR; ws.cell(35+i,1).font=BODY
page(ws,landscape=False); ws.sheet_properties.tabColor="7F7F7F"
# --- 1_Datos
ws=wb["1_Datos"]; ws.sheet_view.showGridLines=False
ws["A1"].value="DATOS DEL PREDIO Y DEL ENCARGO"; title(ws,"A1","C",30)
for m in list(ws.merged_cells.ranges):
    if str(m)=="A2:C2": ws.unmerge_cells(str(m))
note(ws,"A2","C",42)
box(ws,"A4:B18")
for r in range(4,19): ws.cell(r,1).fill=LIGHT
ws.column_dimensions["A"].width=42; ws.column_dimensions["B"].width=84; ws.column_dimensions["C"].width=3
for r in range(4,19): ws.row_dimensions[r].height=20
ws["B9"].number_format='0.0000" ha"'; ws["B9"].alignment=Alignment(horizontal="left",vertical="center"); ws["B10"].alignment=Alignment(horizontal="left",vertical="center")
page(ws,landscape=False); ws.sheet_properties.tabColor="7F7F7F"
# --- 2_IGAC
ws=wb["2_IGAC_Catastro"]; ws.sheet_view.showGridLines=False
title(ws,"A1","H",30); 
for m in list(ws.merged_cells.ranges):
    if str(m) in("A2:H2","A11:H11"): ws.unmerge_cells(str(m))
note(ws,"A2","H",42); note(ws,"A11","H",54)
hh(ws,4,36); box(ws,"A4:H9")
for r in (5,6,7):
    for c in (1,2,3,4,5,6): ws.cell(r,c).fill=GRN
for c in (1,3,4,6): ws.cell(8,c).fill=TOT
ws["A9"].font=F2(name="Calibri",size=10,bold=True)
for r in (5,6,7): ws.row_dimensions[r].height=34
ws.column_dimensions["G"].width=46; ws.column_dimensions["H"].width=62
page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
# --- 3_Ofertas
ws=wb["3_Ofertas_reales"]
last=ws.max_row-2
hh(ws,1,48); box(ws,f"A1:N{last}")
for c in ws[1]: c.font=W; c.fill=HDR; c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
for r in range(2,last+1):
    ws.row_dimensions[r].height=78
    comp=str(ws.cell(r,14).value or "")
    ws.cell(r,14).fill=PatternFill("solid",fgColor="EDEDED" if comp.startswith(("MEDIA","POSIBLE")) else ("F2F2F2" if comp.startswith("BAJA") else "FFF2CC"))
    ws.cell(r,5).number_format='"$" #,##0'; ws.cell(r,6).number_format='"$" #,##0'
note(ws,f"A{ws.max_row}","N",34)
ws.freeze_panes="C2"; page(ws,"1:1"); ws.sheet_properties.tabColor="7F7F7F"
# --- 4_Homog
ws=wb["4_Homogeneizacion"]; ws.sheet_view.showGridLines=False
for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))
title(ws,"A1","P",30); note(ws,"A2","P",44)
hh(ws,4,58); box(ws,"A4:P10")
for r in range(5,11): ws.row_dimensions[r].height=40
box(ws,"A12:B18")
for r in range(12,19): ws.cell(r,1).fill=LIGHT
for c in (1,2): ws.cell(18,c).fill=TOT; ws.cell(18,c).font=F2(name="Calibri",size=11,bold=True)
ws["B14"].number_format='"$" #,##0'; ws["B12"].number_format='"$" #,##0'; ws["B13"].number_format='"$" #,##0'; ws["B18"].number_format='"$" #,##0'
ws["B15"].number_format='0.0" %"'; ws["B16"].number_format='0" %"'
ws["B17"].alignment=Alignment(wrap_text=True,vertical="center"); ws.row_dimensions[17].height=48
for r in range(5,11):
    for c in (4,6,7,8,9,15): ws.cell(r,c).number_format='"$" #,##0'
    for c in (10,11,12,13,14,5): ws.cell(r,c).number_format='0.00'
ws.column_dimensions["A"].width=40; ws.column_dimensions["B"].width=46
for r in range(5,11): ws.cell(r,1).alignment=Alignment(horizontal="center",vertical="center")
ws.freeze_panes="C5"; page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
# --- 5_Terreno
ws=wb["5_Terreno"]; ws.sheet_view.showGridLines=False
for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))
title(ws,"A1","H",30); note(ws,"A2","H",38); hh(ws,4,36); box(ws,"A4:H9")
for r in (5,6,7): ws.row_dimensions[r].height=28; ws.cell(r,4).number_format='0.00'; ws.cell(r,5).number_format='0.00'
for c in range(1,9): ws.cell(8,c).fill=TOT
ws.merge_cells("A9:G9"); ws["A9"].alignment=Alignment(horizontal="right",vertical="center"); ws["A9"].font=F2(name="Calibri",size=10,bold=True); ws.row_dimensions[9].height=22
ws["H8"].number_format='"$" #,##0'; ws["H9"].number_format='"$" #,##0'; ws["D8"].number_format='0.00'
for r in (5,6,7):
    for c in (6,7,8): ws.cell(r,c).number_format='"$" #,##0'
page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
# --- 6_Renta
ws=wb["6_Renta_contraste"]; ws.sheet_view.showGridLines=False
for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))
title(ws,"A1","L",30); note(ws,"A2","L",34); note(ws,"A12","L",58); hh(ws,4,48); box(ws,"A4:L10")
for r in (5,6,7):
    ws.row_dimensions[r].height=26; ws.cell(r,2).number_format='0.00'
    for c in (6,8,11,12): ws.cell(r,c).number_format='"$" #,##0'
for c in range(1,13): ws.cell(8,c).fill=TOT
for rr in (9,10):
    ws.merge_cells(f"A{rr}:K{rr}"); ws[f"A{rr}"].alignment=Alignment(horizontal="right",vertical="center"); ws[f"A{rr}"].font=F2(name="Calibri",size=10,bold=True); ws.row_dimensions[rr].height=22
ws["L8"].number_format='"$" #,##0'; ws["L9"].number_format='"$" #,##0'; ws["B8"].number_format='0.00'; ws["L10"].number_format='0.0%'
page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
# --- 7_Construcciones
ws=wb["7_Construcciones"]; ws.sheet_view.showGridLines=False
for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))
title(ws,"A1","N",30); note(ws,"A2","N",38); hh(ws,4,48); box(ws,"A4:N13"); box(ws,"Q4:R13")
for r in range(5,13): ws.row_dimensions[r].height=40
for c in range(1,15): ws.cell(13,c).fill=TOT
ws.merge_cells("A13:L13"); ws["A13"].alignment=Alignment(horizontal="right",vertical="center"); ws["A13"].font=F2(name="Calibri",size=11,bold=True); ws.row_dimensions[13].height=24
ws["M13"].number_format='"$" #,##0'
for r in range(5,13):
    for c in (5,13): ws.cell(r,c).number_format='"$" #,##0'
    ws.cell(r,3).number_format='#,##0'
ws.column_dimensions["Q"].width=10; ws.column_dimensions["R"].width=12; ws.column_dimensions["O"].width=3; ws.column_dimensions["P"].width=3
ws.freeze_panes="C5"; page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
# --- 8_Anuncios
ws=wb["8_Anuncios_Fincaraiz"]
hh(ws,1,48); box(ws,f"A1:P{ws.max_row}")
for c in ws[1]: c.font=W; c.fill=HDR; c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
for r in range(2,ws.max_row+1):
    ws.row_dimensions[r].height=48
    for c in (5,7,8): ws.cell(r,c).number_format='"$" #,##0'
ws.freeze_panes="E2"; ws.auto_filter.ref=f"A1:P{ws.max_row}"; page(ws,"1:1"); ws.sheet_properties.tabColor="7F7F7F"
ws=wb["9_Topografia"]; ws.sheet_view.showGridLines=False
title(ws,"A1","G",30); note(ws,"A2","G",58); hh(ws,4,32); box(ws,"A4:E12"); box(ws,"A14:B19"); hh(ws,21,32); box(ws,"A21:G24")
for r in range(14,20): ws.cell(r,1).fill=LIGHT
for c in range(1,6): ws.cell(12,c).fill=TOT
for r in (8,9): 
    for c in range(1,6): ws.cell(r,c).fill=PatternFill("solid",fgColor="F2F2F2")
note(ws,"A26","G",58); note(ws,"A27","G",30)
ws["B14"].alignment=Alignment(wrap_text=True,vertical="center"); ws.row_dimensions[19].height=34
page(ws,"4:4"); ws.sheet_properties.tabColor="7F7F7F"
wb.active=0

wb.save("Avaluo_Helechal_Alto_LIBRO_CONSOLIDADO.xlsx")
print("ok",l)
