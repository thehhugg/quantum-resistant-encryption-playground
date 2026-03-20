"""Tests for the PQC example scripts in examples/."""

import subprocess
import sys

import pytest


class TestMLKEMExample:
    """Tests that the ML-KEM example runs without errors."""

    def test_runs_successfully(self):
        result = subprocess.run(
            [sys.executable, "examples/01_ml_kem_keygen.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Script failed:\n{result.stderr}"
        assert "ML-KEM" in result.stdout or "Kyber" in result.stdout

    def test_outputs_shared_secret(self):
        result = subprocess.run(
            [sys.executable, "examples/01_ml_kem_keygen.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        # The script should confirm that shared secrets match
        output_lower = result.stdout.lower()
        assert "match" in output_lower or "shared secret" in output_lower


class TestMLDSAExample:
    """Tests that the ML-DSA example runs without errors."""

    def test_runs_successfully(self):
        result = subprocess.run(
            [sys.executable, "examples/02_ml_dsa_signatures.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Script failed:\n{result.stderr}"
        assert "ML-DSA" in result.stdout or "Dilithium" in result.stdout

    def test_verifies_signatures(self):
        result = subprocess.run(
            [sys.executable, "examples/02_ml_dsa_signatures.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output_lower = result.stdout.lower()
        assert "valid" in output_lower or "verified" in output_lower or "verif" in output_lower
