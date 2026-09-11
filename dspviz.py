#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# ============================================================
# Complex Exponential
# ============================================================

def complex_exponential():
    """
    Interactive visualization of:

        x(t) = A * exp(j(2*pi*f*t + phi))
    """

    A0 = 1.0
    f0 = 1.0
    phi0 = 0.0
    t0 = 0.0

    fig, ax = plt.subplots(figsize=(7, 7))
    plt.subplots_adjust(bottom=0.30)

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(
        np.cos(theta),
        np.sin(theta),
        "--",
        alpha=0.3
    )

    # Calculate initial complex value
    z = A0 * np.exp(
        1j * (2 * np.pi * f0 * t0 + phi0)
    )

    # Constellation point
    point, = ax.plot(
        [z.real],
        [z.imag],
        "o",
        markersize=10
    )

    # Vector
    vector, = ax.plot(
        [0, z.real],
        [0, z.imag],
        linewidth=2
    )

    # Axes
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")

    ax.set_xlabel("In-phase (I)")
    ax.set_ylabel("Quadrature (Q)")
    ax.set_title("Complex Exponential")

    ax.grid(True, alpha=0.3)

    # --------------------------------------------------------
    # Sliders
    # --------------------------------------------------------

    ax_A = plt.axes([0.15, 0.20, 0.70, 0.03])
    slider_A = Slider(
        ax_A,
        "Amplitude",
        0,
        2,
        valinit=A0
    )

    ax_f = plt.axes([0.15, 0.14, 0.70, 0.03])
    slider_f = Slider(
        ax_f,
        "Frequency",
        0,
        5,
        valinit=f0
    )

    ax_phi = plt.axes([0.15, 0.08, 0.70, 0.03])
    slider_phi = Slider(
        ax_phi,
        "Phase",
        -np.pi,
        np.pi,
        valinit=phi0
    )

    ax_t = plt.axes([0.15, 0.02, 0.70, 0.03])
    slider_t = Slider(
        ax_t,
        "Time",
        0,
        1,
        valinit=t0
    )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(_):

        A = slider_A.val
        f = slider_f.val
        phi = slider_phi.val
        t = slider_t.val

        z = A * np.exp(
            1j * (2 * np.pi * f * t + phi)
        )

        point.set_data(
            [z.real],
            [z.imag]
        )

        vector.set_data(
            [0, z.real],
            [0, z.imag]
        )

        fig.canvas.draw_idle()

    slider_A.on_changed(update)
    slider_f.on_changed(update)
    slider_phi.on_changed(update)
    slider_t.on_changed(update)

    plt.show()


# ============================================================
# CLI
# ============================================================

def main():

    print("Hello! Welcome to the Interactive DSP Visualization Tool.")
    parser = argparse.ArgumentParser(
        description="Interactive DSP visualization tool"
    )

    parser.add_argument(
        "visualization",
        help="Visualization to display"
    )

    args = parser.parse_args()

    if args.visualization == "complex-exponential":
        complex_exponential()

    else:
        parser.error(
            f"Unknown visualization: {args.visualization}"
        )


if __name__ == "__main__":
    main()