from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic, write_dot
from functools import cmp_to_key
import re

# Funcion que compara 2 estados 
def comp(state1, state2):
    state1_name = state1.name.lower()
    state2_name = state2.name.lower()

    # Criterios: Estado inicial -> 1º, empty -> ultimo
    if state1_name == "initial": return -1
    elif state2_name == "initial": return 1
    if state1_name == "empty": return 1
    elif state2_name == "empty": return -1
    if state1_name == "qf" or state1_name == "final": return 1
    elif state2_name == "qf" or state2_name == "final": return -1
    
    # En otro caso
    if state1_name[1:].isdigit() and state2_name[1:].isdigit():
        return int(state1_name[1:]) - int(state2_name[1:])

    # Para el caso de que los estados sean letras (A, B...)
    val_state1 = 0
    val_state2 = 0

    for i in state1_name:
        val_state1 += ord(i)
    for i in state2_name:
        val_state2 += ord(i)
    
    return val_state1 - val_state2 

# Creamos un estado a partir de un conjunto de estados -> La usamos en to_minimized
def state_create(set_states):
    list_states = list(set_states)
    # Lista de estados ordenada usando el comparador anterior
    sorted_state_list = sorted(list_states, key=cmp_to_key(comp))
    # Nombre del estado
    name = str()
    final = False

    # Si los estados son A, B, C no tienen un numero asociado
    letters = False
    if sorted_state_list[0].name[1:0].isdigit():
        letters = True
    
    for state in sorted_state_list:
        # Junto el nombre de todos los estados
        if letters: name += "q" + state.name[1:] + ","
        else: name += state.name 

        # Si alguno de los estados es final, el estado tambien lo es
        if state.is_final: final = True
    
    # Elimino la ultima coma
    if letters: name = name[:-1]

    return State(name, final) 

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

# Funcion para comprobar si un automata es determinista
def is_deterministic(finiteAutomaton):
    for state in finiteAutomaton.states:
        for symbol in finiteAutomaton.symbols:
            # Sin transicion para el simbolo
            if len(finiteAutomaton.transitions.get_transition(state, symbol)) == 0:
                return False
            # Varias transiciones para el mismo simbolo
            n_transitions = len(finiteAutomaton.transitions.get_transition(state, symbol))
            if n_transitions > 1:
                return False
            
            
    return True

class DeterministicFiniteAutomaton(FiniteAutomaton):
            
    @staticmethod
    def to_deterministic(finiteAutomaton):
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        from queue import Queue

        # Si el automata ya es determinista lo devolvemos
        if is_deterministic(finiteAutomaton):
            return finiteAutomaton

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
        from queue import Queue
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(dfa) # Conjunto de estados actual
        previous = FiniteAutomatonEvaluator(dfa) # Estado del que vengo al llegar al actual 
        
        # Verifica que el automata sea determinista
        # if not isinstance(dfa, DeterministicFiniteAutomaton):
            # raise ValueError("El autómata no es determinista")

        # Eliminacion estados inaccesibles usando BFS 
        q = Queue()
        q.put(evaluator.current_states)
        accesible_states = set()
        accesible_states.add(dfa.initial_state)
        while not q.empty():
            state = q.get()
            for sym in dfa.symbols:
                evaluator.current_states = state
                evaluator.process_symbol(sym)
                if len(evaluator.current_states) > 0:
                    flag_addqueue=False
                    for next_state in evaluator.current_states:
                        if next_state not in accesible_states:
                            if not flag_addqueue:
                                q.put(evaluator.current_states)
                                flag_addqueue=True
                            accesible_states.add(next_state)
        
        accesible_states_list = sorted(list(accesible_states), key=cmp_to_key(comp))

        ############################### CLASES DE EQUIVALENCIA #########################################
        
        # Usamos una matriz para guardar las clases de equivalencia: fila 0 -> estados, fila 1 -> clases de equivalencia (1º Iteración)
        matrix = [list(state for state in accesible_states_list)]                      # Primera fila 
        matrix.append([1 if state.is_final else 0 for state in accesible_states_list]) # Segunda fila 
        # Recorremos la tabla de izqda a dcha y asignamos la clase 0 al primer estado sin clase de equivalencia 
        matrix.append([None] * len(matrix[0])) # Añadimos una fila vacia para las iteraciones 
        #import pdb; pdb.set_trace() 
        while True:
            counter_classes = 0
            
            for j in range(len(accesible_states_list)):  
                # 1º Iteracion -> Asdignamos la clase 0 al primer estado sin clase de equivalencia
                if matrix[2][j] == None: 
                    matrix[2][j] = counter_classes
                    counter_classes += 1

                    # Comparamos las transiciones 
                    for i in range(1, len(accesible_states_list)):
                        same_class = True # Flag para saber si todos los estados de la clase son equivalentes
                        # 1º Requisito -> El estado siguiente no puede tener clase de equivalencia asignada 
                        if matrix[2][i] == None: 
                            # 2º Requisito -> La clase de equivalencia en la iteracion anterior dene ser igual
                            if matrix[1][i] == matrix[1][j]:
                                for symbol in dfa.symbols: 
                                    # 3º requisito -> Las transiciones deben ser equivalentes 
                                    previous.current_states = {accesible_states_list[j]}
                                    evaluator.current_states = {accesible_states_list[i]}
                                    # Obtenemos transiciones 
                                    previous.process_symbol(symbol)
                                    evaluator.process_symbol(symbol)
                                    # Obtenemos el estado (sin conjunto)
                                    previous_state = previous.current_states.pop()
                                    actual_state = evaluator.current_states.pop()
                                    # Verificamos si las clases coniciden 
                                    if matrix[1][accesible_states_list.index(previous_state)] != matrix[1][accesible_states_list.index(actual_state)]:
                                        same_class = False
                                        break
                                    
                                # Si cumple los 3 requisitos => son equivalentes => asignamos la misma clase de equivalencia
                                if same_class:
                                    matrix[2][i] = matrix[2][j]
            
            # CONDICION DE PARADA DEL ALGORITMO => si las filas son iguales, paramos
            if matrix[1] == matrix[2]:
                break
            else: 
                # Si no, la 3º fila se convierte en la segunda 
                for i in range(len(accesible_states_list)):
                    matrix[1][i] = matrix[2][i]
                    matrix[2][i] = None

        ############################# CONSTRUCCION DEL AUTOMATA MINIMIZADO ############################# 
        # Estados 
        first_row = [matrix[1][i] for i in range(len(matrix[0]))]
        first_row.sort(reverse=True) # Ordenamos la primera lista de mayor a menor (decreciente)
        new_states_tam = int(first_row[0]) + 1 # Numero de estados del automata minimizado

        new_minimized_states = [set() for i in range(new_states_tam)] 
        for i in range(len(accesible_states_list)):
            new_minimized_states[matrix[1][i]].add(accesible_states_list[i])
        final_minimized_states = set() 

        # Transiciones 
        transitions_dict = dict()
        for i in range(new_states_tam):
            # Creamos el estado
            state = state_create(new_minimized_states[i]) 
            final_minimized_states.add(state)

            transitions_dict[state] = dict()
            for symbol in dfa.symbols: 
                # Averiguamos todas las transiciones 
                evaluator.current_states = new_minimized_states[i]
                evaluator.process_symbol(symbol)
                transitions_dict[state][symbol] = set()

                # Si no esta en el set de estados 
                if evaluator.current_states not in new_minimized_states:
                    # Averiguamos el estado solo 
                    current_state = evaluator.current_states.pop()
                    evaluator.current_states = new_minimized_states[matrix[1][accesible_states_list.index(current_state)]]

                # Añadimos el estado 
                transitions_dict[state][symbol].add(state_create(evaluator.current_states)) 
        
        transitions = Transitions(transitions_dict)

        minimized_automaton = FiniteAutomaton(state_create(new_minimized_states[0]), 
                                              final_minimized_states, 
                                              dfa.symbols, 
                                              transitions)
        
        return minimized_automaton 
    
        

        

           
    
        


     