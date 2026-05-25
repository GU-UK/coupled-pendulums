import numpy as np


def coupled_pendulums(t, y, L, m, k, L1, beta, g=9.81):

    phi1, omega1, phi2, omega2 = y

    coupling = (k * L1**2) / (m * L**2)

    dphi1 = omega1

    domega1 = (
        -beta * omega1
        - (g / L) * phi1
        - coupling * (phi1 - phi2)
    )

    dphi2 = omega2

    domega2 = (
        -beta * omega2
        - (g / L) * phi2
        - coupling * (phi2 - phi1)
    )

    return [
        dphi1,
        domega1,
        dphi2,
        domega2
    ]