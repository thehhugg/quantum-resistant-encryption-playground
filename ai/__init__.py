"""AI/ML analysis utilities for lattice-based encryption schemes.

This package provides tools for analyzing and predicting the performance
of lattice-based post-quantum encryption algorithms using regression models.
"""

from ai.parameter_optimization import (
    predict_encryption_time as predict_time_from_lattice_size,
    visualize_model as visualize_single_feature,
)
from ai.lattice_optimizer import (
    predict_encryption_time as predict_time_from_features,
    visualize_model as visualize_multi_feature,
)

__all__ = [
    "predict_time_from_lattice_size",
    "predict_time_from_features",
    "visualize_single_feature",
    "visualize_multi_feature",
]
