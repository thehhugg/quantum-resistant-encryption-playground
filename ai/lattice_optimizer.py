#!/usr/bin/env python3
"""
Lattice Optimizer — Multi-Feature Encryption Time Prediction
=============================================================

This script loads real benchmark data from ``data/encryption_times.csv``
and trains a multi-feature linear regression model to predict encryption
time from three inputs:

1. **Lattice size** — the dimension of the lattice (e.g., 256, 512, 1024).
   Larger lattices provide stronger security but cost more computation.

2. **Key generation time** — how long it took to generate the keypair.
   This is correlated with lattice size and implementation efficiency.

3. **Decryption time** — how long decryption took for the same parameters.
   Encryption and decryption times are correlated because they involve
   similar polynomial operations.

Why multi-feature regression?
-----------------------------
A single-feature model (lattice size alone) captures the dominant trend,
but key generation and decryption times carry additional information
about the specific hardware and implementation. Including them can
improve prediction accuracy.

See ``ai/parameter_optimization.py`` for the simpler single-feature version.

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
# Build the path to the CSV relative to this script's location,
# so it works regardless of the caller's working directory.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_SCRIPT_DIR, "..", "data", "encryption_times.csv")

# The CSV has columns: lattice_size, encryption_time, keygen_time, decryption_time
# Each row represents one benchmark measurement at a given parameter set.
data = pd.read_csv(_DATA_PATH)

# ─── Feature Engineering ────────────────────────────────────────────────────
# We use three features to predict encryption_time:
#   - lattice_size:    primary driver of computational cost
#   - keygen_time:     proxy for hardware speed and implementation
#   - decryption_time: correlated with encryption (similar operations)
#
# In a real study, you might also include: polynomial ring degree,
# modulus q, number of NTT operations, or CPU frequency.

features = data[["lattice_size", "keygen_time", "decryption_time"]].values
encryption_times = data["encryption_time"].values

# ─── Model Training ─────────────────────────────────────────────────────────
# Ordinary least squares linear regression:
#   encryption_time = w1*lattice_size + w2*keygen_time + w3*decryption_time + b
#
# With only a few data points, this model will overfit. The purpose here
# is to demonstrate the approach, not to build a production model.

model = LinearRegression().fit(features, encryption_times)


def predict_encryption_time(
    lattice_size: int, keygen_time: float, decryption_time: float
) -> float:
    """Predict encryption time from lattice parameters.

    Args:
        lattice_size:    Lattice dimension (e.g., 256, 512, 768, 1024).
        keygen_time:     Measured key generation time in seconds.
        decryption_time: Measured decryption time in seconds.

    Returns:
        Predicted encryption time in seconds.
    """
    return model.predict([[lattice_size, keygen_time, decryption_time]])[0]


def visualize_model(save_path: str = None) -> None:
    """Plot actual vs. predicted encryption times.

    The x-axis shows lattice size (the dominant feature). Blue dots are
    actual measurements; the red line shows the model's predictions for
    the same input rows.

    Args:
        save_path: If provided, save the chart to this file path.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        data["lattice_size"], encryption_times,
        color="blue", s=80, zorder=3, label="Actual measurements"
    )
    ax.plot(
        data["lattice_size"], model.predict(features),
        color="red", linewidth=2, marker="x", markersize=10,
        label="Model predictions"
    )

    ax.set_xlabel("Lattice Dimension")
    ax.set_ylabel("Encryption Time (seconds)")
    ax.set_title("Multi-Feature Regression: Lattice Size vs. Encryption Time")
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
    # ── Print model coefficients ─────────────────────────────────────────
    feature_names = ["lattice_size", "keygen_time", "decryption_time"]
    print("Model coefficients:")
    for name, coef in zip(feature_names, model.coef_):
        print(f"  {name:>20s}: {coef:+.6f}")
    print(f"  {'intercept':>20s}: {model.intercept_:+.6f}")
    print(f"  R-squared (training): {model.score(features, encryption_times):.4f}")
    print()

    # ── Example prediction ───────────────────────────────────────────────
    lattice_size = 768
    keygen_time = 0.03
    decryption_time = 0.20

    predicted_time = predict_encryption_time(lattice_size, keygen_time, decryption_time)
    print(
        f"Predicted encryption time for lattice_size={lattice_size}, "
        f"keygen_time={keygen_time}, decryption_time={decryption_time}:"
    )
    print(f"  {predicted_time:.4f} seconds")

    # ── Visualize ────────────────────────────────────────────────────────
    chart_path = os.path.join(_SCRIPT_DIR, "..", "lattice_optimizer.png")
    visualize_model(save_path=chart_path)
