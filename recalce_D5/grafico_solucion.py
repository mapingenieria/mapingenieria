"""Imagen explicativa de la solución propuesta (planta y corte). Uso: python3 grafico_solucion.py -> solucion.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

C = dict(col="#222222", zap="#5dade2", cut="#e74c3c", caj="#f0b27a", viga="#58d68d", arc="#e8d3a8", gra="#b3a99a")
fig, (ax, bx) = plt.subplots(1, 2, figsize=(15.5, 7.8), gridspec_kw=dict(width_ratios=[1.05, 1]))


def R(a, x0, x1, y0, y1, **kw):
    a.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))


# ================================================================ PLANTA (lindero a la derecha)
R(ax, 0, 2.0, -1.0, 1.0, fc="none", ec="#7f8c8d", ls="--", lw=1.4, zorder=2)                # Z1 original
R(ax, 0, 2.0, -1.0, 0.0, fc=C["zap"], ec="#1b4f72", lw=1.8, alpha=.85, zorder=3)            # queda
R(ax, 0, 2.9, 0.0, 2.1, fc=C["caj"], ec="#a04000", lw=2, alpha=.9, zorder=4)                # cajón
R(ax, 0.2, 2.7, 0.2, 1.9, fc="white", ec="#a04000", lw=1.2, zorder=5)                       # pozo
R(ax, 0, 2.0, 0.0, 1.0, fc="none", ec="#922b21", lw=2, hatch="////", zorder=6)              # demolición
R(ax, 0.3, 4.2, -0.2, 0.2, fc=C["viga"], ec="#1d8348", lw=1.5, zorder=6)                    # viga de enlace
R(ax, 0, 0.3, -0.5, 0.5, fc=C["col"], zorder=7)                                               # columna
R(ax, 0.1, 3.6, 2.13, 5.0, fc="#d5d8dc", ec="#566573", lw=1.5, hatch="..", zorder=1)
ax.text(2.0, 3.6, "ESCALERA\n(lectura aprox. de la planta\nde 2.º nivel)", ha="center", va="center", fontsize=8.5, color="#2c3e50", fontweight="bold")
ax.annotate("escalera existente: no se toca\n(holgura ≈ 0,0–0,1 m, confirmar en obra)", xy=(2.9, 2.13), xytext=(7.0, 2.9), fontsize=8.5, color="#1d8348",
            fontweight="bold", ha="left", arrowprops=dict(arrowstyle="->", color="#1d8348"))
ax.annotate("", xy=(2.7, 1.72), xytext=(0.2, 1.72), arrowprops=dict(arrowstyle="<->", color="#333"), zorder=12)
ax.text(1.45, 1.80, "2,50 libres", ha="center", va="top", fontsize=8, fontweight="bold", zorder=12)
ax.annotate("", xy=(2.55, 1.9), xytext=(2.55, 0.2), arrowprops=dict(arrowstyle="<->", color="#333"), zorder=12)
ax.text(2.58, 1.05, "1,70\nlibres", ha="left", va="center", fontsize=8, fontweight="bold", zorder=12)
ax.annotate("", xy=(3.15, 2.1), xytext=(3.15, 0.0), arrowprops=dict(arrowstyle="<->", color="#a04000"), zorder=12)
ax.text(3.2, 0.5, "2,10 ext.\n(muros 0,20)", ha="left", va="center", fontsize=7.5, color="#a04000", zorder=12)
ax.axvline(0, color="k", lw=3, zorder=8)
ax.text(0, -1.78, "LINDERO", ha="center", va="center", fontsize=10, fontweight="bold")
ax.annotate("Columna D5\n0,30 x 1,00", xy=(0.0, -0.3), xytext=(-0.45, -1.1), fontsize=8, ha="left",
            arrowprops=dict(arrowstyle="->", color=C["col"]))
ax.text(1.3, -0.62, "① Zapata Z1 (2,0 x 2,0)\nrecortada: se conserva", ha="center", va="center",
        fontsize=8.5, color="#0b2e4a", fontweight="bold", zorder=9)
ax.annotate("② se demuele: 1,0 m de la zapata\nque chocan con el foso", xy=(1.5, 0.5), xytext=(7.0, 1.2),
            fontsize=8.5, color="#7b241c", fontweight="bold", ha="left", arrowprops=dict(arrowstyle="->", color="#922b21"))
ax.annotate("③ CAJÓN DEL FOSO\nlosa-zapata + muros\nhuella exterior 2,90 x 2,10", xy=(2.5, 1.6), xytext=(7.0, 1.9),
            fontsize=9, color="#7e3500", fontweight="bold", ha="left", arrowprops=dict(arrowstyle="->", color="#a04000"))
ax.text(1.35, 1.55, "pozo libre", ha="center", va="center", fontsize=8, color="#555", zorder=9)
ax.annotate("④ Viga de enlace del eje 5\n0,40 x 1,00 m  →  hacia A5", xy=(3.9, -0.2), xytext=(4.5, -1.3), fontsize=9,
            color="#1d8348", fontweight="bold", ha="left", arrowprops=dict(arrowstyle="->", color="#1d8348"))
ax.annotate("", xy=(2.0, -1.45), xytext=(0, -1.45), arrowprops=dict(arrowstyle="<->"))
ax.text(1.0, -1.58, "2,0 m", ha="center", fontsize=8)
ax.text(-0.15, 0.0, "eje 5", fontsize=8, va="center", ha="left")
ax.set_xlim(7.2, -1.6); ax.set_ylim(5.2, -2.1); ax.set_aspect("equal")
ax.set_xlabel("distancia desde el lindero (m, hacia el interior)", fontsize=8)
ax.set_ylabel("a lo largo del lindero (m, sur ↓)", fontsize=8)
ax.set_title("PLANTA (zona de D5)", fontsize=11, fontweight="bold")

# ================================================================ CORTE por el foso (lindero a la derecha)
R(bx, -1.2, 7.6, -2.0, 0.0, fc=C["arc"], ec="none", zorder=1)
R(bx, -1.2, 7.6, -3.3, -2.0, fc=C["gra"], ec="none", zorder=1)
bx.text(5.1, -0.95, "ARCILLA firme", ha="left", va="center", fontsize=9, color="#6e5a2c", fontweight="bold")
bx.text(5.1, -2.65, "GRAVA\nmedia-suelta\n(sin parámetros)", ha="left", va="center", fontsize=9, color="#4d463c", fontweight="bold")
R(bx, 0.2, 2.7, -1.5, 0.0, fc="white", ec="none", zorder=3)                                    # foso
R(bx, 0.0, 2.9, -2.0, -1.55, fc=C["caj"], ec="#a04000", lw=2, zorder=4)                        # losa-zapata
R(bx, 0.0, 0.2, -1.55, 0.0, fc=C["caj"], ec="#a04000", lw=2, zorder=4)                         # muros
R(bx, 2.7, 2.9, -1.55, 0.0, fc=C["caj"], ec="#a04000", lw=2, zorder=4)
R(bx, 0.2, 2.7, -1.55, -1.5, fc="#bbb", ec="none", zorder=4)                                   # acabado
R(bx, 0.0, 2.9, -2.55, -2.0, fc="none", ec="#566573", ls="--", lw=1.5, zorder=4)               # opción A
bx.text(1.45, -2.28, "Opción A (zapata profunda): base −2,55\n✗ descartada: entra 0,55 m en la grava",
        ha="center", va="center", fontsize=8.5, color="#2c3e50")
bx.axhline(0, color="k", lw=2.2, zorder=6)
bx.text(5.1, 0.12, "terreno = piso terminado\ndel sótano (±0,00)", fontsize=8.5, va="bottom", ha="left")
bx.text(1.45, -0.75, "POZO / FOSO\nfondo terminado −1,50", ha="center", va="center", fontsize=9, fontweight="bold")
bx.text(1.45, -1.78, "LOSA-ZAPATA ≤ 0,45 m  →  base −2,00", ha="center", va="center", fontsize=8,
        fontweight="bold", color="#7e3500", zorder=7)
bx.annotate("base de la zapata original = −2,00\n(contacto arcilla / grava)", xy=(2.95, -2.0), xytext=(5.1, -3.2),
            fontsize=8.5, ha="left", va="center", arrowprops=dict(arrowstyle="->"))
bx.axvline(0, color="k", lw=3, zorder=6)
bx.text(0, 0.95, "LINDERO", ha="center", va="center", fontsize=10, fontweight="bold")
bx.set_xlim(7.4, -1.2); bx.set_ylim(-3.4, 1.3)
bx.set_xlabel("distancia desde el lindero (m)", fontsize=8); bx.set_ylabel("cota (m)", fontsize=8)
bx.set_title("CORTE por el foso (perpendicular al lindero)", fontsize=11, fontweight="bold")

fig.suptitle("SOLUCIÓN PROPUESTA PARA D5:  zapata recortada + cajón del foso + viga de enlace (escalera existente respetada)",
             fontsize=14, fontweight="bold", y=0.985)
fig.text(0.5, 0.012,
         "Qué logra: libera el foso (1,50 m), respeta la escalera construida, no excava en la grava y mantiene la base en −2,00.   "
         "Requiere: apuntalamiento y transferencia de carga antes de demoler.\n"
         "Preliminar: falta confirmar la posición construida del hueco, cargas reales de D3/A3, restricción al giro y criterio del geotecnista.",
         ha="center", fontsize=8.5, style="italic")
fig.tight_layout(rect=(0, 0.05, 1, 0.955)); fig.savefig("solucion.png", dpi=140)
