from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic, write_dot
import queue

class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic(finiteAutomaton):
        """Returns an equivalent deterministic finite automaton."""
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        # Estado inicial del automata determinista 
        initial_state = frozenset(evaluator.current_states)
        
        # Diccionario para guardar la tabla de transiciones 
        # Va a ser un diccionario de diccionarios 
        dfa_states = dict() 

        # Set de estados para el nuevo automata 
        new_states = set()
        new_states.add(initial_state)
        empty_state = State("empty", False) # Estado sumidero 
        new_states.add(empty_state)

        # Cola para tratar los estados para procesr 
        states_to_check = queue.Queue()
        states_to_check.put(initial_state)
        #import pdb; pdb.set_trace()
        # Mientras queden estados en la cola
        while not states_to_check.empty():
            # Obtengo el conjunto de estados actual 
            state = states_to_check.get()
            evaluator.current_states = state 
            #print(f"Process Symbol Antes {evaluator.current_states}")
            for symbol in finiteAutomaton.symbols:
                evaluator.process_symbol(symbol) 
                #print(f"Process Symbol Despues {evaluator.current_states, symbol}")

                # Si el estado no esta en el diccionario -> lo añado 
                if state not in dfa_states.keys():
                    dfa_states[state] = dict() 

                if any(symbol in finiteAutomaton.transitions[s] for s in state): 
                    # Añado el nuevo estado al diccionario 
                    dfa_states[state][symbol] = set(evaluator.current_states)
                else: 
                # Si esta en el diccionario y no tiene transicion con symbol -> añado esa transicion al estado sumidero 
                    dfa_states[state][symbol] = {empty_state} # todos los estados seran conjuntos 

                # Si el estado no esta en los estados del automata determinista -> lo añado
                if evaluator.current_states not in new_states and len(evaluator.current_states) > 0 :
                    new_states.add(frozenset(evaluator.current_states))
                    states_to_check.put(frozenset(evaluator.current_states)) 

        # Añado las transiciones a los estados del nuevo automata 
        transitions = Transitions(dfa_states)

        # Añado las transiciones al estado sumidero 
        for symbols in finiteAutomaton.symbols: 
            if symbol == None: continue # No añado la transicion lambda 
            transitions.add_transition(empty_state, symbol, symbols)
        
        print(transitions)

        dfa = FiniteAutomaton(initial_state, new_states, finiteAutomaton.symbols, transitions)
        

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


    