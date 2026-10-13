"""Lámina sobria (monocroma) de la solución propuesta para D5: planta y corte. Uso: python3 dibujo_solucion.py -> solucion_plano.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib import rcParams

rcParams["font.family"] = "DejaVu Sans"
rcParams["hatch.linewidth"] = 0.5
rcParams["hatch.color"] = "#9a9a9a"
K, G1, G2, G3 = "#111111", "#d9d9d9", "#efefef", "#8c8c8c"

fig = plt.figure(figsize=(16.5, 10.2), facecolor="white")
ax = fig.add_axes([0.02, 0.27, 0.58, 0.66])      # planta
bx = fig.add_axes([0.62, 0.30, 0.36, 0.62])      # corte
lg = fig.add_axes([0.04, 0.03, 0.55, 0.20]); lg.axis("off")
tb = fig.add_axes([0.62, 0.03, 0.35, 0.20]); tb.axis("off")


def R(a, x0, x1, y0, y1, **kw):
    a.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))


def dim(a, p, q, off, txt, horiz=True, fs=8, up=True, flip=False):
    """Cota con ticks a 45°; el texto va junto a la línea (sin interrumpirla)."""
    if horiz:
        a.plot([p, q], [off, off], color=K, lw=0.8, zorder=20)
        for v in (p, q):
            a.plot([v, v], [off - 0.07, off + 0.07], color=K, lw=0.8, zorder=20)
            a.plot([v - 0.04, v + 0.04], [off + 0.04, off - 0.04], color=K, lw=1.2, zorder=20)
        sgn = -1 if flip else 1                      # eje y invertido: "arriba" en pantalla = y menor
        a.text((p + q) / 2, off - 0.1 * sgn, txt, ha="center", va="bottom" if sgn > 0 else "top", fontsize=fs, zorder=21)
    else:
        a.plot([off, off], [p, q], color=K, lw=0.8, zorder=20)
        for v in (p, q):
            a.plot([off - 0.07, off + 0.07], [v, v], color=K, lw=0.8, zorder=20)
            a.plot([off - 0.04, off + 0.04], [v - 0.04, v + 0.04], color=K, lw=1.2, zorder=20)
        a.text(off + (0.25 if flip else -0.25), (p + q) / 2, txt, ha="center", va="center", fontsize=fs,
               rotation=90, zorder=21)


def num(a, x, y, n):
    a.text(x, y, str(n), ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=31,
           bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=K, lw=1.1))


# ================================================================ PLANTA
R(ax, 0.1, 3.6, 2.13, 4.7, fc=G2, ec=G3, lw=0.9, hatch="....", zorder=1)                     # escalera existente
R(ax, 0, 2.0, -1.0, 0.0, fc=G1, ec=K, lw=1.3, zorder=3)                                       # zapata que se conserva
R(ax, 0, 2.9, 0.0, 2.1, fc="white", ec=K, lw=1.8, hatch="xxx", zorder=4)                      # cajón (concreto nuevo)
R(ax, 0.2, 2.7, 0.2, 1.9, fc="white", ec=K, lw=1.1, zorder=5)                                 # pozo libre
R(ax, 0, 2.0, 0.0, 1.0, fc="none", ec=K, lw=1.3, ls=(0, (5, 3)), zorder=7)                    # zapata a demoler (contorno)
R(ax, 0.3, 4.4, -0.2, 0.2, fc="white", ec=K, lw=1.3, hatch="////", zorder=6)                  # viga de enlace
R(ax, 0, 0.3, -0.5, 0.5, fc=K, ec=K, zorder=8)                                                # columna D5
ax.plot([-1.0, 4.9], [0, 0], color=G3, lw=0.8, ls=(0, (8, 2, 1, 2)), zorder=2)                # eje 5
ax.text(5.0, 0.0, "EJE 5", fontsize=8, va="center", ha="right")
ax.axvline(0, color=K, lw=3.2, zorder=9)
ax.text(0.0, -2.1, "LINDERO", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(-0.25, -0.75, "D5", fontsize=9, fontweight="bold", ha="left", va="center")
ax.text(1.45, 1.38, "POZO LIBRE", ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=22, bbox=dict(fc="white", ec="none", pad=1.5))
ax.text(2.2, 3.4, "ESCALERA EXISTENTE", ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=22,
        bbox=dict(fc="white", ec="none", pad=1.5))
# cotas
dim(ax, 0.2, 2.7, 1.68, "2,50 libres")
dim(ax, 0.2, 1.9, 2.2, "1,70 libres", horiz=False, flip=True)
dim(ax, 0, 2.0, -1.28, "2,00  (Z1 existente)")
dim(ax, 0, 2.9, -1.68, "2,90  (huella exterior del cajón)")
dim(ax, 0, 2.1, -1.3, "2,10 ext. (muros 0,20)", horiz=False)
dim(ax, 0, 1.0, -1.85, "1,00 a demoler", horiz=False)
ax.plot([3.55, 3.55], [2.1, 2.13], color=K, lw=2.2, zorder=21)
ax.annotate("holgura ≈ 0,03 m\n(medir en obra)", xy=(3.55, 2.115), xytext=(4.6, 1.95), fontsize=7.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.7))
# llamadas numeradas
num(ax, 1.0, -0.55, 1); num(ax, 0.95, 0.8, 2); num(ax, 2.8, 0.1, 3); num(ax, 3.7, 0.0, 4); num(ax, 3.0, 4.2, 5)
# línea de corte B-B
ax.plot([-0.95, 3.55], [0.5, 0.5], color=K, lw=1.1, ls=(0, (10, 2, 2, 2)), zorder=12)
for xx in (-0.95, 3.55):
    ax.plot([xx, xx], [0.3, 0.7], color=K, lw=2.4, zorder=12)
    ax.text(xx + (0.0), 1.0, "B", fontsize=10, fontweight="bold", ha="center", va="center")
# barra gráfica
R(ax, 5.4, 6.4, 4.45, 4.55, fc=K, ec=K, zorder=5); R(ax, 6.4, 6.9, 4.45, 4.55, fc="white", ec=K, lw=0.8, zorder=5)
ax.text(5.4, 4.3, "0", fontsize=7, ha="center", va="top"); ax.text(6.4, 4.3, "1 m", fontsize=7, ha="center", va="top")
ax.set_xlim(7.2, -2.4); ax.set_ylim(4.8, -2.4); ax.set_aspect("equal")
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for sp in ax.spines.values():
    sp.set_linewidth(0.8)
ax.set_title("PLANTA – zona de D5 (cimentación)", fontsize=11, fontweight="bold", loc="left")

# ================================================================ CORTE B-B
SX = 5.2                                                                                      # borde izquierdo del suelo dibujado
bx.add_patch(Rectangle((-1.2, -2.0), SX + 1.2, 2.0, fc=G2, ec="none", hatch="---", zorder=1))
bx.add_patch(Rectangle((-1.2, -3.3), SX + 1.2, 1.3, fc=G1, ec="none", hatch="ooo", zorder=1))
bx.plot([-1.2, SX], [-2.0, -2.0], color=K, lw=0.8, zorder=2)
for yy in (0.0, -3.3):
    bx.plot([-1.2, SX], [yy, yy], color=K, lw=0.6, zorder=2)
R(bx, 0.2, 2.7, -1.5, 0.0, fc="white", ec="none", zorder=3)                                    # pozo
R(bx, 0.0, 2.9, -2.0, -1.55, fc="white", ec=K, lw=1.8, hatch="xxx", zorder=4)                   # losa-zapata
R(bx, 0.0, 0.2, -1.55, 0.0, fc="white", ec=K, lw=1.8, hatch="xxx", zorder=4)                    # muros
R(bx, 2.7, 2.9, -1.55, 0.0, fc="white", ec=K, lw=1.8, hatch="xxx", zorder=4)
R(bx, 0.2, 2.7, -1.55, -1.5, fc=G1, ec=K, lw=0.6, zorder=4)                                     # acabado
R(bx, 0.0, 2.9, -2.55, -2.0, fc="none", ec=K, lw=1.0, ls=(0, (5, 3)), zorder=4)                 # opción A descartada
bx.axvline(0, color=K, lw=3.2, zorder=9)
bx.text(0, 0.8, "LINDERO", ha="center", va="center", fontsize=9, fontweight="bold")
bx.plot([-1.2, SX], [0, 0], color=K, lw=2.0, zorder=6)
bx.text(1.45, -0.62, "POZO LIBRE", ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=8)
dim(bx, 0.2, 2.7, -0.2, "2,50 libres", flip=False)
dim(bx, -2.0, -1.55, 3.45, "0,45", horiz=False, flip=True)
bx.text(1.45, -1.78, "LOSA-ZAPATA ≤ 0,45", ha="center", va="center", fontsize=7.8, fontweight="bold", zorder=8,
        bbox=dict(fc="white", ec="none", pad=0.8))
bx.text(1.45, -2.28, "opción A (descartada)", ha="center", va="center", fontsize=7.5, style="italic", zorder=8,
        bbox=dict(fc=G1, ec="none", pad=0.8))
bx.text(SX - 0.1, -0.9, "ARCILLA firme", fontsize=8, ha="left", va="center", style="italic", zorder=8, bbox=dict(fc="white", ec="none", pad=1.0))
bx.text(SX - 0.1, -2.9, "GRAVA\nmedia-suelta", fontsize=8, ha="left", va="center", style="italic", zorder=8, bbox=dict(fc="white", ec="none", pad=1.0))
# niveles (a la izquierda del suelo)
for z, t in ((0.0, "±0,00  piso terminado del sótano\n= terreno de los sondeos"),
             (-1.5, "−1,50  fondo terminado del foso"),
             (-2.0, "−2,00  base del cajón = base de Z1\nexistente (contacto arcilla/grava)"),
             (-2.55, "−2,55  opción A descartada\n(0,55 m dentro de la grava)")):
    bx.plot([2.95, SX], [z, z], color=K, lw=0.6, ls=(0, (6, 2)), zorder=7)
    bx.text(SX + 0.2, z, t, fontsize=7.8, va="center", ha="right", zorder=8)
bx.set_xlim(11.6, -1.3); bx.set_ylim(-3.4, 1.1)
bx.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for sp in bx.spines.values():
    sp.set_linewidth(0.8)
bx.set_title("CORTE B–B – por el foso (perpendicular al lindero)", fontsize=11, fontweight="bold", loc="left")

# ================================================================ LEYENDA
lg.set_xlim(0, 1); lg.set_ylim(0, 1)
lg.text(0, 0.97, "REFERENCIAS", fontsize=9.5, fontweight="bold", va="top")
items = ["Zapata Z1 existente 2,0 x 2,0 m: se conserva la parte norte (hasta el eje 5).",
         "Demolición de 1,0 m de zapata, previo apuntalamiento de la columna y transferencia de carga.",
         "Cajón del foso: losa-zapata ≤ 0,45 m y muros de 0,20 m (concreto nuevo); pozo libre 1,70 x 2,50 m.",
         "Viga de enlace del eje 5: 0,40 x 1,00 m (nueva / reforzada) hacia A5.",
         "Escalera existente: no se interviene."]
for i, t in enumerate(items):
    y = 0.80 - i * 0.14
    lg.text(0.012, y, str(i + 1), fontsize=8, ha="center", va="center", fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=K, lw=1.0))
    lg.text(0.035, y, t, fontsize=8.5, va="center")
# simbología
sx = 0.0; sy = 0.04
for k, (hatch, fc, lab, ls) in enumerate((("xxx", "white", "concreto nuevo", "-"), ("", G1, "concreto existente", "-"),
                                          ("", "white", "a demoler / descartado", "--"))):
    lg.add_patch(Rectangle((sx + k * 0.30, sy), 0.035, 0.07, fc=fc, ec=K, lw=1.0, hatch=hatch, ls=ls, transform=lg.transAxes))
    lg.text(sx + k * 0.30 + 0.045, sy + 0.035, lab, fontsize=8, va="center")

# ================================================================ ROTULO
tb.set_xlim(0, 1); tb.set_ylim(0, 1)
tb.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=K, lw=1.3))
tb.plot([0, 1], [0.60, 0.60], color=K, lw=0.8); tb.plot([0, 1], [0.28, 0.28], color=K, lw=0.8); tb.plot([0.55, 0.55], [0, 0.28], color=K, lw=0.8)
tb.text(0.03, 0.92, "RECALCE DE D5 POR INTERFERENCIA CON EL FOSO DEL ASCENSOR", fontsize=10, fontweight="bold", va="top")
tb.text(0.03, 0.74, "Edificio multifamiliar – esquema de la solución propuesta", fontsize=8.5, va="top")
tb.text(0.03, 0.52, "ESQUEMA PRELIMINAR – NO PARA CONSTRUCCIÓN", fontsize=9, fontweight="bold", va="top")
tb.text(0.03, 0.43, "Sujeto a: cargas reales de D3/A3, restricción al giro,\ncriterio del geotecnista y medición en obra.", fontsize=7.5, va="top")
tb.text(0.03, 0.17, "Dimensiones en metros", fontsize=8, va="center")
tb.text(0.58, 0.17, "Fecha: 2026-10-13", fontsize=8, va="center")
fig.savefig("solucion_plano.png", dpi=150)
