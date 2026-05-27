"""
Zone-level SIR ODE system.

State vector y (length 3n, n=9 zones):
  y[0:n]    = S_i
  y[n:2n]   = I_i
  y[2n:3n]  = R_i

lambda_i(t) = beta * [ rho * I_i/N_i + (1-rho) * sum_j W_hat_ij * I_j/N_j ]
dS_i/dt = -lambda_i * S_i
dI_i/dt =  lambda_i * S_i - mu * I_i
dR_i/dt =  mu * I_i
"""
import numpy as np
from scipy.integrate import solve_ivp


def sir_rhs(t, y, beta, mu, rho, W_hat, N):
    """RHS of the zone-level SIR ODE."""
    n = len(N)
    S = y[0:n]
    I = y[n:2*n]

    prevalence = I / N
    network_force = W_hat @ prevalence

    lam = beta * (rho * prevalence + (1 - rho) * network_force)

    dS = -lam * S
    dI =  lam * S - mu * I
    dR =  mu  * I
    return np.concatenate([dS, dI, dR])


def make_y0(seed_zone_idx: int, seed_count: float, N: np.ndarray) -> np.ndarray:
    """Initial state with seed_count infected in one zone."""
    n = len(N)
    S0 = N.copy()
    I0 = np.zeros(n)
    R0 = np.zeros(n)
    I0[seed_zone_idx] = seed_count
    S0[seed_zone_idx] -= seed_count
    return np.concatenate([S0, I0, R0])


def run_simulation(y0, beta, mu, rho, W_hat, N, t_span=(0, 30), t_eval=None):
    """Integrate the zone-level SIR system."""
    if t_eval is None:
        t_eval = np.linspace(t_span[0], t_span[1], 1000)

    sol = solve_ivp(
        sir_rhs,
        t_span,
        y0,
        method="RK45",
        args=(beta, mu, rho, W_hat, N),
        t_eval=t_eval,
        dense_output=True,
        rtol=1e-8,
        atol=1e-10,
    )
    assert sol.success, f"ODE solver failed: {sol.message}"
    return sol
