
class Automaton:

    def __init__(self, automaton_name):
        self.automaton_name = automaton_name


class State:

    def __init__(self, state_id, state_name, edges = None):
        self.state_id = state_id
        self.state_name = state_name
        if edges is None:
            self.edges = []
        else: 
            self.edges = edges


class Edge:

    def __init__(self, edge_id, edge_accepted_value, is_recursive):
        self.edge_id = edge_id
        self.edge_accepted_value = edge_accepted_value
        self.is_recursive = is_recursive



