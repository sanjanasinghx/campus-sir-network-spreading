"""
Run all four simulation scenarios and save results to data/.

Outputs:
  scen_A.npz          Scenario A: H2 seed (I_H2(0)=5)
  scen_B.npz          Scenario B: A seed (I_A(0)=5)
  wellmixed_B.npz     well-mixed baseline, same seed total as B
  intervention_A.npz  Scenario A with H2 isolation from day 7
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from network import NODES, IDX, POPULATIONS, W_HAT, N_TOTAL
from sir_network import make_y0, run_simulation
from sir_wellmixed import run_wellmixed

# Parameters
BETA = 0.34
MU   = 0.20
RHO  = 0.55
T_EVAL = np.linspace(0, 30, 1000)
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)


def save(name, sol, extra=None):
    path = os.path.join(OUT_DIR, name)
    data = {"t": sol.t, "y": sol.y}
    if extra:
        data.update(extra)
    np.savez(path, **data)
    print(f"  Saved {name}.npz  shape y={sol.y.shape}")


# Scenario A: H2 seed
print("Running Scenario A (H2 seed)...")
y0_A = make_y0(IDX["H2"], 5.0, POPULATIONS)
sol_A = run_simulation(y0_A, BETA, MU, RHO, W_HAT, POPULATIONS, t_eval=T_EVAL)
save("scen_A", sol_A)

# Scenario B: A seed
print("Running Scenario B (A seed)...")
y0_B = make_y0(IDX["A"], 5.0, POPULATIONS)
sol_B = run_simulation(y0_B, BETA, MU, RHO, W_HAT, POPULATIONS, t_eval=T_EVAL)
save("scen_B", sol_B)

# Well-mixed baseline (I(0)=5, N=2530, same as scenario B)
print("Running well-mixed baseline...")
sol_WM = run_wellmixed(BETA, MU, N_TOTAL, I0=5, t_eval=T_EVAL)
np.savez(os.path.join(OUT_DIR, "wellmixed_B.npz"), t=sol_WM.t, y=sol_WM.y)
print(f"  Saved wellmixed_B.npz  shape y={sol_WM.y.shape}")

# Intervention A: isolate H2 at day 7 (80% edge reduction)
print("Running Scenario A + H2 isolation at day 7...")

# t = 0 to 7 with the original W_hat
T1 = np.linspace(0, 7, 300)
sol_i1 = run_simulation(y0_A, BETA, MU, RHO, W_HAT, POPULATIONS, t_span=(0, 7), t_eval=T1)

# Rebuild W from raw weights, cut H2 edges by 80%, re-normalise
W_mod = W_HAT.copy()
from network import EDGES as _EDGES, IDX as _IDX
n = len(NODES)
W_raw = np.zeros((n, n))
for u, v, w in _EDGES:
    i, j = _IDX[u], _IDX[v]
    W_raw[i, j] = w
    W_raw[j, i] = w

h2 = IDX["H2"]
W_raw_mod = W_raw.copy()
W_raw_mod[h2, :] *= 0.2
W_raw_mod[:, h2] *= 0.2

row_sums = W_raw_mod.sum(axis=1, keepdims=True)
row_sums = np.where(row_sums == 0, 1.0, row_sums)
W_hat_mod = W_raw_mod / row_sums
assert np.allclose(W_hat_mod.sum(axis=1), 1.0), "Modified W_hat rows don't sum to 1"

# t = 7 to 30 with the modified W_hat, starting from the day-7 state
T2 = np.linspace(7, 30, 700)
y_day7 = sol_i1.y[:, -1]
sol_i2 = run_simulation(y_day7, BETA, MU, RHO, W_hat_mod, POPULATIONS, t_span=(7, 30), t_eval=T2)

t_int = np.concatenate([sol_i1.t, sol_i2.t[1:]])
y_int = np.concatenate([sol_i1.y, sol_i2.y[:, 1:]], axis=1)
np.savez(os.path.join(OUT_DIR, "intervention_A.npz"), t=t_int, y=y_int)
print(f"  Saved intervention_A.npz  shape y={y_int.shape}")

print("\nConservation check (S+I+R at t=30, should be 2530):")
for name, sol_y in [("Scen A", sol_A.y), ("Scen B", sol_B.y),
                    ("Intervention", y_int)]:
    n_nodes = 9
    total_final = sol_y[:, -1].reshape(3, n_nodes).sum()
    print(f"  {name}: total = {total_final:.4f}  (expected {N_TOTAL})")

print("\nDone.")
