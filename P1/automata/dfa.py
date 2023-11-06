from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic, write_dot
import re

class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic(finiteAutomaton):
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        from queue import Queue

        # Funcion para sacar el nombre de un conjunto de estados ordenado 
        def order_states (states):
            # Averiguo el nombre del conjunto
            name = str()
            for state in states: 
                name += state.name
            # Divide la cadena en partes usando expresiones regulares
            partes = re.findall(r'q\d+', name)
            # Ordena las partes convirtiendo el número en entero
            partes_ordenadas = sorted(partes, key=lambda x: int(re.search(r'\d+', x).group()))
            # Une las partes ordenadas y devuelve el resultado
            return ''.join(partes_ordenadas)

        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)
        # Estado inicial del automata determinista
        initial_state = frozenset(evaluator.current_states)
        init_state = State(order_states(evaluator.current_states), any(state.is_final for state in evaluator.current_states)) 
        # Conjunto de transiciones del AFD
        transitions = Transitions()
        #import pdb; pdb.set_trace()
        # Diccionario para guardar la tabla de transiciones
        dfa_states = {
            initial_state: State(order_states(evaluator.current_states), any(state.is_final for state in initial_state))
        }
        
        # Simbolos para el automata determinista
        dfa_symbols = list()
        for symbol in finiteAutomaton.symbols: 
            if symbol != 'λ': dfa_symbols.append(symbol)

        # Estado sumidero
        empty_state = State("empty", False)
        dfa_states[frozenset()] = empty_state # Añadir el estado sumidero al diccionario de estados

        # Cola para tratar los estados para procesar
        states_to_check = Queue()
        states_to_check.put(initial_state)
        
        # Mientras queden estados en la cola
        while not states_to_check.empty():
            # Obtengo el conjunto de estados actual
            current_states_frozenset = states_to_check.get()

            for symbol in dfa_symbols:
                evaluator.current_states = set(current_states_frozenset)  # Estado actual
                evaluator.process_symbol(symbol)  # Procesar el símbolo

                # Crear un frozenset para los nuevos estados después de la transición
                new_states_frozenset = frozenset(evaluator.current_states)

                # Crear un nuevo State object para el nuevo estado
                new_state = State(order_states(evaluator.current_states), any(state.is_final for state in evaluator.current_states))

                # Añadir el nuevo estado al diccionario si no existe
                if new_states_frozenset not in dfa_states and evaluator.current_states:
                    dfa_states[new_states_frozenset] = new_state
                    states_to_check.put(new_states_frozenset)
                # Si el estado actual no tiene transición para el símbolo actual, añadir una transición al estado sumidero
                if not evaluator.current_states:
                    #transitions.add_transition(current_states_frozenset, symbol, empty_state)
                    transitions.add_transition(dfa_states[current_states_frozenset], symbol, empty_state)
                else: 
                    # Añadir la transición al diccionario de transiciones
                    #transitions.add_transition(current_states_frozenset, symbol, new_state)
                    transitions.add_transition(dfa_states[current_states_frozenset], symbol, new_state)

        # Añadir las transiciones del estado sumidero al estado sumidero
        for symbol in finiteAutomaton.symbols:
            if symbol != 'λ': transitions.add_transition(empty_state, symbol, empty_state)

        # Construir el nuevo automata determinista
        dfa = FiniteAutomaton(init_state, dfa_states.values(), dfa_symbols, transitions)

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


    