"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case2(self):
        """Test Case 2"""
        automaton_str = """
        Automaton:
        Symbols: -+λ.d
        
        q0
        q1
        q2
        q3
        q4
        q5 final
        
        ini q0 ---> q1
        ini q0 -+-> q1
        ini q0 -λ-> q1
        q1 -d-> q1
        q1 -.-> q2
        q1 -d-> q4
        
        q2 -d->q3
        q4 -.->q3
        q3 -d->q3
        q3 -λ->q5
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: +-d.
        
        q0q1
        q1
        q1q4
        q2
        q2q3q5 final 
        q3q5 final
        
        ini q0q1 -d-> q1q4
        ini q0q1 ---> q1
        ini q0q1 -+-> q1
        ini q0q1 -.->q2
        q1 -d-> q1q4 
        q1 -.-> q1q4
        q2 -d-> q3q5
        q1q4 -d-> q1q4
        q1q4 -.-> q2q3q5
        q2q3q5 -d-> q3q5
        q3q5 -d-> q3q5
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

if __name__ == '__main__':
    unittest.main()
