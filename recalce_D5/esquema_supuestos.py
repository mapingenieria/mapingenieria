"""Esquema en planta de los SUPUESTOS geométricos del modelo (para que el ingeniero los corrija)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import modelo_parrilla as m

fig, ax = plt.subplots(figsize=(7.2, 10.5))
XA, XC, XD = m.XA, m.XC, m.XD
for a, y in m.YAX.items():                                   # vigas
    ax.plot([XA, XD], [y, y], color="#555", lw=3, alpha=.5, zorder=1)
    ax.text(XD + 0.9, y, f"eje {a}", va="center", fontsize=9)
ax.plot([XC, XC], [0, m.YAX[6]], color="#555", lw=2, alpha=.5)
for col, x in (("A", XA), ("D", XD)):                        # zapatas Z1 y columnas
    sg = 1 if col == "A" else -1
    for a, y in m.YAX.items():
        x0 = x - sg * 0.15
        xs = sorted((x0, x0 + sg * 1.8))
        ax.add_patch(Rectangle((xs[0], y - 0.9), 1.8, 1.8, fc="#d9d9d9", ec="#888", lw=1, zorder=2))
        ax.add_patch(Rectangle((x - 0.15, y - 0.5), 0.30, 1.0, fc="#222", zorder=4))
        ax.text(x + (-0.2 if col == "A" else 0.2), y - 1.05, f"{col}{a}", ha="center", fontsize=8)
# supuestos para D5
y5 = m.YAX[5]
xe = XD + 0.15                                               # cara del lindero D
ax.add_patch(Rectangle((xe - 2.10, y5 - 1.45), 2.10, 2.90, fc="#f5b7b1", ec="#c0392b", lw=2, alpha=.8, zorder=3))
ax.text(xe - 1.05, y5 - 1.1, "FOSO supuesto\nadosado al lindero\n2,10 x 2,90 m\n(caja libre 1,70 x 2,50)",
        ha="center", fontsize=8, color="#7b241c", zorder=6)
ax.add_patch(Rectangle((xe - 0.9, y5 - 2.5), 0.9, 5.0, fc="none", ec="#1f618d", lw=2.2, ls="--", zorder=5))
ax.text(xe - 0.45, y5 + 2.75, "Corrida 0,9 x 5,0 m", ha="center", fontsize=8, color="#1f618d")
ax.axvline(xe, color="k", lw=1); ax.text(xe + 0.05, 0.4, "lindero D", rotation=90, fontsize=8)
ax.axvline(XA - 0.15, color="k", lw=1); ax.text(XA - 0.45, 0.4, "lindero A", rotation=90, fontsize=8)
ax.text(XC, -1.4, "Zapatas Z1 supuestas 1,8 x 1,8 m (gris)\nVigas VC.S‑55x40 y VC.S‑6 como líneas gruesas",
        ha="center", fontsize=8)
ax.set_xlim(-1.2, 9.0); ax.set_ylim(m.YAX[6] + 2.2, -2.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Supuestos del modelo (planta, ejes A–D, 1–6)\n¿Dónde está el foso realmente?", fontsize=10)
fig.tight_layout(); fig.savefig("esquema_supuestos.png", dpi=130)
