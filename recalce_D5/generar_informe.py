"""Lee resultados.json y produce comparacion.png (python3 generar_informe.py)."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.load(open("resultados.json"))
Q = 323.65
names = list(d["base"].keys())
short = {"Base (Z1 original)": "Base", "A  zapata nueva profunda (grava)": "A\nprofunda",
         "A2 cajon del foso integrado": "A2\ncajón", "B  zapata angosta y larga": "B\nangosta",
         "C  D5 colgada de viga de lindero": "C\ncolgada",
         "T0 transicion: D5 sin zapata, vigas actuales": "T0\nsin zapata"}


def rng(n, fn):
    vals = [fn(r["res"][n]) for r in d["sens"]]
    vals = [v for v in vals if v is not None]
    return min(vals), max(vals)


def neigh(m):
    return max(m["A5_p_max"], m["D3_p_max"], m["D6_p_max"]) / Q


panels = [
    ("Presión máx. bajo D5 / q_adm", lambda m: None if m["D5_p_max"] is None else m["D5_p_max"] / Q),
    ("Presión máx. vecinas (A5, D3, D6) / q_adm", neigh),
    ("Asentamiento diferencial entre zapatas (mm)", lambda m: m["dif_settle_mm"]),
]
fig, axs = plt.subplots(1, 3, figsize=(15, 4.4))
for ax, (title, fn) in zip(axs, panels):
    xs, hs, lo, hi, cols = [], [], [], [], []
    for i, n in enumerate(names):
        v = fn(d["base"][n]["metrics"])
        if v is None:
            continue
        a, b = rng(n, fn)
        xs.append(i); hs.append(v); lo.append(v - a); hi.append(b - v)
        cols.append("#8a8a8a" if n.startswith("Base") else "#c0392b" if n[0] in "CT" else "#2471a3")
    ax.bar(xs, hs, color=cols, yerr=[lo, hi], capsize=4, ecolor="#333")
    ax.set_xticks(range(len(names))); ax.set_xticklabels([short[n] for n in names], fontsize=8)
    ax.set_title(title, fontsize=10)
    if "q_adm" in title:
        ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.grid(axis="y", alpha=0.3)
fig.suptitle("Comparación preliminar de alternativas para D5 (carga calibrada: Z1 original = q_adm; "
             "barras de error = sensibilidad a ks y fisuración)", fontsize=10)
fig.tight_layout()
fig.savefig("comparacion.png", dpi=140)

# tablas auxiliares para el informe
b = d["base"]["Base (Z1 original)"]["metrics"]
print("ratio D5 pmax vs base (min-max sens):")
for n in names[1:4]:
    rr = [r["res"][n]["D5_p_max"] / r["res"]["Base (Z1 original)"]["D5_p_max"] for r in d["sens"]]
    print(f"  {n}: {min(rr):.2f}-{max(rr):.2f}")
print("ratio vecinas max pmax variante/base:")
for n in names[1:]:
    rr = [max(r["res"][n][k] for k in ("A5_p_max","D3_p_max","D6_p_max")) /
          max(r["res"]["Base (Z1 original)"][k] for k in ("A5_p_max","D3_p_max","D6_p_max")) for r in d["sens"]]
    print(f"  {n}: {min(rr):.2f}-{max(rr):.2f}")
