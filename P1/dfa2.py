from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic, write_dot
from collections import deque

class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic_v2(finiteAutomaton):
        """Returns an equivalent deterministic finite automaton."""
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        # Dictionary to store transition table
        dfa_states = dict()

        # List of states for the new automaton
        states = []

        # Queue to keep track of states to process
        states_to_check = queue.Queue()
        states.append(finiteAutomaton.initial_state)
        states_to_check.put(finiteAutomaton.initial_state)

        # While there are states in the queue
        while not states_to_check.empty():
            # Get the current state
            to_check = states_to_check.get()

            for symbol in finiteAutomaton.symbols:
                # Obtain the states we can reach with symbol from to_check
                evaluator.process_symbol(symbol)
                current_states = evaluator.current_states
                if not current_states:
                    current_states = set()

                # Keys will be strings of the set of states
                current_states_key = "q" + '_'.join(sorted([str(s.name) for s in current_states]))
                new_states = State(current_states_key, False)

                # Add it to the dictionary {state, symbol} -> next_state
                dfa_states[(to_check, symbol)] = new_states

                # If the key is not in the dictionary -> The state has not been seen
                if new_states not in states:
                    states_to_check.put(new_states)
                    states.append(new_states)

        # When there are no more states to see, add the transitions
        transitions = Transitions()
        for (current_state, symbol), dest_state in dfa_states.items():
            transitions.add_transition(current_state, symbol, dest_state)

        # Assign final states
        final_states_afn = [state for state in finiteAutomaton.states if state.is_final]
        for state in final_states_afn:
            for state2 in states:
                if state.name in state2.name:
                    state2.is_final = True

        # Add empty state and connect missing transitions to it
        empty_state = State("empty", False)
        for symbol in finiteAutomaton.symbols:
            transitions.add_transition(empty_state, symbol, empty_state)
        for state in states:
            for symbol in finiteAutomaton.symbols:
                if not transitions.get_transition(state, symbol):
                    transitions.add_transition(state, symbol, empty_state)

        dfa = FiniteAutomaton(finiteAutomaton.initial_state, states, finiteAutomaton.symbols, transitions)
        return dfa



    @staticmethod
    def to_minimized(dfa):
        """
        Return a equivalent minimal automaton.
        Returns:
            Equivalent minimal automaton.
        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        
        #---------------------------------------------------------------------
        raise NotImplementedError("This method must be implemented.")


    def to_deterministic(finiteAutomaton):
        """Returns an equivalent deterministic finite automaton."""
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        # Diccionario para guardar la tabla de transiciones 
        dfa_states = dict()

        # Lista de estados para el nuevo automata 
        states = []
        import pdb; pdb.set_trace()

        # Cola para tratar los estados para procesr 
        states_to_check = queue.Queue()
        #initial_state = State("q_initial", False)  
        states.append(evaluator.current_states)
        states_to_check.put(evaluator.current_states)

        # Mientras queden estados en la cola
        while not states_to_check.empty():
            # Obtengo el estado actual 
            to_check = states_to_check.get()

            for symbol in finiteAutomaton.symbols:
                # Obtenemos los estados a los que podemos llegar con symbol desde to_check
                current_states = evaluator.process_symbol(symbol)
                if current_states is None:
                    current_states = set()

                # Las llaves seran strings del conjunto de estados 
                current_states_key = "q" + '_'.join(sorted([str(s) for s in current_states]))
                new_states = State(current_states_key, False)

                # Lo añado al diccionario {estado, simbolo} -> estado_siguiente 
                dfa_states[(current_states_key, symbol)] = new_states

                # Si la clave no esta en el diccionario -> El estado no lo hemos visto 
                if new_states not in states:
                    states_to_check.put(new_states)
                    states.append(new_states)

        # Cuando no queden más estados por ver, añadimos las transiciones 
        transitions = Transitions()
        for (current_state, symbol), dest_state in dfa_states.items():
            transitions.add_transition(current_state, symbol, dest_state)

        # Asignamos estados finales 
        final_states_afn = [state for state in finiteAutomaton.states if state.is_final] # Estados finales del automata no determinista 
        for state in final_states_afn:
            for state2 in states:
                if state in state2:
                    state2.is_final = True

        # Añadir estado vacío y conectar las transiciones que faltan a él
        empty_state = State("empty", False)
        for symbol in finiteAutomaton.symbols:
            transitions.add_transition(empty_state, symbol, empty_state)
        for (state, symbol), next_state in dfa_states.items():
            if next_state is None:
                transitions.add_transition(state, symbol, empty_state)

        dfa = FiniteAutomaton(finiteAutomaton.initial_state, states, finiteAutomaton.symbols, transitions)
        return dfa