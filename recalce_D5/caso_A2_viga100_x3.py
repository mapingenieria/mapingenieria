"""Caso puntual: A2 (zapata recortada + cajón del foso) con VC eje 5 de 0,40 x 1,00 m y restricción x3.
y0 = 0,5 m, Z1 = 2,0 x 2,0 m, P_D5 = 85 t (servicio), sótano al nivel del terreno.
Uso: PYTHONPATH=. python3 caso_A2_viga100_x3.py -> caso_A2_viga100_x3.json"""
import json
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
m.SUPER_MULT = 3.0
Q, Z, Y0 = m.QADM_CLAY, 2.0, 0.5
H = 1.00
over = {"VC eje 5 (A-C)": (0.40, H), "VC eje 5 (C-D)": (0.40, H)}
P = m.column_loads(m.W_TOTAL)


def caso(nombre, d5):
    foot = {f"{c}{a}": dict(m.Z1, Bx=Z, By=Z) for c in "AD" for a in m.YAX}
    foot["D5"] = d5
    res = m.solve_nt(foot, over, loads=P)
    return nombre, m.post(res), res


pa = lambda bx, a, b: dict(Bx=bx, By=b - a, yoff=(a + b) / 2, ks=m.KS_CLAY)
casos = [caso("V0 Z1 2x2 original", [pa(Z, -1.0, 1.0)]),
         caso("A2 recortada + cajón", [pa(Z, -1.0, Y0), pa(2.90, Y0, Y0 + 2.10)])]
out = {}
for nombre, p, res in casos:
    f, b = p["footings"], p["beams"]
    print(f"\n===== {nombre} | VC eje 5 0,40x{H:.2f} | restricción x3 | P_D5 = {P_D5:.0f} kN =====")
    print("Zapata  P(kN)  R/P   p_máx/q_adm  contacto  asent.(mm)")
    for k in ("A1", "A3", "A5", "A6", "D1", "D3", "D5", "D6"):
        x = f[k]
        print(f"{k:6s} {P[k]:6.0f}  {x['R_over_P']:.2f}   {x['p_max']/Q:5.2f}       {x['contact_frac']:.2f}     {x['settle_mm']:.1f}")
    d5 = f["D5"]
    if len(d5["patches"]) > 1:
        print("Parches de D5 (norte = Z1 recortada, sur = cajón):")
        for nm, pt in zip(("norte", "cajón"), d5["patches"]):
            print(f"   {nm:6s} R={pt['R']:6.0f} kN ({pt['R']/d5['R']*100:3.0f} %)  p_máx={pt['p_max']:4.0f} kPa = {pt['p_max']/Q:.2f} q_adm"
                  f"  p_mín={pt['p_min']:5.0f} kPa  contacto={pt['bx']/pt['Bx']:.2f}")
    print(f"M_exc (R·e) = {abs(d5['e_x'])*d5['R']:.0f} kN·m ; φMn indicativo VC 0,40x{H:.2f} = {m.phiMn(0.40, H):.0f} kN·m")
    print("Vigas (M sag / M hog kN·m, T kN·m):")
    for lab in ("VC eje 5 (A-C)", "VC eje 5 (C-D)", "Lindero D 3-5", "Lindero D 5-6", "VC.S-6 3-5", "VC.S-6 5-6"):
        v = b[lab]
        print(f"   {lab:16s} +{v['M_sag']:6.0f} / {v['M_hog']:6.0f}   T={v['T']:5.1f}   (φMn ρ=1 %: {m.phiMn(v['b'], v['h']):.0f})")
    out[nombre] = dict(
        footings={k: {kk: vv for kk, vv in f[k].items() if kk != 'patches'} for k in f},
        patches=d5["patches"], beams=b)
json.dump(out, open("caso_A2_viga100_x3.json", "w"), indent=1, default=float)
m.SUPER_MULT = 1.0
