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

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    
    def test_case2(self):
        """Test Case 2"""
        automaton_str = """
        Automaton:
        Symbols: -+.d
        
        q0
        q1
        q2
        q3
        q4
        q5 final
        
        ini q0 ---> q1
        ini q0 -+-> q1
        ini q0 --> q1
        q1 -d-> q1
        q1 -.-> q2
        q1 -d-> q4
        
        q2 -d->q3
        q4 -.->q3
        q3 -d->q3
        q3 -->q5
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
        empty 
        
        ini q0q1 -d-> q1q4
        ini q0q1 ---> q1
        ini q0q1 -+-> q1
        ini q0q1 -.->q2

        q1 -d-> q1q4 
        q1 -.-> q2
        q1 ---> empty
        q1 -+-> empty

        q2 -d-> q3q5
        q2 ---> empty
        q2 -+-> empty
        q2 -.-> empty

        q1q4 -d-> q1q4
        q1q4 -.-> q2q3q5
        q1q4 ---> empty
        q1q4 -+-> empty

        q2q3q5 -d-> q3q5
        q2q3q5 ---> empty
        q2q3q5 -+-> empty
        q2q3q5 -.-> empty

        q3q5 -d-> q3q5
        q3q5 ---> empty
        q3q5 -+-> empty
        q3q5 -.-> empty

        empty -+-> empty
        empty ---> empty
        empty -d-> empty
        empty -.-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self):
        """Test Case 3."""
        automaton_str = """
        Automaton:
        Symbols: ab
        
        q0
        q1
        q2
        q3
        q4 final
        
        ini q0 -a-> q0
        ini q0 -b-> q0
        ini q0 -b-> q1

        q1 -a-> q1
        q1 -b-> q0
        q1 -b-> q2
        
        q2 -a-> q3
        q2 -b-> q2

        q3 -a-> q3
        q3 -a-> q4
        q3 -b-> q3

        q4 -a-> q0
        q4 -b-> q0 
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: ab
        
        q0
        q0q1
        q0q1q2
        q0q1q3
        q0q1q2q3
        q0q1q3q4 final 
        empty 
        
        ini q0 -a-> q0
        ini q0 -b-> q0q1
        
        q0q1 -a-> q0q1
        q0q1 -b-> q0q1q2 

        q0q1q2 -b-> q0q1q2
        q0q1q2 -a-> q0q1q3

        q0q1q3 -b-> q0q1q2q3
        q0q1q3 -a-> q0q1q3q4

        q0q1q2q3 -b-> q0q1q2q3
        q0q1q2q3 -a-> q0q1q3q4

        q0q1q3q4 -a-> q0q1q3q4
        q0q1q3q4 -b-> q0q1q2q3 

        empty -a-> empty
        empty -b-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self):
        """Test Case 4."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1
        q2
        q3
        q4
        q5
        q6 final 
        q7
        
        ini q0 --> q2
        ini q0 --> q1

        q1 -1-> q5
        q1 -1-> q3

        q2 -0-> q4 

        q4 -1-> q6

        q5 --> q7
        q5 -0-> q4
        q5 -0-> q3 

        q7 --> q6 
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0q1q2
        q4
        q3q5q6q7 final
        q3q4
        q6 final 
        empty
        
        ini q0q1q2 -0-> q4
        ini q0q1q2 -1-> q3q5q6q7
        
        q4 -1-> q6
        q4 -0-> empty

        q3q5q6q7 -0-> q3q4
        q3q5q6q7 -1-> empty 

        q3q4 -1-> q6
        q3q4 -0-> empty

        q6 -0-> empty
        q6 -1-> empty

        empty -0-> empty
        empty -1-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    
    
if __name__ == '__main__':
    unittest.main()
