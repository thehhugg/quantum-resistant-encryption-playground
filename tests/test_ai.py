"""Tests for ai/ analysis scripts."""

import pytest

from ai.lattice_optimizer import predict_encryption_time as predict_multi
from ai.parameter_optimization import predict_encryption_time as predict_single
from ai.utils.data_handler import load_data


class TestParameterOptimization:
    """Tests for the single-feature regression model."""

    def test_returns_float(self):
        result = predict_single(640)
        assert isinstance(result, float)

    def test_returns_finite(self):
        import math
        result = predict_single(512)
        assert math.isfinite(result)

    def test_different_inputs_give_different_outputs(self):
        t1 = predict_single(512)
        t2 = predict_single(1024)
        assert t1 != t2


class TestLatticeOptimizer:
    """Tests for the multi-feature regression model."""

    def test_returns_float(self):
        result = predict_multi(768, 0.003, 0.004)
        assert isinstance(result, float)

    def test_returns_finite(self):
        import math
        result = predict_multi(512, 0.002, 0.003)
        assert math.isfinite(result)

    def test_different_inputs_give_different_outputs(self):
        t1 = predict_multi(512, 0.002, 0.003)
        t2 = predict_multi(1024, 0.010, 0.012)
        assert t1 != t2


class TestDataHandler:
    """Tests for the CSV data loading utility."""

    def test_load_encryption_data(self):
        df = load_data("data/encryption_times.csv")
        assert len(df) > 0
        assert "lattice_size" in df.columns
        assert "encryption_time" in df.columns

    def test_has_expected_columns(self):
        df = load_data("data/encryption_times.csv")
        expected = {"lattice_size", "encryption_time", "keygen_time", "decryption_time"}
        assert expected.issubset(set(df.columns))

    def test_has_algorithm_column(self):
        df = load_data("data/encryption_times.csv")
        assert "algorithm" in df.columns
        assert len(df) >= 6  # At least 3 KEM + 3 DSA
