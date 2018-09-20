import re
class Automaton:

    def __init__(self, automaton_name):
        self.automaton_name = automaton_name


class State:

    def __init__(self, state_id,is_initial, is_final, edges=None):
        self.state_id = state_id
        self.is_initial = is_initial
        if edges is None:
            self.edges = []
        else: 
            self.edges = edges

class Edge:

    def __init__(self, initial_state, final_state, is_recursive, edge_accepted_values=None):
        self.initial_state = initial_state
        self.final_state =  final_state
        self.is_recursive = is_recursive
        if edge_accepted_values is None:
            self.edge_accepted_values = []
        else:
            self.edge_accepted_values = edge_accepted_values

    @classmethod
    def read_from_str(cls, line_str):
        
        line_arr = re.split(",", line_str)
        edge_str = ''.join(list(filter(lambda x: '-' in x, line_arr)))
        states_arr = list(filter(lambda x: '(' in x, line_arr))
        recursive = re.findall(r"[\w']+", states_arr[0]) == re.findall(r"[\w']+", states_arr[1])
        accepted_values = re.findall(r'\d+',edge_str)
        edge = Edge(''.join(re.findall(r"[\w']+", states_arr[0])), ''.join(re.findall(r"[\w']+", states_arr[1])), recursive, accepted_values )
        return edge


class DFA(Automaton):

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
        automaton_arr = list(filter(lambda x: len(x)>0,re.split("\n", automaton_str)))  
        edges = []
        states = []
        states_tmp = []
        for x in range(0,len(automaton_arr)):
            edges.append(Edge.read_from_str(automaton_arr[x]))
            states_tmp.extend(list(filter(lambda x: '(' in x, re.split(",",automaton_arr[x]))))
        
        states_arr = list(set(states_tmp))
        for x in range(0,len(states_arr)):
            print(states_arr[x])
            states.append(State())



   
automaton_file = open("automata.txt")
automaton_string = automaton_file.read()
DFA.read_from_str(automaton_string)



