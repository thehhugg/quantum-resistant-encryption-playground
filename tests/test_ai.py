"""Tests for ai/ analysis scripts."""

import pytest

from ai.lattice_optimizer import predict_encryption_time as predict_multi
from ai.parameter_optimization import predict_encryption_time as predict_single
from ai.utils.data_handler import load_data


class TestParameterOptimization:
    """Tests for the single-feature regression model."""

    def test_prediction_is_positive(self):
        result = predict_single(512)
        assert result > 0

    def test_larger_lattice_takes_longer(self):
        t_small = predict_single(256)
        t_large = predict_single(1024)
        assert t_large > t_small

    def test_returns_float(self):
        result = predict_single(640)
        assert isinstance(result, float)


class TestLatticeOptimizer:
    """Tests for the multi-feature regression model."""

    def test_prediction_is_positive(self):
        result = predict_multi(512, 0.03, 0.18)
        assert result > 0

    def test_returns_float(self):
        result = predict_multi(768, 0.03, 0.20)
        assert isinstance(result, float)


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
