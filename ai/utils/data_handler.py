#!/usr/bin/env python3
"""
Data Handler — CSV I/O Utilities for Benchmark Data
====================================================

Simple helper functions for loading and saving encryption benchmark
data in CSV format. Used by the AI analysis scripts in ``ai/``.

The expected CSV schema is::

    lattice_size,encryption_time,keygen_time,decryption_time
    256,0.08,0.02,0.07
    512,0.20,0.04,0.18
    ...

Each row represents one benchmark measurement at a given lattice
parameter set. Times are in seconds.
"""

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Load encryption performance data from a CSV file.

    Args:
        filepath: Path to the CSV file (e.g., ``data/encryption_times.csv``).

    Returns:
        A pandas DataFrame with columns like ``lattice_size``,
        ``encryption_time``, ``keygen_time``, ``decryption_time``.
    """
    return pd.read_csv(filepath)


def save_data(data: pd.DataFrame, filepath: str) -> None:
    """Save a DataFrame to a CSV file.

    Args:
        data:     The DataFrame to write.
        filepath: Destination file path. Will be created or overwritten.
    """
    data.to_csv(filepath, index=False)
