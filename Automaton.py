import re

class Automaton:

    ndfa = False

    def __init__(self, automaton_name, states=None, edges=None):
        self.automaton_name = automaton_name

        if states is None :
            self.states = []
        else:
            self.states = states

        if edges is None :
            self.edges = []
        else:
            self.edges = edges

    @classmethod
    def read_from_str(cls, automaton_arr):
        automaton_type = ""
        edges = []
        initial_state = ""
        final_state = ""
        states = []
        states_tmp = []
        for x in range(0,len(automaton_arr)):
            edges.append(Edge.read_from_str(automaton_arr[x]))
            states_tmp.extend(list(filter(lambda x: '(' in x, re.split(",",automaton_arr[x]))))
        
        states_arr = list(set(states_tmp))
        for x in range(0,len(states_arr)):
            is_final = "((" in states_arr[x]
            is_initial = ">" in states_arr[x]
            state_id = ''.join(re.findall(r"[\w']+", states_arr[x]))
            state_edges = list(filter(lambda x: x.initial_state == state_id, edges))
            if len(state_edges[0].edge_accepted_values) == 0:
                Automaton.ndfa = True
            state = State(state_id, is_initial, is_final, state_edges)
            states.append(state)
            if  is_initial:
                initial_state = state
            if is_final:
                final_state = state
        if Automaton.ndfa:
            return NDFA("automatonDFA", initial_state, final_state, states, edges)
        else:
            return DFA("automatonDFA", initial_state, final_state, states, edges)

class State:

    def __init__(self, state_id,is_initial, is_final, edges=None):
        self.state_id = state_id
        self.is_initial = is_initial
        self.is_final = is_final
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

    def __init__(self, automaton,initial_state, final_state, states=None, edges=None):
        super().__init__(automaton)
        self.initial_state = initial_state
        self.final_state = final_state
        if any(x for x in edges if len(x.edge_accepted_values) == 0) == True:
            return None
        if states is None:
            self.states = [] 
            self.edges = []
        else:
            self.states = states
            if edges is None:
                self.edges = []
            else:
                self.edges = edges
        

    def evaluate_expresion_by_automaton(self, expresion_str, actual_state):  
        
        if expresion_str != "":
            expresion_arr = list(expresion_str)
            for x in range(0,len(actual_state.edges)):
                for z in range(0, len(expresion_arr)):
                    if any(expresion_arr[z] in s for s in actual_state.edges[x].edge_accepted_values):
                        if expresion_str != "":
                            expresion_arr.remove(expresion_arr[x])
                            expresion_str = ''.join(expresion_arr)
                            actual_state = next((a for a in self.states if a.state_id == actual_state.edges[x].final_state), None)
                            return self.evaluate_expresion_by_automaton(expresion_str, actual_state)
                        elif actual_state.is_final and expresion_str == "" :
                            return True
                    else:
                        return False 
        elif actual_state.is_final:
            return True
        else:
            return False

class NDFA(Automaton):

    def __init__(self, automaton,initial_state, final_state, states=None, edges=None):
        super().__init__(automaton)
        self.initial_state = initial_state
        self.final_state = final_state
        if any(x for x in edges if len(x.edge_accepted_values) == 0) == True:
            return None
        if states is None:
            self.states = [] 
            self.edges = []
        else:
            self.states = states
            if edges is None:
                self.edges = []
            else:
                self.edges = edges
        

    def evaluate_expresion_by_automaton(self, expresion_str, actual_state):  
        return True
 
automaton_file = open("automata.txt")
automaton_string = automaton_file.read()
automaton_arr = list(filter(lambda x: len(x)>0,re.split("\n", automaton_string))) 
run_program = True

while run_program:
    
    if automaton_arr[0] == '1':
        automaton_arr.pop(0)
        obj_automaton = Automaton.read_from_str(automaton_arr)
        if obj_automaton == None:
            print("Syntax error, check the automaton")
        else:
            expresion_str = input("write an expresion and press enter to evaluate in automaton:  ")
            if expresion_str == "false":
                run_program = False
            print(obj_automaton.evaluate_expresion_by_automaton(expresion_str, obj_automaton.initial_state))
    elif automaton_arr[0] == '2':
        automaton_arr.pop(0)
        obj_automaton = Automaton.read_from_str(automaton_arr)



