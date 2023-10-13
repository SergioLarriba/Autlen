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
        #self.current_states = self.automaton.transitions.get_transition(self.current_states, symbol)
        #self.current_states = self._complete_lambdas(self.current_states)
        # Control de errores 
        if symbol not in self.automaton.symbols:
            raise ValueError("The symbol is not in the alphabet of the automaton")
        
        estados_nuevos = set()
        for state in self.current_states:
            estados_nuevos.update(self.automaton.get_transition(state,symbol))

        self._complete_lambdas(estados_nuevos)
        self.current_states = estados_nuevos
        
        return 
        
        

        
    def _complete_lambdas(self, set_to_complete):
        """
        Add states reachable with lambda transitions to the set.

        {State('Empty', is_final=False)}
        {State('1', is_final=False)}

        Args:
            set_to_complete: Current set of states to be completed.
        """
         

        
        
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

