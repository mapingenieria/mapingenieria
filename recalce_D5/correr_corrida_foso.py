"""Corrida angosta a lo largo del lindero con el foso ADOSADO al lindero (P_D5 = 85 t).

Geometría supuesta (a confirmar): foso adosado al lindero D, caja libre 1,70 (x) x 2,50 (y) m
más muros de 0,20 m -> huella 2,10 x 2,90 m, centrada en el eje 5. Donde la corrida pasa bajo
la huella del foso debe ir MÁS PROFUNDA que la placa del foso (base ~ -2,4 a -2,55 m bajo el
piso del sótano, en la grava); fuera de la huella queda al nivel original (arcilla).
Por eso la corrida se modela escalonada: tramo profundo (ks de grava) + tramos someros (arcilla).

Uso: PYTHONPATH=. python3 correr_corrida_foso.py -> resultados_corrida_foso.json, comparacion_corrida_foso.png"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
Q = m.QADM_CLAY
PIT_Y = 2.50 + 0.40                                    # largo exterior del foso a lo largo del lindero
MULTS = (1.0, 3.0, 10.0)


def strip(bx, by_total, pit_c=0.0, ks_g=m.KS_GRAVEL, modo="escalonada"):
    y0, y1 = -by_total / 2, by_total / 2
    d0, d1 = max(y0, pit_c - PIT_Y / 2), min(y1, pit_c + PIT_Y / 2)
    pats = []

    def add(a, b, ks):
        if b - a > 1e-6:
            pats.append(dict(Bx=bx, By=b - a, yoff=(a + b) / 2, ks=ks))
    if modo == "arcilla":
        add(y0, y1, m.KS_CLAY)
    elif modo == "grava" or d1 <= d0:
        add(y0, y1, ks_g if modo == "grava" else m.KS_CLAY)
    else:
        add(y0, d0, m.KS_CLAY); add(d0, d1, ks_g); add(d1, y1, m.KS_CLAY)
    return pats


def correr(pats_d5, ks_g):
    foot = {f"{c}{a}": dict(m.Z1) for c in "AD" for a in m.YAX}
    foot["D5"] = pats_d5
    res = m.solve_nt(foot, None, loads=m.column_loads(m.W_TOTAL))
    p = m.post(res)
    f = p["footings"]
    d5 = f["D5"]
    clay = [x["p_max"] for x in d5["patches"] if x["ks"] == m.KS_CLAY]
    grav = [x["p_max"] for x in d5["patches"] if x["ks"] == ks_g]
    Rg = sum(x["R"] for x in d5["patches"] if x["ks"] == ks_g)
    neigh = max(f[k]["p_max"] for k in ("A5", "D3", "D6")) / Q
    settles = [v["settle_mm"] for v in f.values()]
    return dict(p_clay_Q=(max(clay) / Q if clay else None), p_grav_kPa=(max(grav) if grav else None),
                R_grav_frac=Rg / d5["R"], M_exc=abs(d5["e_x"]) * d5["R"], contacto=d5["contact_frac"],
                R_over_P=d5["R_over_P"], neigh_Q=neigh, dif_mm=max(settles) - min(settles),
                M_lindD=max(max(abs(v["M_sag"]), abs(v["M_hog"])) for k, v in p["beams"].items()
                            if k.startswith("Lindero D")))


CASOS = [
    ("Corrida 0,9x5,0 escalonada, foso centrado", dict(bx=0.9, by_total=5.0)),
    ("Corrida 0,9x4,0 escalonada, foso centrado", dict(bx=0.9, by_total=4.0)),
    ("Corrida 0,6x5,0 escalonada, foso centrado", dict(bx=0.6, by_total=5.0)),
    ("Corrida 0,9x5,0, foso desplazado +1,0 m", dict(bx=0.9, by_total=5.0, pit_c=1.0)),
    ("Corrida 0,9x5,0, foso desplazado -1,0 m", dict(bx=0.9, by_total=5.0, pit_c=-1.0)),
    ("Corrida 0,9x5,0 toda en grava (peor caso)", dict(bx=0.9, by_total=5.0, modo="grava")),
    ("Corrida 0,9x5,0 toda en arcilla (sin foso, ref.)", dict(bx=0.9, by_total=5.0, modo="arcilla")),
]
out = {"P_D5_kN": P_D5, "casos": {}, "sens_ks_grava": {}}
for mult in MULTS:
    m.SUPER_MULT = mult
    out["casos"][mult] = {}
    print(f"\n=== restricción rotacional x{mult:g} (ks grava = {m.KS_GRAVEL:.0f}) ===")
    for lab, kw in CASOS:
        r = correr(strip(**kw), m.KS_GRAVEL)
        out["casos"][mult][lab] = r
        pc = "  - " if r["p_clay_Q"] is None else f"{r['p_clay_Q']:.2f}"
        pg = "  - " if r["p_grav_kPa"] is None else f"{r['p_grav_kPa']:4.0f}"
        print(f"{lab:50s} arcilla p/qadm={pc} grava p={pg} kPa  %R en grava={r['R_grav_frac']*100:3.0f}"
              f"  M_exc={r['M_exc']:4.0f}  vecinas={r['neigh_Q']:.2f}  dif={r['dif_mm']:.1f} mm")
    # sensibilidad al ks de la grava (caso principal)
    out["sens_ks_grava"][mult] = {}
    for ksg in (15_000.0, 25_000.0, 60_000.0):
        r = correr(strip(0.9, 5.0, ks_g=ksg), ksg)
        out["sens_ks_grava"][mult][ksg] = r
        print(f"   sens. ks grava={ksg:6.0f}: arcilla p/qadm={r['p_clay_Q']:.2f} grava p={r['p_grav_kPa']:4.0f} kPa"
              f"  %R grava={r['R_grav_frac']*100:3.0f}  vecinas={r['neigh_Q']:.2f}  dif={r['dif_mm']:.1f} mm")
m.SUPER_MULT = 1.0
json.dump(out, open("resultados_corrida_foso.json", "w"), indent=1, default=float)

fig, axs = plt.subplots(1, 2, figsize=(13, 4.6))
labs = ["0,9x5,0\nfoso centrado", "0,9x4,0", "0,6x5,0", "0,9x5,0\nfoso +1,0", "0,9x5,0\nfoso −1,0",
        "0,9x5,0\ntoda grava", "0,9x5,0\ntoda arcilla"]
w = 0.26
for i, mult in enumerate(MULTS):
    vals = [out["casos"][mult][lab]["p_clay_Q"] or 0 for lab, _ in CASOS]
    gv = [out["casos"][mult][lab]["p_grav_kPa"] or 0 for lab, _ in CASOS]
    axs[0].bar(np.arange(7) + (i - 1) * w, vals, w, label=f"restricción ×{mult:g}")
    axs[1].bar(np.arange(7) + (i - 1) * w, gv, w, label=f"restricción ×{mult:g}")
axs[0].axhline(1.0, color="k", ls="--", lw=0.8)
axs[0].set_title("Tramos en arcilla: p_máx / q_adm", fontsize=10)
axs[1].set_title("Tramo en grava bajo el foso: p_máx (kPa) — q_adm de la grava sin dato", fontsize=10)
for a in axs:
    a.set_xticks(range(7)); a.set_xticklabels(labs, fontsize=7); a.grid(axis="y", alpha=0.3); a.legend(fontsize=8)
fig.suptitle("Corrida angosta con foso adosado al lindero, P_D5 = 85 t", fontsize=10)
fig.tight_layout(); fig.savefig("comparacion_corrida_foso.png", dpi=140)
