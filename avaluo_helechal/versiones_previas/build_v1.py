import statistics as st
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

RED=PatternFill("solid",fgColor="FFC7CE"); YEL=PatternFill("solid",fgColor="FFF2CC"); HDR=PatternFill("solid",fgColor="1F4E78")
B=Font(bold=True); W=Font(bold=True,color="FFFFFF"); thin=Side(style="thin",color="999999"); BR=Border(left=thin,right=thin,top=thin,bottom=thin)
MON='#,##0'; 
def hdr(ws,r,vals,c0=1):
    for i,v in enumerate(vals):
        c=ws.cell(r,c0+i,v); c.font=W; c.fill=HDR; c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center"); c.border=BR
wb=Workbook()

# ---------- 1 DATOS
ws=wb.active; ws.title="1_Datos"
ws["A1"]="MEMORIA DE CÁLCULO - AVALÚO COMERCIAL RURAL (PRELIMINAR)"; ws["A1"].font=Font(bold=True,size=14)
ws["A2"]="Celdas ROJAS = dato SUPUESTO/EJEMPLO que debe reemplazarse con la visita técnica, certificado de tradición, ficha predial y ofertas reales. Celdas AMARILLAS = parámetro técnico del perito."
ws["A2"].alignment=Alignment(wrap_text=True); ws.merge_cells("A2:D2"); ws.row_dimensions[2].height=45
rows=[("Predio","LOTE 1-1 TEQUENDAMA"),("Vereda","Helechal Alto"),("Municipio / Departamento","Los Patios, Norte de Santander"),
("Matrícula inmobiliaria","260-323861 (Oficina de Registro de Cúcuta - verificar certificado)"),("Código catastral","54405-00-00-0009-0020-000"),("Área total (ha) - catastral IGAC (195.355 m²)",19.5355),
("Destino económico catastral / área construida","D (agropecuario) / 70 m² (verificar en campo)"),("Propietario / Solicitante","POR CONFIRMAR"),("Objeto del avalúo","Determinar el valor comercial"),("Fecha de visita","POR CONFIRMAR"),("Fecha del informe","2026-11-08"),
("Metodología","Res. IGAC 941 del 31-jul-2026 y su Anexo Técnico (comparación de mercado, renta/capitalización de ingresos como contraste, costo de reposición depreciado con Ross-Heideck)")]
for i,(a,b) in enumerate(rows,4):
    ws.cell(i,1,a).font=B; c=ws.cell(i,2,b)
    if "CONFIRMAR" in str(b) or i==9: c.fill=RED
ws.column_dimensions["A"].width=34; ws.column_dimensions["B"].width=70

# ---------- 2 MERCADO
wm=wb.create_sheet("2_Mercado")
wm["A1"]="MÉTODO DE COMPARACIÓN DE MERCADO (Res. 941/2026 arts. 17-21) - TERRENO (valor/ha del terreno de referencia: ondulado, acceso bueno)"; wm["A1"].font=Font(bold=True,size=12)
wm["A2"]="Factores >1 si la oferta es INFERIOR al sujeto-referencia (se le suma valor); <1 si es superior. DATOS DE EJEMPLO - reemplazar por ofertas/transacciones reales verificadas (mín. 4, recomendable 6+)."
wm.merge_cells("A2:N2")
wm["A3"]="Art. 17: depurar sobre el valor negociado; el método NO es igualación de ofertas, es análisis técnico de las dinámicas del mercado. Art. 19: comparar área, vocación/AHT, clase agrológica, pendiente, infraestructura productiva, norma urbanística y ambiental."
hdr(wm,4,["#","Ubicación (municipio/vereda)","Área (ha)","Valor oferta ($)","Valor construcc. ($)","Valor terreno ($)","$/ha bruto","F. negociación","F. topografía","F. acceso","F. aguas/servicios","F. área","$/ha homogeneizado","Observaciones","Fecha captura","Tipo de dato (oferta/transacción)","Fuente / contacto / URL / captura de pantalla","Coordenadas","AHT / clase agrológica"])
comps=[(15,1050e6,150e6,.94,1.00,1.00,1.00,1.00),(20,1100e6,0,.92,1.10,1.00,1.00,1.03),(8,640e6,90e6,.95,1.00,1.00,1.00,.96),
(25,1250e6,0,.90,1.12,1.03,1.00,1.05),(10,760e6,60e6,.93,1.00,1.00,1.00,.95),(18,1100e6,120e6,.92,1.05,1.00,1.00,1.00)]
for i,c in enumerate(comps):
    r=5+i; wm.cell(r,1,i+1); wm.cell(r,2,f"Oferta {i+1} - Los Patios / Cúcuta rural (EJEMPLO)")
    wm.cell(r,3,c[0]); wm.cell(r,4,c[1]); wm.cell(r,5,c[2])
    wm.cell(r,6,f"=D{r}-E{r}"); wm.cell(r,7,f"=F{r}/C{r}")
    for j in range(5): wm.cell(r,8+j,c[3+j])
    wm.cell(r,13,f"=G{r}*H{r}*I{r}*J{r}*K{r}*L{r}"); wm.cell(r,14,"Dato de ejemplo")
    for cc in (15,16,17,18,19): wm.cell(r,cc,"POR DILIGENCIAR").fill=RED
    for col in range(2,15): wm.cell(r,col).fill=RED if col in(2,3,4,5,8,9,10,11,12) else PatternFill()
    for col in (4,5,6,7,13): wm.cell(r,col).number_format=MON
n=len(comps); f,l=5,4+n
stats=[("Promedio ($/ha)",f"=AVERAGE(M{f}:M{l})"),("Desviación estándar",f"=STDEV(M{f}:M{l})"),("Coeficiente de variación (%)",f"=B{l+3}/B{l+2}*100"),
("Límite inferior (media-1DE)",f"=B{l+2}-B{l+3}"),("Límite superior (media+1DE)",f"=B{l+2}+B{l+3}"),
("Control CV rural ≤ 10 % (Res. 941/2026 art. 21)",f'=IF(B{l+4}<=10,"CUMPLE","NO CUMPLE - depurar muestra / sustentar (art. 21 par. 2)")'),("VALOR ADOPTADO $/ha terreno referencia (promedio)",f"=ROUND(B{l+2},-5)")]
for i,(a,b) in enumerate(stats):
    wm.cell(l+2+i,1,a).font=B; c=wm.cell(l+2+i,2,b); c.number_format=MON if "%" not in a and "Control" not in a else '0.00'
    wm.cell(l+2+i,1).alignment=Alignment(wrap_text=True)
ADOPT=f"'2_Mercado'!B{l+8}"
wm.column_dimensions["A"].width=38; wm.column_dimensions["B"].width=34
for c in range(3,20): wm.column_dimensions[L(c)].width=16
wm.column_dimensions["N"].width=22

# ---------- 3 TERRENO
wt=wb.create_sheet("3_Terreno")
wt["A1"]="VALORACIÓN DEL TERRENO POR FRANJAS / ÁREAS HOMOGÉNEAS DE TIERRA (AHT) - Res. 941/2026 arts. 11 y 46 num. 5"; wt["A1"].font=Font(bold=True,size=12)
hdr(wt,3,["Zona (AHT por identificar)","Descripción","Pendiente","Área (ha)","Factor relativo vs. referencia","Valor ref. $/ha","Valor ajustado $/ha","Valor zona ($)"])
zonas=[("ZF008/ZE012","IGAC: AHT 09CSd1-38; norma agrosilvopastoril-deportiva y turística; uso actual bosques; vía regular sin pavimentar","ver AHT",2.865679,2.00),("ZF014/ZE014","IGAC: AHT 10CSe1-30; norma recreación turística-agrosilvopastoril; uso actual pastos naturales; vía regular pavimentada","ver AHT",16.20642,1.00),("ZF021/ZE016","IGAC: AHT 11MSfqp-23; norma agrosilvopastoril-forestal protección-producción; uso actual bosques","ver AHT",0.463391,0.56)]
for i,z in enumerate(zonas):
    r=4+i
    for j,v in enumerate(z): wt.cell(r,1+j,v)
    wt.cell(r,4).fill=RED; wt.cell(r,5).fill=YEL
    wt.cell(r,6,f"={ADOPT}"); wt.cell(r,7,f"=F{r}*E{r}"); wt.cell(r,8,f"=D{r}*G{r}")
    for c in (6,7,8): wt.cell(r,c).number_format=MON
wt.cell(7,1,"TOTAL").font=B; wt.cell(7,4,"=SUM(D4:D6)").font=B; wt.cell(7,8,"=SUM(H4:H6)").font=B; wt.cell(7,8).number_format=MON
wt.cell(8,1,"Valor promedio $/ha"); wt.cell(8,8,"=H7/D7").number_format=MON
wt.cell(9,1,"Control área vs. declarada (ha)"); wt.cell(9,4,"='1_Datos'!B9-D7")
wt["A11"]="Franjas = zonas físicas/económicas que el catastro del IGAC asigna al predio (Registro 2, base pública 09-2026). Factores = relación de valores/ha catastrales (6,0 / 3,0 / 1,68 millones). El valor de referencia $/ha viene de la muestra de mercado, que hoy es FICTICIA: la columna F no es utilizable hasta reemplazarla."
for c,w in zip("ABCDEFGH",(10,42,12,12,18,16,16,18)): wt.column_dimensions[c].width=w

# ---------- 4 CONSTRUCCIONES
wc=wb.create_sheet("4_Construcciones")
wc["A1"]="COSTO DE REPOSICIÓN DEPRECIADO - ROSS-HEIDECK (Res. 941/2026, Anexo Técnico 2.3.4, Ecs. 2-5)"; wc["A1"].font=Font(bold=True,size=12)
wc["A2"]="FD = (1 - 0,5 x (x/n + x²/n²)) x E ; E = (100 - coef. Heideck)/100 ; VA = Vn x FD (Anexo Ecs. 3-5). Coef. Heideck (Tabla 6): 1=0 ; 1,5=0,032 ; 2=2,52 ; 2,5=8,09 ; 3=18,10 ; 3,5=33,20 ; 4=52,60 ; 4,5=75,20 ; 5=100 (%)."
wc.merge_cells("A2:L2")
hdr(wc,4,["Ítem","Descripción","Área / cant.","Unidad","Costo reposición nuevo $/u","Edad t (años)","Vida útil n (años)","Ross","Estado Heidecke","C Heidecke","Depreciación total (1-FD)","Valor ($)","Sustento vida útil (Tabla 2 Anexo)"])
tab={1:0,1.5:.00032,2:.0252,2.5:.0809,3:.181,3.5:.332,4:.526,4.5:.752,5:1}
items=[("C1","Vivienda campestre, acabados medios (1 piso) - área catastral, verificar",70,"m²",2300000,12,70,2),("C2","Piscina (vaso, enchape, equipos)",32,"m²",2000000,10,50,2),
("A1","Cercas de alambre de púas, postería (4 hilos)",3500,"ml",9000,8,15,2.5),("A2","Corral / brete / establo básico",1,"gl",18000000,10,50,2.5),("A3","Reservorio / tanque y conducciones de agua",1,"gl",12000000,10,50,2.5)]
for i,it in enumerate(items):
    r=5+i
    for j,v in enumerate(it[:7]): wc.cell(r,1+j,v)
    wc.cell(r,9,it[7])
    for c in (3,5,6,7,9): wc.cell(r,c).fill=RED
    wc.cell(r,13,{"C1":"Tabla 2: vida larga 70 (mampostería/aporticado) - confirmar sistema estructural","C2":"Nota 3: vida sustentada (vaso en concreto vs. equipos) - confirmar","A1":"Nota 3: no tipificado en Tabla 2; sustentar","A2":"Tabla 2: vida media 50 (confirmar materiales)","A3":"Tabla 2: vida media 50 (confirmar materiales)"}[it[0]])
    wc.cell(r,8,f"=0.5*(F{r}/G{r}+(F{r}/G{r})^2)")
    wc.cell(r,10,f"=VLOOKUP(I{r},$N$5:$O$13,2,FALSE)")
    wc.cell(r,11,f"=H{r}+(1-H{r})*J{r}"); wc.cell(r,12,f"=C{r}*E{r}*(1-K{r})")
    for c in (5,12): wc.cell(r,c).number_format=MON
    for c in (8,10,11): wc.cell(r,c).number_format='0.00%'
hdr(wc,4,["Estado","C Heidecke"],14)
for k,(a,b) in enumerate(tab.items()): wc.cell(5+k,14,a); wc.cell(5+k,15,b)
last=4+len(items)
wc.cell(last+1,1,"TOTAL CONSTRUCCIONES Y ANEXOS").font=B; wc.cell(last+1,12,f"=SUM(L5:L{last})").number_format=MON; wc.cell(last+1,12).font=B
wc.cell(last+3,1,"Costos de reposición: referencia de mercado de obra 2026 (valores de ejemplo) - actualizar con Construdata / presupuesto de obra y verificar con la visita.")
for c,w in zip("ABCDEFGHIJKLM",(8,46,12,8,18,12,12,10,12,12,14,18,60)): wc.column_dimensions[c].width=w
CONS=f"'4_Construcciones'!L{last+1}"


# ---------- 3b RENTA
wn=wb.create_sheet("3b_Renta_contraste")
wn["A1"]="CONTRASTE: CAPITALIZACIÓN DE INGRESOS - ACTIVIDAD PECUARIA (Res. 941/2026 arts. 46-47; Anexo 4.2, Ecs. 14-17)"; wn["A1"].font=Font(bold=True,size=12)
wn["A2"]="TODOS los parámetros son SUPUESTOS a verificar en campo (aforo/capacidad de carga, precios SIPSA, costos, % participación de la tierra, tasa). Valor = Utilidad x % participación tierra / tasa de capitalización."
wn.merge_cells("A2:L2")
hdr(wn,4,["Zona","Área (ha)","Capacidad de carga (UGG/ha)","Ganancia (kg/UGG/año)","Precio kg en pie ($)","Ingreso $/ha/año","Costos (% ingreso)","Utilidad $/ha/año","% participación tierra","Tasa capitalización","Valor tierra $/ha","Valor zona ($)"])
rz=[("ZF008/ZE012",4,0.4),("ZF014/ZE014",6,0.8),("ZF021/ZE016",8,0.3)]
for i,(z,a,cc) in enumerate(rz):
    r=5+i; wn.cell(r,1,z); wn.cell(r,2,f"='3_Terreno'!D{4+i}"); wn.cell(r,3,cc); wn.cell(r,4,200); wn.cell(r,5,7800)
    wn.cell(r,6,f"=C{r}*D{r}*E{r}"); wn.cell(r,7,.60); wn.cell(r,8,f"=F{r}*(1-G{r})"); wn.cell(r,9,.40); wn.cell(r,10,.073)
    wn.cell(r,11,f"=H{r}*I{r}/J{r}"); wn.cell(r,12,f"=B{r}*K{r}")
    for c in (3,4,5,7,9,10): wn.cell(r,c).fill=RED
    for c in (5,6,8,11,12): wn.cell(r,c).number_format=MON
    wn.cell(r,7).number_format='0%'; wn.cell(r,9).number_format='0%'; wn.cell(r,10).number_format='0.0%'
wn.cell(8,1,"TOTAL renta").font=B; wn.cell(8,2,"=SUM(B5:B7)"); wn.cell(8,12,"=SUM(L5:L7)").number_format=MON
wn.cell(9,1,"Valor terreno por comparación ($)"); wn.cell(9,12,"='3_Terreno'!H7").number_format=MON
wn.cell(10,1,"Relación renta / mercado"); wn.cell(10,12,"=L8/L9").number_format='0.0%'
wn["A12"]="Lectura: si la renta ganadera es muy inferior al mercado, el mercado está pagando uso campestre/ubicación (cercanía a Cúcuta) y no productividad. Esto debe sustentarse con la norma de uso del suelo (agropecuario vs. suburbano/parcelación) y con evidencia de transacciones; si la norma es estrictamente agropecuaria y no hay evidencia de mercado campestre, el art. 47 exige fundamentar el valor en la capacidad de generar ingresos y el peso de este método aumenta."
wn["A12"].alignment=Alignment(wrap_text=True); wn.merge_cells("A12:L12"); wn.row_dimensions[12].height=70
for c,w in zip("ABCDEFGHIJKL",(26,10,16,16,14,16,12,16,14,14,16,18)): wn.column_dimensions[c].width=w


# ---------- 6 IGAC
wi=wb.create_sheet("6_Referencia_IGAC")
wi["A1"]="REFERENCIA OFICIAL IGAC - PREDIO LO 1-1 TEQUENDAMA HELECHAL ALTO"; wi["A1"].font=Font(bold=True,size=12)
wi["A2"]="Fuente: Base Catastral Pública del Gestor IGAC 09-2026 (Registros 1 y 2) y Zonas Homogéneas Gestor IGAC Vigencias 2026 (capas R_ZONA_HOMOGENEA_FISICA / GEOECONOMICA, vigencia de las zonas 01-01-2019). VALORES CATASTRALES, no comerciales."
wi.merge_cells("A2:H2"); wi["A2"].alignment=Alignment(wrap_text=True); wi.row_dimensions[2].height=48
for i,(a,b) in enumerate([("NPN (30 dígitos)","544050000000000090020000000000"),("NPN anterior (20)","54405000000090020000"),("Dirección catastral","Lo 1-1 TEQUENDAMA HELECHAL ALTO"),("Destino económico","D (agropecuario)"),("Área terreno catastral (m²)",195355),("Área construida catastral (m²)",70),("Construcción: habitaciones/pisos/tipificación/puntaje","2 / 1 / 2 / 16 (uso 1 = edificios)")],4):
    wi.cell(i,1,a).font=B; wi.cell(i,2,b)
hdr(wi,12,["Zona física","Zona económica","Área (m²)","Área (ha)","Valor catastral $/ha (zona geoeconómica)","Valor catastral terreno ($)","Norma de uso (capa IGAC)","Agua / vía / uso actual"])
zz=[("008","012",28656.79,6000000,"AGROSILVOPASTORIL-DEPORTIVA Y TURISTICA","Escasas / Regular 4 sin pavimentar, vía angosta / Bosques"),("014","014",162064.2,3000000,"RECREACION TURISTICA-AGROSILVOPASTORIL","Escasas / Regular 3 pavimentada, vía angosta / Pastos naturales"),("021","016",4633.91,1680000,"AGROSILVOPASTORIL-FORESTAL PROTECCION PRODUCCION","Escasas / Regular 3 / Bosques")]
for i,(a,b,m,v,n,o) in enumerate(zz):
    r=13+i; wi.cell(r,1,a); wi.cell(r,2,b); wi.cell(r,3,m); wi.cell(r,4,f"=C{r}/10000"); wi.cell(r,5,v); wi.cell(r,6,f"=D{r}*E{r}"); wi.cell(r,7,n); wi.cell(r,8,o)
    for c in (3,5,6): wi.cell(r,c).number_format=MON
wi.cell(16,1,"TOTAL").font=B; wi.cell(16,3,"=SUM(C13:C15)").number_format=MON; wi.cell(16,4,"=SUM(D13:D15)"); wi.cell(16,6,"=SUM(F13:F15)").number_format=MON; wi.cell(16,6).font=B
wi.cell(17,1,"Valor catastral medio $/ha"); wi.cell(17,6,"=F16/D16").number_format=MON
wi["A19"]="Lectura: el valor catastral del terreno (vigencia 2019, sin los reajustes posteriores) es una REFERENCIA, no el valor comercial. Sirve para contrastar la muestra de mercado: cualquier valor comercial muy por encima de esta cifra requiere comparables de la misma vocación y zona que lo sustenten."
wi["A19"].alignment=Alignment(wrap_text=True); wi.merge_cells("A19:H19"); wi.row_dimensions[19].height=55
for c,w in zip("ABCDEFGH",(36,30,14,12,22,22,52,56)): wi.column_dimensions[c].width=w

# ---------- 5 RESUMEN
wr=wb.create_sheet("5_Resumen")
wr["A1"]="RESUMEN DEL AVALÚO COMERCIAL (PRELIMINAR)"; wr["A1"].font=Font(bold=True,size=14)
hdr(wr,3,["Concepto","Valor ($)"])
data=[("Terreno (19,54 ha, 3 zonas IGAC)","='3_Terreno'!H7"),("Vivienda + piscina + anexos",f"={CONS}")]
for i,(a,b) in enumerate(data): wr.cell(4+i,1,a); wr.cell(4+i,2,b).number_format=MON
wr.cell(6,1,"VALOR COMERCIAL TOTAL").font=B; wr.cell(6,2,"=SUM(B4:B5)").number_format=MON; wr.cell(6,2).font=B
wr.cell(7,1,"Valor total ADOPTADO (redondeado a $1.000.000)").font=B; wr.cell(7,2,"=ROUND(B6,-6)").number_format=MON; wr.cell(7,2).font=B
wr.cell(8,1,"Valor por hectárea (integral)"); wr.cell(8,2,"=B7/'1_Datos'!B9").number_format=MON
wr.cell(9,1,"Participación terreno / construcciones"); wr.cell(9,2,'=TEXT(B4/B6,"0%")&" / "&TEXT(B5/B6,"0%")')
wr.cell(10,1,"Contraste renta pecuaria (terreno) / comparación"); wr.cell(10,2,"='3b_Renta_contraste'!L10").number_format='0.0%'
wr.cell(11,1,"Valor catastral IGAC del terreno (referencia, vigencia 2019)"); wr.cell(11,2,"='6_Referencia_IGAC'!F16").number_format=MON
wr.cell(13,1,"ADVERTENCIA: el valor del terreno parte de una muestra de mercado FICTICIA y NO es utilizable. Referencias reales: catastral IGAC (fila 11) y renta (fila 10). No es avalúo hasta tener comparables reales.").font=Font(bold=True,color="C00000")
wr.column_dimensions["A"].width=58; wr.column_dimensions["B"].width=26
wb.save("/home/user/mapingenieria/avaluo_helechal/Memoria_Calculo_Avaluo_Rural_Helechal_Alto.xlsx")
