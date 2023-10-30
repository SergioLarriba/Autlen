from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic, write_dot
import queue

class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic(finiteAutomaton):
        """Returns an equivalent deterministic finite automaton."""
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        # Diccionario para guardar la tabla de transiciones 
        dfa_states = dict() 

        # Lista de estados para el nuevo automata 
        states = list()
        #import pdb; pdb.set_trace()

        # Set de estados procesados
        processed_states = set()

        # Cola para tratar los estados para procesr 
        states_to_check = queue.Queue()
        initial_state = State(str(evaluator.current_states), False)  
        states.append(initial_state)
        states_to_check.put(evaluator.current_states)

        final_states_afn = set()
        # Estados finales del automata
        for state in finiteAutomaton.states:
            if state.is_final: 
                final_states_afn.add(state) 

        # Mientras queden estados en la cola
        while not states_to_check.empty():
            # Obtengo el conjunto de estados actual 
            to_check = states_to_check.get()

            for symbol in finiteAutomaton.symbols:
                # Si el estado actual tiene transicion con el simbolo lo añado al diccionario
                if finiteAutomaton.has_transition(frozenset(evaluator.current_states), symbol) == False:
                    continue 

                # Llave del diccionario (estado_actual, simbolo)
                dict_key = (''.join(state.name for state in evaluator.current_states), symbol) 
                dfa_states[dict_key] = None 

                # Obtenemos los estados a los que podemos llegar con symbol y actualizamos evaluator.current_states 
                evaluator.process_symbol(symbol)

                # Creo un nuevo estado, teniendo en cuenta los estados finales -> estado conjunto de los estados del evaluator 
                new_states = State(''.join(state.name for state in evaluator.current_states), bool(final_states_afn & evaluator.current_states))

                # Lo añado al diccionario {estado, simbolo} -> estado_siguiente 
                dfa_states[dict_key] = new_states

                # Añado estos estados a la cola 
                if str(new_states) not in processed_states:
                    states_to_check.put(new_states)
                    processed_states.add(str(new_states))


        # Cuando no queden más estados por ver, añadimos las transiciones 
        transitions = Transitions()
        for (current_state, symbol), dest_state in dfa_states.items():
            transitions.add_transition(current_state, symbol, dest_state)
            states.append(dest_state) 
        
        """
        # Añadir estado vacío y conectar las transiciones que faltan a él
        empty_state = State("empty", False)
        for symbol in finiteAutomaton.symbols:
            transitions.add_transition(empty_state, symbol, empty_state)
        for state in states:
            for symbol in finiteAutomaton.symbols:
                if not transitions.get_transition(state, symbol):
                    transitions.add_transition(state, symbol, empty_state)
        """
        print(f"Estados del automata {states}")
        
        dfa = FiniteAutomaton(initial_state, states, finiteAutomaton.symbols, transitions)
        print(f"Automata creado: {write_dot(dfa)}")
        return dfa



    @staticmethod
    def to_minimized(dfa):
        """
        Return a equivalent minimal automaton.
        Returns:
            Equivalent minimal automaton.
        """

        """
        Explicacion del algoritmo:
        1 - Comprobar que el automata sea determinista -> que sea de la clase DeterministicFiniteAutomaton
        2 - Eliminar estados inaccesibles 
            - Hacemos una busqueda en anchura (coger una pila, meto los nodos en la pila, los voy sacando, los marco como visitados en una lista de visitiados, mirar si la lista de visitados es igual a la de estados, y si no lo es, eliminamos los estados que no esten) desde el estado inicial, para ver a cuales llego
              a los que no llegue, son estados inaccesibles, asi que lo eliminamos
        3 - Comienza la minimizacion 
            3.1 - Se basa en clases de equivalencia, tenemos una lista con clases de equivalencia en cada iteracion -> vamos a empezar con una tabla
                  de la siguiente forma: ponemos 1 si es estado final y 0 si no. 
            3.2 - Cogemos el primer estado, le ponemos un 0, comparamos el A con el resto de estados
                        - Equivalente a la iteracion anterior (i-1)
                        - Transite a equivalente
                        Ej: B, no tiene clase de equiv -> podemos revisarla
                            como la A y B tienen un 0 en la iteracion anterior -> son equivalentes
                            miro las transiciones de la B -> B y G tienen la misma clase de equivalencia( 0 = 0)
                                                            hago lo mismo con C...

                            asi todo el rato hasta quedarme si estados para revisar...

             3.3 - Una vez que hemos mirado todos los estados a los que llego desde ese estado (A), paso al siguiente estado que no tenga clase de equivalencia
             3.4 - Repito los 2 pasos anteriores hasta que todos los nodos tengan clase de equivalencia  
             3.5 - Una vez que tengo todos los estados con clases de equivalencia, 3.2, 3.3, 3.4 -> Todo esto es una iteracion
             3.6 - Finaliza la funcion si iteracion actual = iteracion anterior (iteracion actual - 1) 
        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        
        #---------------------------------------------------------------------
        raise NotImplementedError("This method must be implemented.")


    