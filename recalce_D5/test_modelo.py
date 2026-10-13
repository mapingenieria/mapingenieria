"""Verificaciones del modelo contra soluciones cerradas (python3 test_modelo.py)."""
import numpy as np
import modelo_parrilla as m


def test_voladizo():
    # voladizo con carga en el extremo: w = P L^3 / (3 EI), giro = P L^2 / (2 EI)
    L, EI, GJ, P = 3.0, 5e4, 1e3, 100.0
    K = m.beam_k(L, EI, GJ, along_x=True)
    free = [3, 4]                                   # w2, a2 libres
    u = np.linalg.solve(K[np.ix_(free, free)], np.array([P, 0.0]))
    assert abs(u[0] - P * L**3 / (3 * EI)) < 1e-9
    assert abs(u[1] - P * L**2 / (2 * EI)) < 1e-9


def test_torsion():
    L, EI, GJ, T = 2.0, 5e4, 1e3, 10.0
    K = m.beam_k(L, EI, GJ, along_x=True)           # torsion en dof b (indice 2)
    u = T * L / GJ
    assert abs(K[5, 5] * u - T) < 1e-9


def test_zapata_centrada():
    f = dict(Bx=2.0, By=2.0, yoff=0.0, ks=1e4)
    K, g = m.footing_k("A5", f)
    kv = g[4]
    assert abs(kv - 4e4) < 1e-6
    # zapata excentrica: giro libre -> el resorte del nodo debe tener acople w-a = kv*dx
    assert abs(K[0, 1] - kv * g[2]) < 1e-6


def test_equilibrio_y_variantes():
    w0 = m.W_TOTAL
    m.W_TOTAL = m.calibrate_W()                     # carga que lleva Z1 original a q_adm
    r = m.run_all()
    m.W_TOTAL = w0
    for n, v in r.items():
        assert abs(v["equil_err_kN"]) < 1e-6, n     # sum R = sum cargas + peso de vigas
    base = r["Base (Z1 original)"]["metrics"]
    assert abs(base["p_max_global_ratio"] - 1.0) < 1e-3


if __name__ == "__main__":
    for k, fn in list(globals().items()):
        if k.startswith("test_"):
            fn(); print("OK ", k)
