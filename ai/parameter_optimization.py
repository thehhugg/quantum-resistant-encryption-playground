#!/usr/bin/env python3
"""
Parameter Optimization — Predicting PQC Operation Time from Lattice Size
=========================================================================

This script demonstrates a simple machine learning approach to predicting
post-quantum cryptography operation times based on lattice parameters.

It loads real benchmark data from ``data/encryption_times.csv`` (generated
by ``scripts/generate_benchmarks.py``) and trains a linear regression
model to predict encryption/encapsulation time from lattice size.

What this teaches
-----------------
1. **Lattice size drives computational cost.** Larger lattice dimensions
   mean more polynomial multiplications, which take longer.

2. **The relationship is roughly linear** for the parameter sets used in
   ML-KEM and ML-DSA, though the actual complexity is O(n log n) due to
   NTT-based polynomial multiplication.

3. **ML can model performance trade-offs** even with small datasets,
   though with only 6 data points, the model is illustrative, not
   production-grade.

Dependencies
------------
    pip install numpy scikit-learn matplotlib pandas
"""

import os

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend; remove for interactive use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ─── Data Loading ────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_SCRIPT_DIR, "..", "data", "encryption_times.csv")

data = pd.read_csv(_DATA_PATH)

# ─── Feature and Target ─────────────────────────────────────────────────────
# We predict encryption_time (encapsulation for KEM, signing for DSA)
# from lattice_size alone. This is the simplest useful model.

X = data[["lattice_size"]].values
y = data["encryption_time"].values

# ─── Model Training ─────────────────────────────────────────────────────────
model = LinearRegression().fit(X, y)


def predict_encryption_time(lattice_size: int) -> float:
    """Predict encryption/encapsulation time for a given lattice size.

    Args:
        lattice_size: Lattice dimension (e.g., 512, 768, 1024).

    Returns:
        Predicted time in seconds.
    """
    return float(model.predict([[lattice_size]])[0])


def visualize_model(save_path: str = None) -> None:
    """Plot actual vs. predicted operation times by lattice size.

    Args:
        save_path: If provided, save the chart to this file path.
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    # Color-code by algorithm family
    colors = {"ML-KEM": "steelblue", "ML-DSA": "coral"}
    for _, row in data.iterrows():
        family = "ML-KEM" if "KEM" in row["algorithm"] else "ML-DSA"
        ax.scatter(
            row["lattice_size"], row["encryption_time"],
            color=colors[family], s=100, zorder=3,
            label=family if family not in ax.get_legend_handles_labels()[1] else "",
        )
        ax.annotate(
            row["algorithm"], (row["lattice_size"], row["encryption_time"]),
            textcoords="offset points", xytext=(8, 5), fontsize=8,
        )

    # Regression line
    x_range = np.linspace(400, 1100, 100).reshape(-1, 1)
    ax.plot(x_range, model.predict(x_range), "k--", alpha=0.5,
            label=f"Linear fit (R²={model.score(X, y):.3f})")

    ax.set_xlabel("Lattice Dimension")
    ax.set_ylabel("Operation Time (seconds)")
    ax.set_title("PQC Operation Time vs. Lattice Size")
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
    # ── Print model info ─────────────────────────────────────────────────
    print("Linear Regression: encryption_time ~ lattice_size")
    print(f"  Slope:     {model.coef_[0]:.6f} seconds per lattice dimension unit")
    print(f"  Intercept: {model.intercept_:.6f} seconds")
    print(f"  R-squared: {model.score(X, y):.4f}")
    print()

    # ── Show data ────────────────────────────────────────────────────────
    print("Benchmark data:")
    print(data[["algorithm", "lattice_size", "keygen_time",
                "encryption_time", "decryption_time"]].to_string(index=False))
    print()

    # ── Example predictions ──────────────────────────────────────────────
    for size in [512, 640, 768, 1024]:
        t = predict_encryption_time(size)
        print(f"  Predicted time for lattice_size={size}: {t:.6f} s")

    # ── Visualize ────────────────────────────────────────────────────────
    chart_path = os.path.join(_SCRIPT_DIR, "..", "parameter_optimization.png")
    visualize_model(save_path=chart_path)
