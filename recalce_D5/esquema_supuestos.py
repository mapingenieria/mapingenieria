"""Esquema en planta de la geometría usada (Z1 2x2 m, foso según planta de segundo nivel)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import modelo_parrilla as m

fig, ax = plt.subplots(figsize=(7.2, 10.5))
XA, XC, XD = m.XA, m.XC, m.XD
for a, y in m.YAX.items():
    ax.plot([XA, XD], [y, y], color="#555", lw=3, alpha=.5, zorder=1)
    ax.text(XD + 1.0, y, f"eje {a}", va="center", fontsize=9)
ax.plot([XC, XC], [0, m.YAX[6]], color="#555", lw=2, alpha=.5)
Z = 2.0
for col, x in (("A", XA), ("D", XD)):
    sg = 1 if col == "A" else -1
    for a, y in m.YAX.items():
        x0 = x - sg * 0.15
        xs = sorted((x0, x0 + sg * Z))
        ax.add_patch(Rectangle((xs[0], y - Z / 2), Z, Z, fc="#d9d9d9", ec="#888", lw=1, zorder=2))
        ax.add_patch(Rectangle((x - 0.15, y - 0.5), 0.30, 1.0, fc="#222", zorder=4))
        ax.text(x + (-0.25 if col == "A" else 0.25), y - 1.15, f"{col}{a}", ha="center", fontsize=8)
y5, xe, y0 = m.YAX[5], XD + 0.15, 0.5
ax.add_patch(Rectangle((xe - 2.90, y5 + y0), 2.90, 2.10, fc="#f5b7b1", ec="#c0392b", lw=2, alpha=.85, zorder=3))
ax.text(xe - 1.45, y5 + y0 + 1.05, "FOSO (lectura planta 2.º nivel)\nhuella 2,90 x 2,10 m\n(caja libre 2,50 x 1,70)",
        ha="center", va="center", fontsize=8, color="#7b241c", zorder=6)
ax.annotate("", xy=(xe + 0.6, y5 + y0), xytext=(xe + 0.6, y5), arrowprops=dict(arrowstyle="<->", color="#c0392b"))
ax.text(xe + 0.7, y5 + y0 / 2, "y0 = ?\n(borde norte\ndel foso)", fontsize=8, color="#c0392b", va="center")
ax.axvline(xe, color="k", lw=1); ax.text(xe + 0.05, 0.4, "lindero D", rotation=90, fontsize=8)
ax.axvline(XA - 0.15, color="k", lw=1); ax.text(XA - 0.45, 0.4, "lindero A", rotation=90, fontsize=8)
ax.text(XC, -1.6, "Zapatas Z1 de 2,0 x 2,0 m (gris); vigas como líneas gruesas", ha="center", fontsize=8)
ax.set_xlim(-1.2, 9.3); ax.set_ylim(m.YAX[6] + 2.2, -2.4); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Geometría usada en el modelo (planta). Confirmar y0 y la posición del foso", fontsize=10)
fig.tight_layout(); fig.savefig("esquema_supuestos.png", dpi=130)
