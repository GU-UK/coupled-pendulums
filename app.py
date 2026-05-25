import streamlit as st
import matplotlib.pyplot as plt

from src.solver import run_simulation
from src.visualization import create_animation
from src.analysis import normal_frequencies, calculate_energy


st.set_page_config(
    page_title="Coupled Pendulums",
    layout="wide"
)


st.title("Моделирование связанных маятников")


PRESETS = {

    "Передача энергии": {
        "L": 1.0,
        "m": 1.0,
        "k": 6.0,
        "L1": 0.75,
        "beta": 0.02,
        "phi1": 0.35,
        "phi2": 0.0,
        "duration": 35
    },

    "Синфазный режим": {
        "L": 1.0,
        "m": 1.0,
        "k": 8.0,
        "L1": 0.8,
        "beta": 0.0,
        "phi1": 0.25,
        "phi2": 0.25,
        "duration": 20
    },

    "Противофазный режим": {
        "L": 1.0,
        "m": 1.0,
        "k": 8.0,
        "L1": 0.8,
        "beta": 0.0,
        "phi1": 0.25,
        "phi2": -0.25,
        "duration": 20
    },

    "Сильное затухание": {
        "L": 1.0,
        "m": 1.0,
        "k": 8.0,
        "L1": 0.8,
        "beta": 0.25,
        "phi1": 0.4,
        "phi2": 0.0,
        "duration": 30
    }
}


preset = st.sidebar.selectbox(
    "Предустановка",
    list(PRESETS.keys())
)

cfg = PRESETS[preset]

st.sidebar.divider()


def parameter(name, min_v, max_v, value, step):

    return st.sidebar.number_input(
        name,
        min_value=min_v,
        max_value=max_v,
        value=value,
        step=step
    )


L = parameter(
    "L — длина маятника, м",
    0.5,
    3.0,
    cfg["L"],
    0.01
)

m = parameter(
    "m — масса груза, кг",
    0.1,
    10.0,
    cfg["m"],
    0.1
)

k = parameter(
    "k — жёсткость пружины, Н/м",
    0.0,
    50.0,
    cfg["k"],
    0.1
)

max_L1 = round(0.95 * L, 2)

default_L1 = min(
    cfg["L1"],
    max_L1
)

L1 = parameter(
    "L1 — точка крепления пружины, м",
    0.1,
    max_L1,
    default_L1,
    0.01
)

st.sidebar.caption(
    f"Допустимый диапазон: 0.10 ≤ L1 ≤ {max_L1:.2f} м"
)

beta = parameter(
    "β — коэффициент затухания",
    0.0,
    1.0,
    cfg["beta"],
    0.01
)

phi1 = parameter(
    "φ1 — начальный угол 1, рад",
    -1.0,
    1.0,
    cfg["phi1"],
    0.01
)

phi2 = parameter(
    "φ2 — начальный угол 2, рад",
    -1.0,
    1.0,
    cfg["phi2"],
    0.01
)

duration = int(

    parameter(
        "Время моделирования, с",
        5,
        60,
        cfg["duration"],
        1
    )

)

if st.sidebar.button(
    "▶ Запустить моделирование",
    use_container_width=True
):

    result = run_simulation(
        L,
        m,
        k,
        L1,
        beta,
        phi1,
        phi2,
        duration,
        60
    )

    frequencies = normal_frequencies(
        L,
        m,
        k,
        L1
    )

    energy = calculate_energy(
        result,
        L,
        m,
        k,
        L1
    )

    st.subheader("Физические характеристики")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "ω₁, рад/с",
        f"{frequencies['omega_in_phase']:.3f}"
    )

    col2.metric(
        "ω₂, рад/с",
        f"{frequencies['omega_anti_phase']:.3f}"
    )

    col3.metric(
        "f₁, Гц",
        f"{frequencies['freq_in_phase']:.3f}"
    )

    col4.metric(
        "f₂, Гц",
        f"{frequencies['freq_anti_phase']:.3f}"
    )

    st.subheader("Анимация")

    st.plotly_chart(
        create_animation(
            result,
            L,
            L1
        ),
        use_container_width=True
    )

    st.subheader("График угловых скоростей")

    fig2, ax2 = plt.subplots(
        figsize=(10, 3.5)
    )

    ax2.plot(
        result["t"],
        result["omega1"],
        label="ω₁"
    )

    ax2.plot(
        result["t"],
        result["omega2"],
        label="ω₂"
    )

    ax2.set_xlabel("t, с")
    ax2.set_ylabel("ω, рад/с")
    ax2.grid()
    ax2.legend()

    st.pyplot(fig2)

    st.subheader("Энергия системы")

    fig3, ax3 = plt.subplots(
        figsize=(10, 3.5)
    )

    ax3.plot(
        result["t"],
        energy["total_energy"],
        label="Полная энергия"
    )

    ax3.plot(
        result["t"],
        energy["spring_energy"],
        label="Энергия пружины"
    )

    ax3.set_xlabel("t, с")
    ax3.set_ylabel("E, Дж")
    ax3.grid()
    ax3.legend()

    st.pyplot(fig3)