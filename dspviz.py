#!/usr/bin/env python3

import argparse
import sys
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSlider,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


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

    app = QApplication.instance() or QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("DSP Visualization Tool - Complex Exponential")
    window.resize(1280, 900)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)

    fig = Figure(figsize=(12, 9))
    canvas = FigureCanvas(fig)
    main_layout.addWidget(canvas, stretch=1)

    grid = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.38)
    ax = fig.add_subplot(grid[0, 0])
    ax_cos = fig.add_subplot(grid[1, 0])
    ax_sin = fig.add_subplot(grid[1, 1])
    ax_equation = fig.add_subplot(grid[0, 1])
    ax_equation.axis("off")
    fig.subplots_adjust(left=0.08, right=0.96, top=0.94, bottom=0.08)

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

    # Cosine and sine components over one cycle.
    phase_axis = np.linspace(0, 2 * np.pi, 500)
    cosine_line, = ax_cos.plot(phase_axis, np.cos(phase_axis), linewidth=2)
    sine_line, = ax_sin.plot(phase_axis, np.sin(phase_axis), linewidth=2)
    cosine_point, = ax_cos.plot([phi0], [np.cos(phi0)], "o", markersize=8)
    sine_point, = ax_sin.plot([phi0], [np.sin(phi0)], "o", markersize=8)

    for component_ax, title in (
        (ax_cos, "Cosine component: I / A = cos(theta)"),
        (ax_sin, "Sine component: Q / A = sin(theta)"),
    ):
        component_ax.set_xlim(0, 2 * np.pi)
        component_ax.set_ylim(-1.1, 1.1)
        component_ax.set_xticks(
            [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
            ["0", "pi/2", "pi", "3pi/2", "2pi"],
        )
        component_ax.set_ylabel("Value")
        component_ax.set_title(title)
        component_ax.grid(True, alpha=0.3)

    ax_cos.set_xlabel("Angle theta (radians)")
    ax_sin.set_xlabel("Angle theta (radians)")

    equation_text = ax_equation.text(
        0.02,
        0.95,
        "Euler's formula\n\n"
        r"$e^{j\theta} = \cos(\theta) + j\sin(\theta)$"
        "\n\n"
        r"$x(t) = A e^{j(2\pi f t + \phi)}$"
        "\n"
        r"$x(t) = A[\cos(\theta) + j\sin(\theta)]$"
        "\n\n"
        "The cosine value is the in-phase component (I).\n"
        "The sine value is the quadrature component (Q).\n"
        "With amplitude A: I = A cos(theta), Q = A sin(theta).",
        transform=ax_equation.transAxes,
        va="top",
        fontsize=13,
    )

    # Native Qt sliders keep the controls responsive when the window resizes.
    controls_layout = QFormLayout()
    controls_layout.setFieldGrowthPolicy(
        QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow  
    )
    main_layout.addLayout(controls_layout)

    def create_slider(label, minimum, maximum, value, scale):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimumWidth(700)
        slider.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        slider.setRange(minimum, maximum)
        slider.setValue(round(value * scale))
        value_label = QLabel()
        value_label.setMinimumWidth(70)
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        row = QHBoxLayout()
        row.addWidget(slider)
        row.addWidget(value_label)
        controls_layout.addRow(label, row)
        return slider, value_label, scale

    slider_A, value_A, scale_A = create_slider(
        "Amplitude", 0, 200, A0, 100
    )
    slider_f, value_f, scale_f = create_slider(
        "Frequency", 0, 500, f0, 100
    )
    slider_phi, value_phi, scale_phi = create_slider(
        "Phase", -314, 314, phi0, 100
    )
    slider_t, value_t, scale_t = create_slider(
        "Time", 0, 100, t0, 100
    )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(_=None):

        A = slider_A.value() / scale_A
        f = slider_f.value() / scale_f
        phi = slider_phi.value() / scale_phi
        t = slider_t.value() / scale_t

        angle = 2 * np.pi * f * t + phi
        z = A * np.exp(1j * angle)

        point.set_data(
            [z.real],
            [z.imag]
        )

        vector.set_data(
            [0, z.real],
            [0, z.imag]
        )

        phase = angle % (2 * np.pi)
        cosine_point.set_data([phase], [np.cos(angle)])
        sine_point.set_data([phase], [np.sin(angle)])
        equation_text.set_text(
            "Euler's formula\n\n"
            r"$e^{j\theta} = \cos(\theta) + j\sin(\theta)$"
            "\n\n"
            r"$x(t) = A e^{j(2\pi f t + \phi)}$"
            "\n"
            r"$x(t) = A[\cos(\theta) + j\sin(\theta)]$"
            "\n\n"
            f"Current angle: theta = {angle:.3f} rad\n"
            f"I = A cos(theta) = {z.real:.3f}\n"
            f"Q = A sin(theta) = {z.imag:.3f}\n\n"
            "The cosine value is I, the in-phase component.\n"
            "The sine value is Q, the quadrature component."
        )

        value_A.setText(f"{A:.2f}")
        value_f.setText(f"{f:.2f} Hz")
        value_phi.setText(f"{phi:.2f} rad")
        value_t.setText(f"{t:.2f} s")
        canvas.draw_idle()

    slider_A.valueChanged.connect(update)
    slider_f.valueChanged.connect(update)
    slider_phi.valueChanged.connect(update)
    slider_t.valueChanged.connect(update)

    update()
    window.show()
    app.exec()


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