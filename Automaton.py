import re
class Automaton:

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
 
    @classmethod
    def read_from_str(cls, automaton_str):
        automaton_arr = list(filter(lambda x: len(x)>0,re.split("\n", automaton_str)))  
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
            state = State(state_id, is_initial, is_final, state_edges)
            states.append(state)
            if  is_initial:
                initial_state = state
            if is_final:
                final_state = state

        return DFA("automatonDAF", initial_state, final_state, states, edges)

   
automaton_file = open("automata.txt")
automaton_string = automaton_file.read()
automatonDFA = DFA.read_from_str(automaton_string)
if automatonDFA == None:
    print("Syntax error, check the automaton")
else:
    run_program = True
    while run_program:
        expresion_str = input("write an expresion and press enter to evaluate in automaton:  ")
        if expresion_str == "false":
            run_program = False
        print(automatonDFA.evaluate_expresion_by_automaton(expresion_str, automatonDFA.initial_state))



