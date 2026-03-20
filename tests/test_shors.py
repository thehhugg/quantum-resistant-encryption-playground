"""Tests for quantum/shors_simulation.py."""

import pytest

from quantum.shors_simulation import (
    classical_order_finding,
    is_prime,
    is_prime_power,
    shors_algorithm,
)


class TestIsPrime:
    """Tests for the primality checker."""

    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            assert is_prime(p), f"{p} should be prime"

    def test_small_composites(self):
        for n in [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21]:
            assert not is_prime(n), f"{n} should not be prime"

    def test_edge_cases(self):
        assert not is_prime(0)
        assert not is_prime(1)
        assert is_prime(2)


class TestIsPrimePower:
    """Tests for the prime power checker."""

    def test_prime_powers(self):
        assert is_prime_power(4)    # 2^2
        assert is_prime_power(8)    # 2^3
        assert is_prime_power(9)    # 3^2
        assert is_prime_power(27)   # 3^3
        assert is_prime_power(25)   # 5^2

    def test_not_prime_powers(self):
        assert not is_prime_power(6)
        assert not is_prime_power(10)
        assert not is_prime_power(15)
        assert not is_prime_power(21)


class TestClassicalOrderFinding:
    """Tests for the classical order-finding function."""

    def test_known_orders(self):
        # Order of 2 mod 7 is 3 (2^3 = 8 = 1 mod 7)
        assert classical_order_finding(2, 7) == 3
        # Order of 3 mod 7 is 6
        assert classical_order_finding(3, 7) == 6
        # Order of 2 mod 15 is 4
        assert classical_order_finding(2, 15) == 4

    def test_order_divides_euler_totient(self):
        # The order must divide phi(N)
        assert classical_order_finding(7, 15) in [1, 2, 4]


class TestShorsAlgorithm:
    """Integration tests for Shor's factoring algorithm."""

    def test_factor_15(self):
        result = shors_algorithm(15, verbose=False)
        assert result is not None
        p, q = result
        assert p * q == 15
        assert 1 < p < 15
        assert 1 < q < 15

    def test_factor_21(self):
        result = shors_algorithm(21, verbose=False)
        assert result is not None
        p, q = result
        assert p * q == 21

    def test_factor_35(self):
        result = shors_algorithm(35, verbose=False)
        assert result is not None
        p, q = result
        assert p * q == 35

    def test_factor_91(self):
        result = shors_algorithm(91, verbose=False)
        assert result is not None
        p, q = result
        assert p * q == 91

    def test_even_number(self):
        result = shors_algorithm(22, verbose=False)
        assert result is not None
        p, q = result
        assert p * q == 22

    def test_prime_returns_none(self):
        result = shors_algorithm(17, verbose=False)
        assert result is None
