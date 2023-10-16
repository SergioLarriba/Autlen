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

        posibles_estados = set()
        estados_lambdas = set()
        for state in self.current_states:
            posibles_estados = self.automaton.get_transition(state,symbol)
            if posibles_estados is None:
                continue
            #for state2 in posibles_estados:
            #    estados_lambdas.update(self._complete_lambdas(state2))
        estados_lambdas.update(self._complete_lambdas(posibles_estados))
        #Comprobar no vacios y union
        #Actuañlizar self.current states y devolverlo

        if posibles_estados is not None:
            posibles_estados.update(estados_lambdas)


        posibles_estados.update(estados_lambdas)
        self.current_states = posibles_estados

        
        return self.current_states
        
        
        
    def _complete_lambdas(self, set_to_complete):
        """
        Add states reachable with lambda transitions to the set.
        
        Args:
            set_to_complete: Current set of states to be completed.

        Returns:
            set: The set of states including those reachable with lambda transitions.
        """
        # Inicializamos una cola con los estados
        listaestados = set()
        listaestados.update(set_to_complete)

        for estado in set_to_complete:
            estadosNuevos = self.automaton.get_transition(estado,None)
            if estadosNuevos is None:
                listaestados.add(estado)
            else:
                listaestados.update(self._complete_lambdas(set(estadosNuevos)))

    
        return listaestados

        
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

