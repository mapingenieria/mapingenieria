"""Corrida con P_D5 medida (85 t). Las cargas vecinas usan el mismo reparto tributario (SUPUESTO).
La restricción rotacional que aporta la superestructura al nodo de columna es la incógnita
dominante: se barre con multiplicadores x1, x3, x10 sobre un resorte base de 4EI/h (columna 0,30 m).
Uso: PYTHONPATH=. python3 correr_85t.py   -> resultados_85t.json, comparacion_85t.png"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import modelo_parrilla as m

G = 9.81
P_D5 = 85 * G                                         # kN, se asume carga de servicio
s = sum(m.Y_TRIB.values())
m.W_TOTAL = P_D5 * 2 * s / m.Y_TRIB[5]
Q = m.QADM_CLAY
MULTS = (1.0, 3.0, 10.0)
print(f"P_D5 = {P_D5:.0f} kN ; W_total equivalente = {m.W_TOTAL:.0f} kN ; vecinas: "
      + ", ".join(f"{k}={v:.0f}" for k, v in m.column_loads().items()))

# ---------------------------------------------------------------- variantes del estudio
short = {"Base (Z1 original)": "Base", "A  zapata nueva profunda (grava)": "A",
         "A2 cajon del foso integrado": "A2", "B  zapata angosta y larga": "B",
         "C  D5 colgada de viga de lindero": "C",
         "T0 transicion: D5 sin zapata, vigas actuales": "T0"}
out = {"P_D5_kN": P_D5, "W_total": m.W_TOTAL, "variantes": {}, "formas": {}}
for mult in MULTS:
    m.SUPER_MULT = mult
    r = m.run_all()
    rows = {}
    for n, v in r.items():
        mm, f = v["metrics"], v["post"]["footings"]
        d5 = f.get("D5")
        rows[short[n]] = dict(
            D5_pmax_Q=None if d5 is None else d5["p_max"] / Q,
            D5_contact=None if d5 is None else d5["contact_frac"],
            M_exc=None if d5 is None else d5["R"] * abs(d5["e_x"]),
            neigh_pmax_Q=max(mm["A5_p_max"], mm["D3_p_max"], mm["D6_p_max"]) / Q,
            dif_mm=mm["dif_settle_mm"], M_lindD=mm["M_lindD"]["M"], M_lindD_ref=mm["M_lindD"]["phiMn_ref"])
    out["variantes"][mult] = rows
    print(f"\n=== restricción rotacional x{mult:g} ===")
    for k, x in rows.items():
        d = "  -  " if x["D5_pmax_Q"] is None else f"{x['D5_pmax_Q']:.2f}"
        e = "  -" if x["M_exc"] is None else f"{x['M_exc']:.0f}"
        print(f"{k:4s} D5 p/qadm={d}  M_exc={e:>4s}  vecinas p/qadm={x['neigh_pmax_Q']:.2f}"
              f"  dif={x['dif_mm']:.1f} mm  M lind={x['M_lindD']:.0f}/{x['M_lindD_ref']:.0f}")

# ---------------------------------------------------------------- restricción necesaria
lo, hi = 1.0, 1e5
for _ in range(60):
    mid = (lo * hi) ** 0.5
    m.SUPER_MULT = mid
    f = m.run_all()["Base (Z1 original)"]["post"]["footings"]["D5"]
    lo, hi = (mid, hi) if f["p_max"] > Q else (lo, mid)
out["mult_necesario_base"] = hi
print(f"\nZ1 original de D5 llega a q_adm solo con restricción x{hi:.0f}"
      f"  (límite concéntrico: {P_D5/3.24:.0f} kPa = {P_D5/3.24/Q:.2f} q_adm)")


# ---------------------------------------------------------------- barrido de formas
def run_d5(bx, by, ks=m.KS_CLAY):
    foot = {f"{c}{a}": dict(m.Z1) for c in "AD" for a in m.YAX}
    foot["D5"] = dict(Bx=bx, By=by, yoff=0.0, ks=ks)
    r = m.solve_nt(foot, None, loads=m.column_loads(m.W_TOTAL))
    return m.post(r)["footings"]["D5"]


FORMAS = [("Z1 original 1,8x1,8", 1.8, 1.8), ("A2 cajón 2,1x2,9", 2.1, 2.9),
          ("B 1,2x3,0", 1.2, 3.0), ("Corrida 0,9x4,0", 0.9, 4.0),
          ("Corrida 0,9x5,0", 0.9, 5.0), ("Corrida 0,6x5,0", 0.6, 5.0)]
print("\nForma de D5 (p_max/q_adm | M_exc = R*e en kN.m):")
for mult in MULTS:
    m.SUPER_MULT = mult
    out["formas"][mult] = {}
    print(f"  restricción x{mult:g}")
    for lab, bx, by in FORMAS:
        f = run_d5(bx, by)
        out["formas"][mult][lab] = dict(p_Q=f["p_max"] / Q, M_exc=f["R"] * abs(f["e_x"]),
                                        contacto=f["contact_frac"])
        print(f"    {lab:22s} {f['p_max']/Q:5.2f} | {f['R']*abs(f['e_x']):4.0f}  contacto {f['contact_frac']:.2f}")
m.SUPER_MULT = 1.0
json.dump(out, open("resultados_85t.json", "w"), indent=1, default=float)

# ---------------------------------------------------------------- figura
fig, axs = plt.subplots(1, 2, figsize=(13, 4.6))
labs = ["Base", "A (grava)", "A2 cajón", "B", "Corrida\n0,9x5,0", "Corrida\n0,6x5,0"]
src = lambda mult: [out["variantes"][mult]["Base"]["D5_pmax_Q"], out["variantes"][mult]["A"]["D5_pmax_Q"],
                    out["variantes"][mult]["A2"]["D5_pmax_Q"], out["variantes"][mult]["B"]["D5_pmax_Q"],
                    out["formas"][mult]["Corrida 0,9x5,0"]["p_Q"], out["formas"][mult]["Corrida 0,6x5,0"]["p_Q"]]
srcM = lambda mult: [out["variantes"][mult]["Base"]["M_exc"], out["variantes"][mult]["A"]["M_exc"],
                     out["variantes"][mult]["A2"]["M_exc"], out["variantes"][mult]["B"]["M_exc"],
                     out["formas"][mult]["Corrida 0,9x5,0"]["M_exc"], out["formas"][mult]["Corrida 0,6x5,0"]["M_exc"]]
w = 0.26
for i, mult in enumerate(MULTS):
    axs[0].bar(np.arange(6) + (i - 1) * w, src(mult), w, label=f"restricción ×{mult:g}")
    axs[1].bar(np.arange(6) + (i - 1) * w, srcM(mult), w, label=f"restricción ×{mult:g}")
axs[0].axhline(1.0, color="k", ls="--", lw=0.8)
axs[0].set_title("p_máx bajo D5 / q_adm  (P = 85 t)", fontsize=10)
axs[1].set_title("Momento por excentricidad R·e que debe equilibrar el sistema (kN·m)", fontsize=10)
for a in axs:
    a.set_xticks(range(6)); a.set_xticklabels(labs, fontsize=8); a.grid(axis="y", alpha=0.3); a.legend(fontsize=8)
fig.tight_layout(); fig.savefig("comparacion_85t.png", dpi=140)
