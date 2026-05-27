"""
Well-mixed SIR baseline.

dS/dt = -beta * S * I / N
dI/dt =  beta * S * I / N - mu * I
dR/dt =  mu * I
"""
import numpy as np
from scipy.integrate import solve_ivp


def wellmixed_rhs(t, y, beta, mu, N):
    S, I, R = y
    force = beta * I / N
    dS = -force * S
    dI =  force * S - mu * I
    dR =  mu * I
    return [dS, dI, dR]


def run_wellmixed(beta, mu, N_total, I0=5, t_span=(0, 30), t_eval=None):
    if t_eval is None:
        t_eval = np.linspace(t_span[0], t_span[1], 1000)

    y0 = [N_total - I0, float(I0), 0.0]
    sol = solve_ivp(
        wellmixed_rhs,
        t_span,
        y0,
        method="RK45",
        args=(beta, mu, N_total),
        t_eval=t_eval,
        dense_output=True,
        rtol=1e-8,
        atol=1e-10,
    )
    assert sol.success, f"Well-mixed ODE solver failed: {sol.message}"
    return sol
