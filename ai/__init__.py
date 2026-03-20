"""AI/ML analysis utilities for lattice-based encryption schemes.

This package provides tools for analyzing and predicting the performance
of lattice-based post-quantum encryption algorithms using regression models.
"""

from ai.parameter_optimization import (
    predict_encryption_time as predict_time_from_lattice_size,
    visualize_data,
)
from ai.lattice_optimizer import (
    predict_encryption_time as predict_time_from_features,
    visualize_model,
)

__all__ = [
    "predict_time_from_lattice_size",
    "predict_time_from_features",
    "visualize_data",
    "visualize_model",
]
