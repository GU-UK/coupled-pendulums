import numpy as np


def normal_frequencies(L, m, k, L1, g=9.81):

    omega_in_phase = np.sqrt(g / L)

    omega_anti_phase = np.sqrt(
        (g / L) + (2 * k * L1**2) / (m * L**2)
    )

    return {
        "omega_in_phase": omega_in_phase,
        "omega_anti_phase": omega_anti_phase,
        "freq_in_phase": omega_in_phase / (2 * np.pi),
        "freq_anti_phase": omega_anti_phase / (2 * np.pi)
    }


def calculate_energy(result, L, m, k, L1, g=9.81):

    phi1 = result["phi1"]
    phi2 = result["phi2"]
    omega1 = result["omega1"]
    omega2 = result["omega2"]

    kinetic_1 = 0.5 * m * (L * omega1) ** 2
    kinetic_2 = 0.5 * m * (L * omega2) ** 2

    potential_1 = m * g * L * (1 - np.cos(phi1))
    potential_2 = m * g * L * (1 - np.cos(phi2))

    spring_energy = 0.5 * k * (L1 * (phi1 - phi2)) ** 2

    total_energy = (
        kinetic_1
        + kinetic_2
        + potential_1
        + potential_2
        + spring_energy
    )

    return {
        "kinetic_1": kinetic_1,
        "kinetic_2": kinetic_2,
        "potential_1": potential_1,
        "potential_2": potential_2,
        "spring_energy": spring_energy,
        "total_energy": total_energy
    }