"""Evaluation of automata."""
from automata.automaton import FiniteAutomaton, State, Transitions
from collections import defaultdict, deque

class FiniteAutomatonEvaluator():
    """
    Definition of an automaton evaluator.

    Args:
        automaton: Automaton to evaluate.

    Attributes:
        current_states: Set of current states of the automaton.

    """

    # automaton: FiniteAutomaton
    # current_states: Set[State]

    def __init__(self, automaton):
        self.automaton = automaton
        
        current_states = {self.automaton.initial_state}
        #---------------------------------------------------------------------
        # TO DO: 
        # add usefull code if necessary
        #---------------------------------------------------------------------
        
        self.current_states = self._complete_lambdas(current_states)
        



    def process_symbol(self, symbol):
        """
        Process one symbol.
        Args:
            symbol: Symbol to consume. Type: str

        """
        if symbol not in self.automaton.symbols:
            raise ValueError("The symbol is not in the alphabet of the automaton")
        
        transitions = set()
        for i in self.current_states:
            transitions.update(self.automaton.get_transition(i, symbol))
        
        self.current_states = self._complete_lambdas(transitions)
        
    def _complete_lambdas(self, set_to_complete, visited=None):
        """
        Add states reachable with lambda transitions to the set.

        Args:
            set_to_complete: Current set of states to be completed.
            visited: Set of states that have already been checked for lambda transitions.
        """
        #import pdb;pdb.set_trace()
        """
        if visited is None:
            visited = set()

        next_states = set(set_to_complete)
        for state in set_to_complete:
            if state not in visited:
                visited.add(state)
                if self.automaton.has_transition(state, None):
                    aux = self.automaton.get_transition(state, None)
                    for i in aux:
                        if i not in next_states:
                            next_states.add(i)
                            next_states.update(self._complete_lambdas({i}, visited))
        return next_states
        """
        final_set = set()
        final_set.update(set_to_complete)

        for state in set_to_complete:
            new_states = self.automaton.get_transition(state, None)
            if new_states is None:
                final_set.add(state)
            else:
                final_set.update(self._complete_lambdas(set(new_states)))
        
        return final_set

        
    def process_string(self, string):
        """
        Process a full string of symbols.

        Args:
            string: String to process.

        """
        for symbol in string:
            self.process_symbol(symbol)


    def is_accepting(self):
        """Check if the current state is an accepting one."""
        
        for state in self.current_states: 
            if state.is_final: 
                return True 
        
        return False 
    
        
    def accepts(self, string):
        """
        Return if a string is accepted without changing state.

        Note: This function is NOT thread-safe.

        """
        old_transitions = self.current_states
        
        try:
            self.process_string(string)
            accepted = self.is_accepting()
        finally:
            self.current_states = old_transitions
        
        return accepted

