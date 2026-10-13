"""A2 con el foso según la planta de 2.º nivel y la escalera EXISTENTE respetada.
Hueco libre ~0,2 a 1,9 m al sur del eje de D5 (1,70 m); con muros de 0,20 m la huella exterior va de 0,0 a 2,1 m
(la escalera arranca ~2,13 m). Zapata Z1 recortada hasta y = 0,0; el cajón (2,90 x 2,10) toma el resto.
VC eje 5 de 0,40 x 1,00; restricción x3; P_D5 = 85 t; vecinas con reparto tributario (supuesto).
Uso: PYTHONPATH=. python3 caso_A2_planta.py"""
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
m.SUPER_MULT = 3.0
Q, Z = m.QADM_CLAY, 2.0
over = {"VC eje 5 (A-C)": (0.40, 1.0), "VC eje 5 (C-D)": (0.40, 1.0)}
pa = lambda bx, a, b: dict(Bx=bx, By=b - a, yoff=(a + b) / 2, ks=m.KS_CLAY)
CASOS = {"V0 Z1 2x2 original": [pa(Z, -1.0, 1.0)],
         "A2 (planta): zapata hasta y=0,0 + cajón 0,0-2,1": [pa(Z, -1.0, 0.0), pa(2.9, 0.0, 2.1)]}
for nombre, pats in CASOS.items():
    foot = {f"{c}{a}": dict(m.Z1, Bx=Z, By=Z) for c in "AD" for a in m.YAX}
    foot["D5"] = pats
    p = m.post(m.solve_nt(foot, over, loads=m.column_loads(m.W_TOTAL)))
    f, d5 = p["footings"], p["footings"]["D5"]
    print(f"\n{nombre}")
    print("  p_max/q_adm  D5 {:.2f} | D3 {:.2f} | A3 {:.2f} | A5 {:.2f} | D6 {:.2f}".format(
        d5["p_max"] / Q, f["D3"]["p_max"] / Q, f["A3"]["p_max"] / Q, f["A5"]["p_max"] / Q, f["D6"]["p_max"] / Q))
    print("  contacto D5 {:.2f} ; M_exc {:.0f} kN·m ; asent. D5 {:.1f} mm".format(
        d5["contact_frac"], abs(d5["e_x"]) * d5["R"], d5["settle_mm"]))
    if len(d5["patches"]) > 1:
        for nm, pt in zip(("zapata norte", "cajón"), d5["patches"]):
            print(f"  {nm:13s} {pt['R']/d5['R']*100:3.0f} % de la carga  p_max={pt['p_max']/Q:.2f} q_adm  contacto={pt['bx']/pt['Bx']:.2f}")
