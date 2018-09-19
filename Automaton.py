
class Automaton:

    def __init__(self, automaton_name):
        self.automaton_name = automaton_name


class State:

    def __init__(self, state_id, state_name, edges=None):
        self.state_id = state_id
        self.state_name = state_name
        if edges is None:
            self.edges = []
        else: 
            self.edges = edges


class Edge:

    def __init__(self, edge_id, is_recursive, edge_accepted_values=None):
        self.edge_id = edge_id
        self.is_recursive = is_recursive
        if edge_accepted_values is None:
            self.edge_accepted_values = []
        else:
            self.edge_accepted_values = edge_accepted_values

class Reader:

    def __init__(self, automaton, states=None, edges=None):
        self.automaton = automaton
        if states is None:
            states = [] 
            edges = []
        else:
            states = states
            if edges is None:
                edges = []
            else:
                edges = edges
    
    @classmethod
    def read_from_str(cls, automaton_str):
        print(automaton_str)

automaton_file = open("automata.txt")
automaton_string = automaton_file.read()

Reader.read_from_str(automaton_string)



