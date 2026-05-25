import numpy as np
from scipy.integrate import solve_ivp

from src.physics import coupled_pendulums


def run_simulation(
    L,
    m,
    k,
    L1,
    beta,
    phi1_0,
    phi2_0,
    duration,
    fps
):

    t_eval = np.linspace(
        0,
        duration,
        int(duration * fps)
    )

    y0 = [
        phi1_0,
        0,
        phi2_0,
        0
    ]

    solution = solve_ivp(
        coupled_pendulums,
        [0, duration],
        y0,
        t_eval=t_eval,
        args=(
            L,
            m,
            k,
            L1,
            beta
        )
    )

    return {
        "t": solution.t,
        "phi1": solution.y[0],
        "omega1": solution.y[1],
        "phi2": solution.y[2],
        "omega2": solution.y[3]
    }