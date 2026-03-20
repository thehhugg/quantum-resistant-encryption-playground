#!/usr/bin/env python3
"""
Parameter Optimization — Predicting Encryption Time from Lattice Size
=====================================================================

This script demonstrates a simple linear regression model that predicts
how long a lattice-based encryption operation will take, given the lattice
dimension (size) as input.

Why this matters
----------------
Lattice-based post-quantum algorithms (ML-KEM, ML-DSA) have a key
parameter: the lattice dimension. Larger dimensions provide stronger
security but increase computation time. Understanding this trade-off
helps practitioners choose the right parameter set.

For example, ML-KEM defines three parameter sets:
- ML-KEM-512:  lattice dimension 256, NIST Level 1 (~AES-128 equivalent)
- ML-KEM-768:  lattice dimension 384, NIST Level 3 (~AES-192 equivalent)
- ML-KEM-1024: lattice dimension 512, NIST Level 5 (~AES-256 equivalent)

What this script does
---------------------
1. Defines sample data points mapping lattice sizes to encryption times.
2. Fits a linear regression model: time = slope * lattice_size + intercept.
3. Predicts the encryption time for an unseen lattice size.
4. Visualizes the data and the fitted regression line.

This is a toy model for illustration. In practice, the relationship
between lattice dimension and encryption time is closer to O(n^2) or
O(n^2 * log(n)) due to polynomial multiplication, not strictly linear.

Dependencies
------------
    pip install numpy scikit-learn matplotlib
"""

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend; remove this line for interactive use
import matplotlib.pyplot as plt

# ─── Training Data ───────────────────────────────────────────────────────────
# Each row is a lattice dimension; the corresponding entry in
# encryption_times is the measured encryption time in seconds.
#
# These are synthetic values for demonstration. Replace with real
# benchmark data from data/encryption_times.csv for actual analysis.
# See ai/lattice_optimizer.py for a version that loads real data.

lattice_sizes = np.array([[256], [512], [768], [1024]])
encryption_times = np.array([0.1, 0.25, 0.5, 0.75])

# ─── Model Training ─────────────────────────────────────────────────────────
# Linear regression finds the line y = mx + b that minimizes the sum of
# squared errors between predicted and actual encryption times.
#
# sklearn's LinearRegression uses the ordinary least squares (OLS) method.
# For our 4 data points, this produces a perfect or near-perfect fit
# because the synthetic data is approximately linear.

model = LinearRegression().fit(lattice_sizes, encryption_times)

# The learned parameters:
#   model.coef_[0]  = slope (seconds per unit increase in lattice size)
#   model.intercept_ = y-intercept (predicted time at lattice size 0)


def predict_encryption_time(lattice_size: int) -> float:
    """Predict the encryption time for a given lattice dimension.

    Args:
        lattice_size: The lattice dimension (e.g., 256, 512, 768, 1024).

    Returns:
        Predicted encryption time in seconds.
    """
    return model.predict([[lattice_size]])[0]


def visualize_data(save_path: str = None) -> None:
    """Plot lattice size vs. encryption time with the regression line.

    Args:
        save_path: If provided, save the chart to this file instead of
                   displaying it interactively.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot the actual data points
    ax.scatter(lattice_sizes, encryption_times, color="blue", s=80,
               zorder=3, label="Measured data")

    # Plot the regression line over a wider range to show extrapolation
    x_range = np.linspace(128, 1280, 100).reshape(-1, 1)
    ax.plot(x_range, model.predict(x_range), color="red", linewidth=2,
            label=f"Linear fit (slope={model.coef_[0]:.4f} s/dim)")

    ax.set_xlabel("Lattice Dimension")
    ax.set_ylabel("Encryption Time (seconds)")
    ax.set_title("Lattice Dimension vs. Encryption Time (Linear Regression)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Chart saved to: {save_path}")
    else:
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    # ── Example: predict for an unseen lattice size ──────────────────────
    lattice_size_to_predict = 640
    predicted_time = predict_encryption_time(lattice_size_to_predict)

    print(f"Model parameters:")
    print(f"  Slope:     {model.coef_[0]:.6f} seconds per lattice dimension unit")
    print(f"  Intercept: {model.intercept_:.6f} seconds")
    print()
    print(f"Predicted encryption time for lattice size {lattice_size_to_predict}: "
          f"{predicted_time:.4f} seconds")

    # ── Visualize ────────────────────────────────────────────────────────
    import os
    chart_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "parameter_optimization.png"
    )
    visualize_data(save_path=chart_path)
