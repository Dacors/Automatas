import re
import xlrd

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
    def read_from_xls(cls, automaton_file):
        information_sheet =  automaton_file.sheet_by_index(0)
        automaton_sheet = automaton_file.sheet_by_index(1)
        automaton_initial_state_id = information_sheet.cell_value(1,1)
        automaton_final_state_id = information_sheet.cell_value(2,1)
        automaton_initial_state = State
        automaton_final_state = State
        automaton_states = []

        for i in range(1,automaton_sheet.ncols):
            automaton_edges = []
            is_initial = False
            is_final = False
            for b in range(1,automaton_sheet.nrows):
                if automaton_sheet.cell_value(i,b) == 'E' and automaton_sheet.cell_value(i,b) != 'x':
                    Automaton.ndfa = True
                    edge_accepted_values = automaton_sheet.cell_value(i,b)
                    initial_state = automaton_sheet.cell_value(i,0)
                    final_state = automaton_sheet.cell_value(0,b)
                    automaton_edges.append(Edge(initial_state,final_state,edge_accepted_values))
                elif automaton_sheet.cell_value(i,b) != 'x':
                    edge_accepted_values = re.split(',',automaton_sheet.cell_value(i,b))
                    initial_state = automaton_sheet.cell_value(i,0)
                    final_state = automaton_sheet.cell_value(0,b)
                    automaton_edges.append(Edge(initial_state,final_state,edge_accepted_values))

            if automaton_sheet.cell_value(i,0) == automaton_initial_state_id:
                is_initial = True
                state = State(automaton_sheet.cell_value(i,0),is_initial,is_final,automaton_edges)
                automaton_states.append(state)
                automaton_initial_state = state
            elif automaton_sheet.cell_value(i,0) == automaton_final_state_id:
                is_final = True
                state = State(automaton_sheet.cell_value(i,0),is_initial,is_final,automaton_edges)
                automaton_states.append(state)
                automaton_final_state = state
            else:
                automaton_states.append(State(automaton_sheet.cell_value(i,0),is_initial,is_final,automaton_edges))

        if Automaton.ndfa:
            return NDFA("AutomatonNDFA",automaton_initial_state,automaton_final_state,automaton_states)
        else:
            return DFA("AutomatonDFA",automaton_initial_state,automaton_final_state,automaton_states)

        

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

    def __init__(self, initial_state, final_state, edge_accepted_values=None):
        self.initial_state = initial_state
        self.final_state =  final_state
        if edge_accepted_values is None:
            self.edge_accepted_values = []
        else:
            self.edge_accepted_values = edge_accepted_values

class DFA(Automaton):

    def __init__(self, automaton,initial_state, final_state, states=None):
        super().__init__(automaton)
        self.initial_state = initial_state
        self.final_state = final_state
        if states is None:
            self.states = [] 
        else:
            self.states = states
            

    def evaluate_expresion_by_automaton(self, expresion_str,actual_state):  
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

    def __init__(self, automaton,initial_state, final_state, states=None):
        super().__init__(automaton)
        self.initial_state = initial_state
        self.final_state = final_state
        if states is None:
            self.states = [] 
        else:
            self.states = states

    def evaluate_expresion_by_automaton(self, expresion_str,actual_state):  
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

automaton_file = xlrd.open_workbook("Automaton.xlsx")
sheet = automaton_file.sheet_by_index(0)
action = int(sheet.cell_value(0,1))
run_program = True

while run_program:
    
    if action == 1:
        obj_automaton = Automaton.read_from_xls(automaton_file)
        if obj_automaton == None:
            print("Syntax error, check the automaton")
        else:
            expresion_str = input("write an expresion and press enter to evaluate in automaton:  ")
            if expresion_str == "exit":
                run_program = False
            print(obj_automaton.evaluate_expresion_by_automaton(expresion_str,obj_automaton.initial_state))
    elif action == 2:
        automaton_arr.pop(0)
        obj_automaton = Automaton.read_from_str(automaton_arr)



