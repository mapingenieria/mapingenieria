"""Corrida con Z1 = 2,0 x 2,0 m y el foso según la planta de segundo nivel (P_D5 = 85 t).

Lectura de la planta: el hueco del ascensor (recuadro con X, 2,46-2,56 x 1,70 m) queda pegado al lindero D,
inmediatamente al SUR de D5: 2,50 m hacia el interior (x) x 1,70 m a lo largo del lindero (y). Con muros de 0,20 m
la huella exterior es 2,90 (x) x 2,10 (y). Su borde norte (y0, medido desde el eje de D5 hacia el sur) es el dato
menos seguro: la planta lo muestra casi en el eje de D5, pero una columna de 1,00 m obliga a y0 >= 0,5. Se barre
y0 = 0,0 / 0,5 / 1,0 m.

Uso: PYTHONPATH=. python3 correr_foso_real.py -> resultados_foso_real.json"""
import json
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
Q = m.QADM_CLAY
Z = 2.0
PIT_X, PIT_Y = 2.50 + 0.40, 1.70 + 0.40
CLEAR = 0.10                                              # holgura entre zapata y muro del foso
MULTS = (1.0, 3.0, 10.0)


def patch(bx, y_a, y_b, ks):
    return dict(Bx=bx, By=y_b - y_a, yoff=(y_a + y_b) / 2, ks=ks)


def variantes(y0, ks_g=m.KS_GRAVEL):
    ks = m.KS_CLAY
    ys = y0 - CLEAR                                        # borde sur permitido de la zapata en arcilla
    V = {}
    V["V0 Z1 2x2 original (interfiere)"] = [patch(Z, -1.0, 1.0, ks)]
    V["R  recorte + prolongación al norte (2,0 x 2,0)"] = [patch(Z, ys - 2.0, ys, ks)]
    V["Rc solo recorte (sin prolongar)"] = [patch(Z, -1.0, ys, ks)]
    V["S  corrida 0,9 hacia el norte"] = [patch(0.9, -3.2, ys, ks)]
    V["A  zapata 2x2 profunda en grava"] = [patch(Z, -1.0, 1.0, ks_g)]
    V["A2 zapata recortada + cajón del foso"] = [patch(Z, -1.0, y0, ks), patch(PIT_X, y0, y0 + PIT_Y, ks)]
    return V


def correr(pats):
    foot = {f"{c}{a}": dict(m.Z1, Bx=Z, By=Z) for c in "AD" for a in m.YAX}
    foot["D5"] = pats
    res = m.solve_nt(foot, None, loads=m.column_loads(m.W_TOTAL))
    p = m.post(res)
    f, d5 = p["footings"], p["footings"]["D5"]
    clay = [x["p_max"] for x in d5["patches"] if x["ks"] == m.KS_CLAY]
    grav = [x["p_max"] for x in d5["patches"] if x["ks"] != m.KS_CLAY]
    return dict(D5_Q=(max(clay) / Q if clay else None), D5_grav_kPa=(max(grav) if grav else None),
                M_exc=abs(d5["e_x"]) * d5["R"], contacto=d5["contact_frac"],
                neigh_Q=max(f[k]["p_max"] for k in ("A5", "D3", "D6")) / Q,
                T_max=max(b["T"] for b in p["beams"].values()),
                M_lindD=max(max(abs(v["M_sag"]), abs(v["M_hog"])) for k, v in p["beams"].items()
                            if k.startswith("Lindero D")),
                dif_mm=max(v["settle_mm"] for v in f.values()) - min(v["settle_mm"] for v in f.values()))


out = {}
print(f"P_D5 = {P_D5:.0f} kN; Z1 = {Z} x {Z} m (e = {(Z-0.30)/2:.2f} m); huella del foso {PIT_X:.2f} x {PIT_Y:.2f} m")
for y0 in (0.0, 0.5, 1.0):
    out[y0] = {}
    for mult in MULTS:
        m.SUPER_MULT = mult
        out[y0][mult] = {n: correr(p) for n, p in variantes(y0).items()}
    m.SUPER_MULT = 1.0
    print(f"\n##### borde norte del foso a {y0:.1f} m al sur del eje de D5 #####")
    print(f"{'':48s} p_D5/q_adm (x1 / x3 / x10)   M_exc   vecinas(x1)  T_max  M_lindD")
    for n in out[y0][1.0]:
        r1, r3, r10 = out[y0][1.0][n], out[y0][3.0][n], out[y0][10.0][n]
        f = lambda r: "  - " if r["D5_Q"] is None else f"{r['D5_Q']:.2f}"
        print(f"{n:48s} {f(r1)} / {f(r3)} / {f(r10)}        {r1['M_exc']:5.0f}   {r1['neigh_Q']:.2f}      "
              f"{r1['T_max']:5.0f}  {r1['M_lindD']:5.0f}")
json.dump(out, open("resultados_foso_real.json", "w"), indent=1, default=float)
