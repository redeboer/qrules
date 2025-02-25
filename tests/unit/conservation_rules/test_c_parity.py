from fractions import Fraction
from itertools import product

import pytest

from qrules.conservation_rules import (
    CParityEdgeInput,
    CParityNodeInput,
    c_parity_conservation,
)
from qrules.quantum_numbers import Parity


@pytest.mark.parametrize(
    ("rule_input", "expected"),
    [
        (
            (
                [CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(-1))],
                [
                    CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(-1)),
                    CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(1)),
                ],
                None,
            ),
            True,
        ),
        (
            (
                [CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(1))],
                [
                    CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(-1)),
                    CParityEdgeInput(spin_magnitude=0.0, pid=1, c_parity=Parity(1)),
                ],
                None,
            ),
            False,
        ),
    ],
)
def test_c_parity_all_defined(rule_input, expected):
    assert c_parity_conservation(*rule_input) is expected


@pytest.mark.parametrize(
    ("rule_input", "expected"),
    [
        (
            (
                [
                    CParityEdgeInput(
                        spin_magnitude=0, pid=123, c_parity=Parity(c_parity)
                    )
                ],
                [
                    CParityEdgeInput(spin_magnitude=0, pid=100),
                    CParityEdgeInput(spin_magnitude=0, pid=-100),
                ],
                CParityNodeInput(
                    l_magnitude=Fraction(l_magnitude), s_magnitude=Fraction(0)
                ),
            ),
            (-1) ** l_magnitude == c_parity,
        )
        for c_parity, l_magnitude in product([-1, 1], range(5))
    ],
)
def test_c_parity_multiparticle_boson(rule_input, expected):
    assert c_parity_conservation(*rule_input) is expected


@pytest.mark.parametrize(
    ("rule_input", "expected"),
    [
        (
            (
                [
                    CParityEdgeInput(
                        spin_magnitude=0, pid=123, c_parity=Parity(c_parity)
                    )
                ],
                [
                    CParityEdgeInput(spin_magnitude=0.5, pid=100),
                    CParityEdgeInput(spin_magnitude=0.5, pid=-100),
                ],
                CParityNodeInput(
                    l_magnitude=Fraction(l_magnitude), s_magnitude=Fraction(s_magnitude)
                ),
            ),
            (s_magnitude + l_magnitude) % 2 == abs(c_parity - 1) / 2,
        )
        for c_parity, s_magnitude, l_magnitude in product([-1, 1], range(5), range(5))
    ],
)
def test_c_parity_multiparticle_fermion(rule_input, expected):
    assert c_parity_conservation(*rule_input) is expected
