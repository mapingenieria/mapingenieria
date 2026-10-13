"""Con y0 = 0,5 m y sótano al nivel del terreno: ¿una viga de enlace A5-D5 más peraltada arregla la excentricidad?
Compara Z1 2x2 original (V0) y A2 (zapata recortada + cajón del foso) variando la altura de la VC del eje 5.
Uso: PYTHONPATH=. python3 correr_viga_enlace.py -> resultados_viga_enlace.json"""
import json
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
Q = m.QADM_CLAY
Z, Y0 = 2.0, 0.5
PIT_X, PIT_Y = 2.90, 2.10
ks = m.KS_CLAY


def patch(bx, a, b, k=ks):
    return dict(Bx=bx, By=b - a, yoff=(a + b) / 2, ks=k)


VAR = {"V0 Z1 2x2 original": [patch(Z, -1.0, 1.0)],
       "A2 recortada + cajón": [patch(Z, -1.0, Y0), patch(PIT_X, Y0, Y0 + PIT_Y)]}


def correr(pats, h):
    foot = {f"{c}{a}": dict(m.Z1, Bx=Z, By=Z) for c in "AD" for a in m.YAX}
    foot["D5"] = pats
    over = {"VC eje 5 (A-C)": (0.40, h), "VC eje 5 (C-D)": (0.40, h)}
    res = m.solve_nt(foot, over, loads=m.column_loads(m.W_TOTAL))
    p = m.post(res)
    f, d5 = p["footings"], p["footings"]["D5"]
    b5 = max(max(abs(v["M_sag"]), abs(v["M_hog"])) for k, v in p["beams"].items() if k.startswith("VC eje 5"))
    out = dict(D5_Q=d5["p_max"] / Q, A5_Q=f["A5"]["p_max"] / Q, M_viga5=b5, phiMn=m.phiMn(0.40, h),
               M_exc=abs(d5["e_x"]) * d5["R"], contacto=d5["contact_frac"])
    if len(d5["patches"]) > 1:
        R = d5["R"]
        out["reparto"] = [round(x["R"] / R, 2) for x in d5["patches"]]
        out["p_patch_Q"] = [round(x["p_max"] / Q, 2) for x in d5["patches"]]
    return out


out = {}
for mult in (1.0, 3.0):
    m.SUPER_MULT = mult
    out[mult] = {}
    print(f"\n=== restricción de la superestructura x{mult:g} ===")
    print(f"{'VC eje 5':10s} {'caso':24s}  D5 p/qadm  A5 p/qadm   M viga5 / phiMn(rho=1%)   M_exc")
    for h in (0.55, 0.80, 1.00, 1.20):
        for n, pats in VAR.items():
            r = correr(pats, h)
            out[mult][f"{h}|{n}"] = r
            extra = f"   reparto parches {r['reparto']} p/qadm {r['p_patch_Q']}" if "reparto" in r else ""
            print(f"0,40x{h:<5} {n:24s}  {r['D5_Q']:.2f}       {r['A5_Q']:.2f}       {r['M_viga5']:5.0f} / {r['phiMn']:5.0f}"
                  f"          {r['M_exc']:4.0f}{extra}")
m.SUPER_MULT = 1.0
json.dump(out, open("resultados_viga_enlace.json", "w"), indent=1, default=float)
