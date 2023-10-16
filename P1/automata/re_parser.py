"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transitions

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
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        #---------------------------------------------------------------------

        
        

    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------


    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------


    def _create_automaton_star(self, automaton):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")  
        #---------------------------------------------------------------------


    def _create_automaton_union(self, automaton1, automaton2):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")  
        #---------------------------------------------------------------------


    def _create_automaton_concat(self, automaton1, automaton2):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------


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
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()
"""
# Start with the first two methods: _create_automaton_empty and _create_automaton_lambda

def _create_automaton_empty():
    """
    Create an automaton that accepts the empty language.

    Returns:
        Automaton that accepts the empty language. Type: FiniteAutomaton
    """
    # Create a new state
    state = State('q0', is_initial=True, is_final=False)
    
    # Create an automaton with only the initial state and no transitions
    automaton = FiniteAutomaton(states={state}, alphabet=set())
    
    return automaton


def _create_automaton_lambda():
    
    Create an automaton that accepts the empty string.

    Returns:
        Automaton that accepts the empty string. Type: FiniteAutomaton
  
    # Create a new initial and final state
    state = State('q0', is_initial=True, is_final=True)
    
    # Create an automaton with only one state which is both initial and final, and no transitions
    automaton = FiniteAutomaton(states={state}, alphabet=set())
    
    return automaton

# Insert these methods into the REParser class content
re_parser_updated = re_parser_content.replace(
    '# TO DO: Implement this method...',
    '# TO DO: Implement this method...\n' + _create_automaton_empty.__doc__ + '\n' + 
    '    ' + '\n    '.join(_create_automaton_empty.__code__.co_firstlineno) + 
    '\n\n' + _create_automaton_lambda.__doc__ + '\n' + 
    '    ' + '\n    '.join(_create_automaton_lambda.__code__.co_firstlineno)
)

re_parser_updated[:1000]  # Display the first 1000 characters of the updated content for review


def _create_automaton_symbol(symbol):
    
    Create an automaton that accepts a given symbol.

    Args:
        symbol: The symbol that the automaton should accept. Type: str

    Returns:
        Automaton that accepts the given symbol. Type: FiniteAutomaton
    
    # Create the initial and final states
    initial_state = State('q0', is_initial=True, is_final=False)
    final_state = State('q1', is_initial=False, is_final=True)
    
    # Create the transition for the given symbol
    transitions = Transitions({initial_state: {symbol: final_state}})
    
    # Create the automaton with the states, transitions, and the symbol in its alphabet
    automaton = FiniteAutomaton(states={initial_state, final_state}, alphabet={symbol}, transitions=transitions)
    
    return automaton

# Extract source code from the function and adapt it to be a method of REParser
create_automaton_symbol_code = inspect.getsource(_create_automaton_symbol).replace('_create_automaton_symbol', 'def _create_automaton_symbol(self, symbol)')

# Insert this method into the REParser class content
re_parser_updated = re_parser_updated.replace(
    'def _create_automaton_symbol(self, symbol):',
    create_automaton_symbol_code
)

re_parser_updated[:3000]  # Display the first 3000 characters of the updated content for review

def _create_automaton_star(automaton):
    
    Create an automaton that represents the Kleene star of a given automaton.

    Args:
        automaton: The automaton to be starred. Type: FiniteAutomaton

    Returns:
        Automaton representing the Kleene star of the given automaton. Type: FiniteAutomaton
    
    # Create new initial and final states
    initial_state = State('q_star_initial', is_initial=True, is_final=True)
    final_state = State('q_star_final', is_initial=False, is_final=True)
    
    # Update the existing initial states to be non-initial
    for state in automaton.states:
        if state.is_initial:
            state.is_initial = False
    
    # Add ε-transitions from the new initial state to the old initial states
    for state in automaton.states:
        if state.is_initial == False and state.is_final:
            automaton.transitions.add_transition(initial_state, 'λ', state)
    
    # Add ε-transitions from the old final states to the new final state
    for state in automaton.states:
        if state.is_final:
            automaton.transitions.add_transition(state, 'λ', final_state)
    
    # Add the new states to the automaton's state set
    automaton.states.update({initial_state, final_state})
    
    # Update the automaton's alphabet to include 'λ' if it's not already there
    automaton.alphabet.add('λ')
    
    return automaton

# Extract source code from the function and adapt it to be a method of REParser
create_automaton_star_code = inspect.getsource(_create_automaton_star).replace('_create_automaton_star', 'def _create_automaton_star(self, automaton)')

# Insert this method into the REParser class content
re_parser_updated = re_parser_updated.replace(
    'def _create_automaton_star(self, automaton):',
    create_automaton_star_code
)

re_parser_updated[:4000]  # Display the first 4000 characters of the updated content for review


def _create_automaton_union(automaton1, automaton2):
    
    Create an automaton that represents the union of two given automata.

    Args:
        automaton1: The first automaton for the union. Type: FiniteAutomaton
        automaton2: The second automaton for the union. Type: FiniteAutomaton

    Returns:
        Automaton representing the union of the two given automata. Type: FiniteAutomaton
    
    # Create new initial and final states
    initial_state = State('q_union_initial', is_initial=True, is_final=False)
    final_state = State('q_union_final', is_initial=False, is_final=True)
    
    # Add ε-transitions from the new initial state to the initial states of both automata
    for state in automaton1.states.union(automaton2.states):
        if state.is_initial:
            automaton1.transitions.add_transition(initial_state, 'λ', state)
            automaton2.transitions.add_transition(initial_state, 'λ', state)
    
    # Add ε-transitions from the final states of both automata to the new final state
    for state in automaton1.states.union(automaton2.states):
        if state.is_final:
            automaton1.transitions.add_transition(state, 'λ', final_state)
            automaton2.transitions.add_transition(state, 'λ', final_state)
    
    # Combine states, alphabet, and transitions of both automata
    combined_states = automaton1.states.union(automaton2.states).union({initial_state, final_state})
    combined_alphabet = automaton1.alphabet.union(automaton2.alphabet).union({'λ'})
    combined_transitions = automaton1.transitions.union(automaton2.transitions)
    
    # Create the resulting automaton
    union_automaton = FiniteAutomaton(states=combined_states, alphabet=combined_alphabet, transitions=combined_transitions)
    
    return union_automaton

def _create_automaton_concat(automaton1, automaton2):
    """
    Create an automaton that represents the concatenation of two given automata.

    Args:
        automaton1: The first automaton for the concatenation. Type: FiniteAutomaton
        automaton2: The second automaton for the concatenation. Type: FiniteAutomaton

    Returns:
        Automaton representing the concatenation of the two given automata. Type: FiniteAutomaton
    """
    # Add ε-transitions from the final states of the first automaton to the initial states of the second automaton
    for state1 in automaton1.states:
        for state2 in automaton2.states:
            if state1.is_final and state2.is_initial:
                automaton1.transitions.add_transition(state1, 'λ', state2)
    
    # Combine states, alphabet, and transitions of both automata
    combined_states = automaton1.states.union(automaton2.states)
    combined_alphabet = automaton1.alphabet.union(automaton2.alphabet)
    combined_transitions = automaton1.transitions.union(automaton2.transitions)
    
    # Create the resulting automaton
    concat_automaton = FiniteAutomaton(states=combined_states, alphabet=combined_alphabet, transitions=combined_transitions)
    
    return concat_automaton

# Extract source code from the functions and adapt them to be methods

"""