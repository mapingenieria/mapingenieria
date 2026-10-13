#!/usr/bin/env python3
"""
Modelo PRELIMINAR de parrilla de cimentación para comparar alternativas de
recalce de la zapata D5 (variantes A, A2, B, C).

Unidades: kN, m, kPa.  Cargas SOLO gravitacionales de servicio.

ADVERTENCIA: las cargas, las secciones de vigas, los ks del suelo y la posición
del foso son SUPUESTOS DE TRABAJO (ver SUPUESTOS abajo y resultados.md). El
modelo sirve para comparar tendencias entre alternativas, no para diseñar.

Modelo: parrilla de vigas (flexión + torsión, 3 GDL por nodo: w, a=dw/dx,
b=dw/dy) apoyada en resortes Winkler bajo cada zapata. Cada zapata se une
rígidamente al nodo de la columna (excentricidad zapata-columna incluida).
No incluye la rigidez de la superestructura ni sismo.

Uso:  python3 modelo_parrilla.py   -> escribe resultados.json
"""
import json
import math
import copy
import numpy as np

# ------------------------------------------------------------------ SUPUESTOS
XA, XC, XD = 0.0, 3.88, 6.74                      # ejes A, C, D (plano)
YAX = {1: 0.0, 3: 4.36, 5: 8.79, 6: 13.14}        # ejes 1,3,5,6 (m desde eje 1)
COL_T = 0.30                                      # espesor de columna (perp. lindero)
FPC = 21.0                                        # MPa (supuesto)
EC = 3900.0 * math.sqrt(FPC) * 1e3                # kPa, NSR-10 C.8.5.1
NU_C = 0.20
GC = EC / (2 * (1 + NU_C))
FY = 420.0                                        # MPa

H_STORY = 3.0          # m, altura de entrepiso (SUPUESTO) para el resorte de la superestructura
SUPER_MULT = 1.0       # multiplicador de la restriccion rotacional de la superestructura
SUPER_SPRING = True    # columnas 0,30x1,00 arriba del nodo restringen el giro a (eje debil)
KS_CLAY = 60_000.0     # kN/m3  (E=10000 t/m2, nu=0.35, B=1.8 m -> ~62 000)
KS_GRAVEL = 25_000.0   # kN/m3  SUPUESTO: grava media-suelta, sin datos del estudio
EI_FACTOR = 0.50       # fisuración en servicio
GJ_FACTOR = 0.10
QADM_CLAY = 323.65     # kPa, estudio de suelos (Df=2.00 m, B=1.8 m)

W_TOTAL = 6000.0       # kN servicio, SUPUESTO (~9 kN/m2 x 6,5 niveles x 103 m2)
Y_TRIB = {1: 3.75, 3: 4.40, 5: 4.39, 6: 2.50}     # ancho tributario por eje (m)

SEC = {                 # (b, h) en m
    "T": (0.40, 0.55),  # VC.S-55x40 transversales, ejes 1,3,5,6 (interpretado 40 ancho x 55 alto)
    "L": (0.35, 0.45),  # VC.S-6 longitudinal eje C (SUPUESTO)
    "P": (0.40, 0.55),  # vigas de lindero (SUPUESTO: igual a VC.S-55x40)
}

Z1 = dict(Bx=1.80, By=1.80, yoff=0.0, ks=KS_CLAY)  # zapata original (todas iguales)


# ------------------------------------------------------------------ geometría
def node_xy(name):
    col, ax = name[0], int(name[1:])
    return {"A": XA, "C": XC, "D": XD}[col], YAX[ax]


def build_nodes():
    names = [f"{c}{a}" for a in YAX for c in "ACD"]
    return {n: i for i, n in enumerate(names)}


def build_beams(over=None):
    """Lista de vigas (ni, nj, tipo_seccion, etiqueta). `over` cambia secciones."""
    beams = []
    axes = list(YAX)
    for a in axes:                                  # transversales A-C-D
        beams.append((f"A{a}", f"C{a}", "T", f"VC eje {a} (A-C)"))
        beams.append((f"C{a}", f"D{a}", "T", f"VC eje {a} (C-D)"))
    for a0, a1 in zip(axes[:-1], axes[1:]):         # longitudinal central
        beams.append((f"C{a0}", f"C{a1}", "L", f"VC.S-6 {a0}-{a1}"))
    for col in "AD":                                # linderos
        for a0, a1 in zip(axes[:-1], axes[1:]):
            beams.append((f"{col}{a0}", f"{col}{a1}", "P", f"Lindero {col} {a0}-{a1}"))
    out = []
    for ni, nj, t, lab in beams:
        sec = (over or {}).get(lab, SEC[t])
        out.append((ni, nj, sec, lab))
    return out


def column_loads(W=None):
    s = sum(Y_TRIB.values())
    return {f"{c}{a}": (W or W_TOTAL) / 2 * Y_TRIB[a] / s for c in "AD" for a in YAX}


# ------------------------------------------------------------------ elementos
def sec_props(b, h):
    I = b * h**3 / 12 * EI_FACTOR
    lo, hi = min(b, h), max(b, h)
    J = (1 / 3) * hi * lo**3 * (1 - 0.63 * lo / hi) * GJ_FACTOR
    return EC * I, GC * J


def beam_k(L, EI, GJ, along_x):
    kb = EI / L**3 * np.array([[12, 6 * L, -12, 6 * L],
                               [6 * L, 4 * L**2, -6 * L, 2 * L**2],
                               [-12, -6 * L, 12, -6 * L],
                               [6 * L, 2 * L**2, -6 * L, 4 * L**2]])
    kt = GJ / L * np.array([[1, -1], [-1, 1]])
    # dofs globales por nodo: 0=w, 1=a(dw/dx), 2=b(dw/dy)
    bend = [0, 1] if along_x else [0, 2]
    tors = 2 if along_x else 1
    idx = [(0, bend[0]), (0, bend[1]), (1, bend[0]), (1, bend[1])]
    K = np.zeros((6, 6))
    for p, (ni, di) in enumerate(idx):
        for q, (nj, dj) in enumerate(idx):
            K[ni * 3 + di, nj * 3 + dj] += kb[p, q]
    for p, ni in enumerate((0, 1)):
        for q, nj in enumerate((0, 1)):
            K[ni * 3 + tors, nj * 3 + tors] += kt[p, q]
    return K


def x_range(node, f):
    x, _ = node_xy(node)
    sgn = +1 if node[0] == "A" else -1
    edge = x - sgn * COL_T / 2                     # cara exterior (lindero)
    return sorted((edge, edge + sgn * f["Bx"]))


def footing_k(node, f, contact=None):
    """Matriz 3x3 del resorte de suelo referida al nodo de la columna.
    `contact` = (x1, x2) zona realmente en compresion (sin tracciones)."""
    x, y = node_xy(node)
    x1, x2 = contact or x_range(node, f)
    bx = x2 - x1
    cx = (x1 + x2) / 2
    cy = y + f["yoff"]
    dx, dy = cx - x, cy - y
    kv = f["ks"] * bx * f["By"]
    ka = f["ks"] * bx ** 3 * f["By"] / 12
    kb = f["ks"] * bx * f["By"] ** 3 / 12
    T = np.array([[1, dx, dy], [0, 1, 0], [0, 0, 1]])
    return T.T @ np.diag([kv, ka, kb]) @ T, (cx, cy, dx, dy, kv, bx)


# ------------------------------------------------------------------ solución
def solve(footings, beam_over=None, loads=None, contacts=None):
    nodes = build_nodes()
    beams = build_beams(beam_over)
    n = len(nodes)
    K = np.zeros((3 * n, 3 * n))
    F = np.zeros(3 * n)
    P = loads or column_loads()
    for nm, p in P.items():
        F[nodes[nm] * 3] += p
    geo = {}
    for ni, nj, (b, h), lab in beams:
        xi, yi = node_xy(ni)
        xj, yj = node_xy(nj)
        along_x = abs(yi - yj) < 1e-9
        L = abs(xj - xi) if along_x else abs(yj - yi)
        EI, GJ = sec_props(b, h)
        ke = beam_k(L, EI, GJ, along_x)
        ii, jj = nodes[ni] * 3, nodes[nj] * 3
        ix = list(range(ii, ii + 3)) + list(range(jj, jj + 3))
        K[np.ix_(ix, ix)] += ke
        q = 25.0 * b * h                           # peso propio de la viga (kN/m)
        feq = np.zeros(6)
        bend = [0, 1] if along_x else [0, 2]
        feq[bend[0]] += q * L / 2
        feq[bend[1]] += q * L**2 / 12
        feq[3 + bend[0]] += q * L / 2
        feq[3 + bend[1]] += -q * L**2 / 12
        for k, g in enumerate(ix):
            F[g] += feq[k]
    for nm, f in footings.items():
        if f is None:
            continue
        kf, g = footing_k(nm, f, (contacts or {}).get(nm))
        i0 = nodes[nm] * 3
        K[i0:i0 + 3, i0:i0 + 3] += kf
        geo[nm] = g
    if SUPER_SPRING:
        ksup = SUPER_MULT * 4 * EC * (COL_T**3 * 1.00 / 12) * EI_FACTOR / H_STORY
        for nm in P:
            K[nodes[nm] * 3 + 1, nodes[nm] * 3 + 1] += ksup
    u = np.linalg.solve(K, F)
    return dict(nodes=nodes, beams=beams, u=u, footings=footings, geo=geo, P=P)


def solve_nt(footings, beam_over=None, loads=None, iters=60):
    """Resuelve con zapatas sin tracción: reduce la zona de contacto hasta converger."""
    contacts = {}
    for _ in range(iters):
        res = solve(footings, beam_over, loads, contacts)
        changed = False
        u, nodes = res["u"], res["nodes"]
        for nm, f in footings.items():
            if f is None:
                continue
            cx, cy, dx, dy, kv, bx = res["geo"][nm]
            w, a, b = u[nodes[nm] * 3: nodes[nm] * 3 + 3]
            wc = w + a * dx + b * dy
            x1, x2 = contacts.get(nm) or x_range(nm, f)
            if abs(a) < 1e-12:
                continue
            x0 = cx - wc / a                       # p = ks*(wc + a(x-cx)) = 0
            p1, p2 = wc + a * (x1 - cx), wc + a * (x2 - cx)
            new = [x1, x2]
            if p1 < -1e-9:
                new[0] = min(max(x0, x1), x2 - 0.05)
            if p2 < -1e-9:
                new[1] = max(min(x0, x2), x1 + 0.05)
            if abs(new[0] - x1) > 1e-4 or abs(new[1] - x2) > 1e-4:
                contacts[nm] = tuple(new)
                changed = True
        if not changed:
            break
    res["contacts"] = contacts
    return res


def post(res):
    nodes, u = res["nodes"], res["u"]
    out = {"footings": {}, "beams": {}}
    for nm, f in res["footings"].items():
        if f is None:
            continue
        cx, cy, dx, dy, kv, bx = res["geo"][nm]
        w, a, b = u[nodes[nm] * 3: nodes[nm] * 3 + 3]
        wc = w + a * dx + b * dy
        R = kv * wc
        pmax = f["ks"] * (wc + abs(a) * bx / 2 + abs(b) * f["By"] / 2)
        pmin = f["ks"] * (wc - abs(a) * bx / 2 - abs(b) * f["By"] / 2)
        out["footings"][nm] = dict(R=R, R_over_P=R / res["P"].get(nm, np.nan),
                                   settle_mm=wc * 1000, p_avg=R / (f["Bx"] * f["By"]),
                                   p_max=pmax, p_min=pmin, e_x=dx, Bx=f["Bx"], By=f["By"],
                                   contact_frac=bx / f["Bx"])
    for ni, nj, (b, h), lab in res["beams"]:
        xi, yi = node_xy(ni)
        xj, yj = node_xy(nj)
        along_x = abs(yi - yj) < 1e-9
        L = abs(xj - xi) if along_x else abs(yj - yi)
        EI, GJ = sec_props(b, h)
        ui = u[nodes[ni] * 3: nodes[ni] * 3 + 3]
        uj = u[nodes[nj] * 3: nodes[nj] * 3 + 3]
        d = [0, 1] if along_x else [0, 2]
        w1, t1, w2, t2 = ui[d[0]], ui[d[1]], uj[d[0]], uj[d[1]]
        q = 25.0 * b * h
        Ms = []
        for s in np.linspace(0, L, 41):
            wpp = ((-6 / L**2 + 12 * s / L**3) * w1 + (-4 / L + 6 * s / L**2) * t1
                   + (6 / L**2 - 12 * s / L**3) * w2 + (-2 / L + 6 * s / L**2) * t2)
            wpp += q / (12 * EI) * (6 * s**2 - 6 * L * s + L**2)
            Ms.append(-EI * wpp)
        tw = (uj[2] - ui[2]) / L if along_x else -(uj[1] - ui[1]) / L
        out["beams"][lab] = dict(M_sag=max(Ms), M_hog=min(Ms), T=abs(GJ * tw),
                                 L=L, b=b, h=h)
    return out


def phiMn(b, h, rho=0.01):
    d = h - 0.06
    As = rho * b * d
    a = As * FY * 1e3 / (0.85 * FPC * 1e3 * b)
    return 0.9 * As * FY * 1e3 * (d - a / 2)


# ------------------------------------------------------------------ variantes
def variants(ks_c=KS_CLAY, ks_g=KS_GRAVEL):
    z = lambda **k: dict(Z1, ks=ks_c, **{kk: vv for kk, vv in k.items()})
    base = {f"{c}{a}": dict(Z1, ks=ks_c) for c in "AD" for a in YAX}
    V = {}
    V["Base (Z1 original)"] = (copy.deepcopy(base), None)
    A = copy.deepcopy(base)
    A["D5"] = dict(Bx=1.80, By=1.80, yoff=0.0, ks=ks_g)
    V["A  zapata nueva profunda (grava)"] = (A, None)
    A2 = copy.deepcopy(base)
    A2["D5"] = dict(Bx=2.10, By=2.90, yoff=0.0, ks=ks_c)
    V["A2 cajon del foso integrado"] = (A2, None)
    B = copy.deepcopy(base)
    B["D5"] = dict(Bx=1.20, By=3.00, yoff=0.0, ks=ks_c)
    V["B  zapata angosta y larga"] = (B, None)
    C = copy.deepcopy(base)
    C["D5"] = None
    C["D3"] = dict(Bx=2.20, By=2.20, yoff=0.0, ks=ks_c)
    C["D6"] = dict(Bx=2.20, By=2.20, yoff=0.0, ks=ks_c)
    over = {"Lindero D 3-5": (0.40, 1.20), "Lindero D 5-6": (0.40, 1.20)}
    V["C  D5 colgada de viga de lindero"] = (C, over)
    T0 = copy.deepcopy(base)
    T0["D5"] = None
    V["T0 transicion: D5 sin zapata, vigas actuales"] = (T0, None)
    return V


def loads_now():
    return column_loads(W_TOTAL)


def metrics(name, res, pst):
    f = pst["footings"]
    P = res["P"]
    clay_p = [v["p_max"] for k, v in f.items() if not (k == "D5" and name.startswith("A  "))]
    settles = [v["settle_mm"] for v in f.values()]
    beams = pst["beams"]
    def worst(labels):
        best = None
        for l in labels:
            m = max(abs(beams[l]["M_sag"]), abs(beams[l]["M_hog"]))
            if best is None or m > best[1]:
                best = (l, m)
        return best
    ties5 = [l for l in beams if l.startswith("VC eje 5")]
    lindD = [l for l in beams if l.startswith("Lindero D")]
    d5 = f.get("D5")
    m = dict(
        D5_R_over_P=(d5["R_over_P"] if d5 else 0.0),
        D5_p_max=(d5["p_max"] if d5 else None),
        D5_p_min=(d5["p_min"] if d5 else None),
        D5_settle_mm=(d5["settle_mm"] if d5 else None),
        A5_R_over_P=f["A5"]["R_over_P"], A5_p_max=f["A5"]["p_max"],
        D3_R_over_P=f["D3"]["R_over_P"], D3_p_max=f["D3"]["p_max"],
        D6_R_over_P=f["D6"]["R_over_P"], D6_p_max=f["D6"]["p_max"],
        p_max_global=max(clay_p), p_max_global_ratio=max(clay_p) / QADM_CLAY,
        min_R_over_P=min(v["R_over_P"] for v in f.values()),
        dif_settle_mm=max(settles) - min(settles),
        M_tie5=worst(ties5), M_lindD=worst(lindD),
        T_max=max(b["T"] for b in beams.values()),
    )
    for key, labs in (("M_tie5", ties5), ("M_lindD", lindD)):
        lab, mv = m[key]
        b, h = beams[lab]["b"], beams[lab]["h"]
        m[key] = dict(label=lab, M=mv, phiMn_ref=phiMn(b, h))
    return m


def run_all(ks_c=KS_CLAY, ks_g=KS_GRAVEL):
    out = {}
    for name, (foot, over) in variants(ks_c, ks_g).items():
        res = solve_nt(foot, over, loads=loads_now())
        pst = post(res)
        # control de equilibrio
        tot_R = sum(v["R"] for v in pst["footings"].values())
        beam_w = sum(25 * b * h * (abs(xj - xi) + abs(yj - yi))
                     for ni, nj, (b, h), _ in res["beams"]
                     for (xi, yi), (xj, yj) in [(node_xy(ni), node_xy(nj))])
        eq = tot_R - (sum(res["P"].values()) + beam_w)
        out[name] = dict(metrics=metrics(name, res, pst), equil_err_kN=eq, post=pst)
    return out


def calibrate_W(target=QADM_CLAY):
    """W_TOTAL para el cual la presión máxima del caso base iguala q_adm (arcilla)."""
    global W_TOTAL
    w0 = W_TOTAL
    lo, hi = 300.0, 8000.0
    for _ in range(50):
        W_TOTAL = (lo + hi) / 2
        r = run_all()["Base (Z1 original)"]["metrics"]["p_max_global"]
        lo, hi = (W_TOTAL, hi) if r < target else (lo, W_TOTAL)
    wcal = W_TOTAL
    W_TOTAL = w0
    return wcal


def sensitivity():
    rows = []
    global EI_FACTOR
    ei0 = EI_FACTOR
    for ks_c in (30_000, 60_000, 120_000):
        for ks_g in (15_000, 25_000, 60_000):
            for ei in (0.35, 0.5, 1.0):
                EI_FACTOR = ei
                r = run_all(ks_c, ks_g)
                rows.append(dict(ks_c=ks_c, ks_g=ks_g, ei=ei,
                                 res={n: v["metrics"] for n, v in r.items()}))
    EI_FACTOR = ei0
    return rows


if __name__ == "__main__":
    W_PLACEHOLDER = W_TOTAL
    W_CAL = calibrate_W()
    W_TOTAL = W_CAL                     # todo el análisis principal a carga calibrada
    base = run_all()
    sens = sensitivity()
    W_TOTAL = W_PLACEHOLDER
    base_ph = run_all()
    print(f"W_TOTAL placeholder = {W_PLACEHOLDER:.0f} kN ; W calibrado (Z1 base = q_adm) = {W_CAL:.0f} kN ;"
          f" P_D5 calibrada = {column_loads(W_CAL)['D5']:.0f} kN")
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return float(o)
        return o
    json.dump(clean(dict(base=base, base_placeholder=base_ph, sens=sens,
                         W_cal=W_CAL, W_placeholder=W_PLACEHOLDER, P_cal=column_loads(W_CAL),
                         P_placeholder=column_loads(W_PLACEHOLDER))),
              open("resultados.json", "w"), indent=1)
    for n, v in base.items():
        m = v["metrics"]
        print(f"{n:48s} D5 R/P={m['D5_R_over_P']:.2f}  pmax D5="
              f"{m['D5_p_max'] if m['D5_p_max'] is not None else float('nan'):6.0f}  "
              f"pglob={m['p_max_global']:.0f} ({m['p_max_global_ratio']:.2f} qadm)  "
              f"Mtie5={m['M_tie5']['M']:.0f}/{m['M_tie5']['phiMn_ref']:.0f}  "
              f"MlindD={m['M_lindD']['M']:.0f}/{m['M_lindD']['phiMn_ref']:.0f}  "
              f"eq={v['equil_err_kN']:.2e}")
