"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transitions
from automata.utils import write_dot



def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = [] # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string



class REParser():
    """Class for processing regular expressions in Kleene's syntax."""
    
    def __init__(self) -> None:
        self.state_counter = 0

    def _create_automaton_empty(self):
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language. Type: FiniteAutomaton

        """
        initial_State = State(name=f"q{self.state_counter}", is_final=False)
        self.state_counter += 1
        # Automata Finito con 1 estado (el estado inicial), 0 transiciones 
        return FiniteAutomaton(states=[initial_State], initial_state=initial_State, transitions=Transitions(), symbols=[])
        
        

    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        initial_State = State(name=f"q{self.state_counter}", is_final=True) # acepta la cadena vacia 
        self.state_counter += 1
        return FiniteAutomaton(states=[initial_State], initial_state=initial_State, transitions=Transitions(), symbols=[None])


    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        initial_State = State(name=f"q{self.state_counter}", is_final=False) # acepta la cadena vacia 
        self.state_counter += 1
        final_state = State(name=f"q{self.state_counter}", is_final=True) # acepta la cadena vacia 
        self.state_counter += 1
        transition = Transitions()
        transition.add_transition(initial_State, symbol, final_state)

        return FiniteAutomaton(states=[initial_State, final_state], initial_state=initial_State, transitions=transition, symbols=[symbol]) 

    def _create_automaton_star(self, automaton):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        # Funcion para ver si un nombre de estado esta en el automata -> para no tener estados repetidos
        def state_name_exists(name, states): 
            return any(state.name == name for state in states) 

        # Creo el estado inicial (q0) y el final (qf) 
        while state_name_exists(f"q{self.state_counter}", automaton.states): 
            self.state_counter += 1
        q0 = State(name=f"q{self.state_counter}", is_final=False)
        self.state_counter += 1

        while state_name_exists(f"q{self.state_counter}", automaton.states): 
            self.state_counter += 1
        qf = State(name=f"q{self.state_counter}", is_final=True)
        self.state_counter += 1

        # Obtengo los símbolos y transiciones del autómata pasado por argumento
        symbols = set(automaton.symbols)
        transitions = Transitions(automaton.transitions)

        # Añado las transiciones
        transitions.add_transition(q0, None, automaton.initial_state) # q0 (lambda) -> estado inicial del autómata
        # Creo la transición de q0 a qf
        transitions.add_transition(q0, None, qf) 

        # Tengo que unir los estados finales del automata al estado inicial del automata mediante lambda 
        for state in automaton.states: 
            if state.is_final: 
                if transitions.has_transition_to(state, None, automaton.initial_state):
                    continue
                else:
                    transitions.add_transition(state, None, automaton.initial_state)  

        # Uno todos los estados finales del automata al nuevo estado final qf mediante lambda 
        for state in automaton.states: 
            if state.is_final: 
                state.is_final = False
                if transitions.has_transition_to(state, None, qf):
                    continue 
                else:
                    transitions.add_transition(state, None, qf)

        # Actualizo los estados para el autómata que voy a retornar
        states = [q0, qf]
        states += list(automaton.states) 

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)
 

    def _create_automaton_union(self, automaton1, automaton2):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        # Funcion para ver si un nombre de estado esta en el automata -> para no tener estados repetidos
        def state_name_exists(name, states): 
            return any(state.name == name for state in states) 
        
        # Creo el estado inicial (q0) y el final (qf) 
        while state_name_exists(f"q{self.state_counter}", automaton1.states + automaton2.states): 
            self.state_counter += 1
        q0 = State(name=f"q{self.state_counter}", is_final=False)
        self.state_counter += 1

        while state_name_exists(f"q{self.state_counter}", automaton1.states + automaton2.states): 
            self.state_counter += 1
        qf = State(name=f"q{self.state_counter}", is_final=True)
        self.state_counter += 1

        # Obtengo los simbolos de ambos automatas y los junto en 1 único set
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols) 

        # Obtengo las transiciones de ambos autómatas, las junto, y añado las 2 nuevas de los estados creados antes 
        transitions = Transitions(automaton1.transitions)
        transitions2 = Transitions(automaton2.transitions)
        transitions.update(transitions2)

        transitions.add_transition(q0, None, automaton1.initial_state) # q0 (lambda) -> estado inicial de automaton1
        transitions.add_transition(q0, None, automaton2.initial_state) # q0 (lambda) -> estado inicial de automaton2

        # Cambiamos los estados finales y añadimos nuevas transiciones a los estados finales 
        # Automata 1 
        for state in automaton1.states: 
            if state.is_final: 
                state.is_final = False 
                transitions.add_transition(state, None, qf) 
        # Automata 2 
        for state in automaton2.states: 
            if state.is_final: 
                state.is_final = False 
                transitions.add_transition(state, None, qf) 

        # Actualizamos los estados 
        states = [q0, qf]
        states += list(automaton1.states)
        states += list(automaton2.states)

        return FiniteAutomaton(q0, states, symbols, transitions) 


    def _create_automaton_concat(self, automaton1, automaton2):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        # Obtengo los simbolos de ambos automatas y los junto en 1 único set
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols) 

        # Obtengo las transiciones de ambos autómatas, las junto, y  
        transitions = Transitions(automaton1.transitions)
        transitions2 = Transitions(automaton2.transitions)
        transitions.update(transitions2) 

        # Cambiamos los estados finales y añadimos nuevas transiciones a los estados finales 
        # Añado la nueva transicion del estado final de automaton1 al estado inicial de automaton2
        # Automata 1 
        for state in automaton1.states: 
            if state.is_final: 
                transitions.add_transition(state, None, automaton2.initial_state)
                state.is_final = False  
        
        # Actualizamos los estados 
        states = list(automaton1.states)
        states += list(automaton2.states)

        return FiniteAutomaton(automaton1.initial_state, states, symbols, transitions) 

    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_empty()
        
        rpn_string = _re_to_rpn(re_string)

        stack = [] # list of FiniteAutomatons

        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                automata_concatenado = self._create_automaton_concat(aut1, aut2)
                stack.append(automata_concatenado)
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()
    
    
