#!/usr/bin/env python3
"""
Lattice Optimizer — Multi-Feature Performance Analysis
=======================================================

This script extends the single-feature model in ``parameter_optimization.py``
by using multiple features to predict PQC operation times:

1. **Lattice size** — the dominant cost driver.
2. **Key generation time** — a proxy for hardware speed.
3. **Decryption/verification time** — correlated with encryption.

It also compares ML-KEM and ML-DSA families, showing how different
algorithm types have different performance profiles even at the same
lattice dimension.

What this teaches
-----------------
- Multi-feature regression can capture more nuance than a single feature.
- ML-KEM operations (encapsulation) are much faster than ML-DSA operations
  (signing) at the same lattice size, because the underlying operations
  differ (NTT-based polynomial multiplication vs. rejection sampling).
- With only 6 data points, the model is illustrative. In practice, you
  would benchmark across many hardware configurations and parameter sets.

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

# ─── Feature Engineering ────────────────────────────────────────────────────
# Use three features: lattice_size, keygen_time, decryption_time
features = data[["lattice_size", "keygen_time", "decryption_time"]].values
encryption_times = data["encryption_time"].values

# ─── Model Training ─────────────────────────────────────────────────────────
model = LinearRegression().fit(features, encryption_times)


def predict_encryption_time(
    lattice_size: int, keygen_time: float, decryption_time: float
) -> float:
    """Predict encryption/encapsulation time from multiple features.

    Args:
        lattice_size:    Lattice dimension (e.g., 512, 768, 1024).
        keygen_time:     Measured key generation time in seconds.
        decryption_time: Measured decryption/verification time in seconds.

    Returns:
        Predicted encryption time in seconds.
    """
    return float(model.predict([[lattice_size, keygen_time, decryption_time]])[0])


def visualize_model(save_path: str = None) -> None:
    """Plot actual vs. predicted times, color-coded by algorithm family.

    Args:
        save_path: If provided, save the chart to this file path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    predictions = model.predict(features)

    # Left panel: Actual vs. Predicted
    ax = axes[0]
    colors = ["steelblue" if "KEM" in alg else "coral" for alg in data["algorithm"]]
    ax.scatter(encryption_times, predictions, c=colors, s=100, zorder=3)
    lims = [0, max(max(encryption_times), max(predictions)) * 1.1]
    ax.plot(lims, lims, "k--", alpha=0.3, label="Perfect prediction")
    for i, row in data.iterrows():
        ax.annotate(row["algorithm"], (encryption_times[i], predictions[i]),
                    textcoords="offset points", xytext=(8, 5), fontsize=8)
    ax.set_xlabel("Actual Time (s)")
    ax.set_ylabel("Predicted Time (s)")
    ax.set_title("Actual vs. Predicted (Multi-Feature)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Right panel: All operation times by algorithm
    ax = axes[1]
    x_pos = np.arange(len(data))
    width = 0.25
    ax.bar(x_pos - width, data["keygen_time"], width, label="KeyGen", color="steelblue")
    ax.bar(x_pos, data["encryption_time"], width, label="Encrypt/Sign", color="coral")
    ax.bar(x_pos + width, data["decryption_time"], width, label="Decrypt/Verify", color="seagreen")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(data["algorithm"], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Operation Times by Algorithm")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")

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
    print("Multi-Feature Linear Regression:")
    print("  encryption_time ~ lattice_size + keygen_time + decryption_time")
    print()
    print("  Coefficients:")
    for name, coef in zip(feature_names, model.coef_):
        print(f"    {name:>20s}: {coef:+.6f}")
    print(f"    {'intercept':>20s}: {model.intercept_:+.6f}")
    print(f"  R-squared: {model.score(features, encryption_times):.4f}")
    print()

    # ── Show data ────────────────────────────────────────────────────────
    print("Benchmark data:")
    print(data[["algorithm", "lattice_size", "keygen_time",
                "encryption_time", "decryption_time"]].to_string(index=False))
    print()

    # ── Visualize ────────────────────────────────────────────────────────
    chart_path = os.path.join(_SCRIPT_DIR, "..", "lattice_optimizer.png")
    visualize_model(save_path=chart_path)
