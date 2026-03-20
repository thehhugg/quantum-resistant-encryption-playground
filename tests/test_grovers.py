"""Tests for quantum/grovers_simulation.py."""

import numpy as np
import pytest

from quantum.grovers_simulation import (
    diffusion,
    hadamard_n,
    optimal_iterations,
    oracle,
    run_grovers,
)


class TestHadamardN:
    """Tests for the n-qubit Hadamard gate."""

    def test_single_qubit(self):
        H = hadamard_n(1)
        expected = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        np.testing.assert_allclose(H, expected, atol=1e-10)

    def test_is_unitary(self):
        for n in range(1, 5):
            H = hadamard_n(n)
            N = 2 ** n
            identity = np.eye(N)
            np.testing.assert_allclose(H @ H.conj().T, identity, atol=1e-10)

    def test_shape(self):
        for n in range(1, 5):
            H = hadamard_n(n)
            assert H.shape == (2 ** n, 2 ** n)


class TestOracle:
    """Tests for the oracle matrix."""

    def test_diagonal(self):
        for n in range(1, 4):
            for target in range(2 ** n):
                O = oracle(n, target)
                assert O[target, target] == -1
                for i in range(2 ** n):
                    if i != target:
                        assert O[i, i] == 1

    def test_is_unitary(self):
        O = oracle(3, 5)
        identity = np.eye(8)
        np.testing.assert_allclose(O @ O.conj().T, identity, atol=1e-10)


class TestDiffusion:
    """Tests for the Grover diffusion operator."""

    def test_is_unitary(self):
        for n in range(1, 5):
            D = diffusion(n)
            N = 2 ** n
            identity = np.eye(N)
            np.testing.assert_allclose(D @ D.conj().T, identity, atol=1e-10)

    def test_shape(self):
        D = diffusion(3)
        assert D.shape == (8, 8)


class TestOptimalIterations:
    """Tests for the optimal iteration count."""

    def test_known_values(self):
        # 2 qubits: N=4, pi/4 * sqrt(4) = pi/2 ~ 1.57 -> 1
        assert optimal_iterations(2) == 1
        # 3 qubits: N=8, pi/4 * sqrt(8) ~ 2.22 -> 2
        assert optimal_iterations(3) == 2
        # 4 qubits: N=16, pi/4 * sqrt(16) ~ 3.14 -> 3
        assert optimal_iterations(4) == 3

    def test_minimum_one(self):
        assert optimal_iterations(1) >= 1


class TestRunGrovers:
    """Integration tests for the full Grover's algorithm."""

    def test_finds_target_3_qubits(self):
        for target in range(8):
            state = run_grovers(3, target, verbose=False)
            probs = np.abs(state) ** 2
            assert probs[target] > 0.9, f"Target {target} prob = {probs[target]}"

    def test_finds_target_4_qubits(self):
        state = run_grovers(4, 7, verbose=False)
        probs = np.abs(state) ** 2
        assert probs[7] > 0.9

    def test_state_vector_normalized(self):
        state = run_grovers(3, 5, verbose=False)
        total_prob = np.sum(np.abs(state) ** 2)
        np.testing.assert_allclose(total_prob, 1.0, atol=1e-10)

    def test_invalid_target_raises(self):
        with pytest.raises(ValueError):
            run_grovers(3, 8, verbose=False)
        with pytest.raises(ValueError):
            run_grovers(3, -1, verbose=False)
