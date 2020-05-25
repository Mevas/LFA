class RegGr:
    def __init__(self, input):
        self.states = input
        self.s_had_eps = False

    def __str__(self):
        string = ''

        for state, non_term in self.states.items():
            string += f'{state}: {non_term}\n'

        return string

    def remove_epsilon(self):
        if 'ε' in self.states['S']:
            self.s_had_eps = True

        for state, values in self.states.items():
            if 'ε' in values:
                for state_to_check, values_to_check in self.states.items():
                    for value in values_to_check:
                        if state in value:
                            self.states[state_to_check] += value[0]
                self.states[state] = [value for value in self.states[state] if value != 'ε']

        if self.s_had_eps:
            self.states['S1'] = self.states['S'] + ['ε']


class NFA:
    class Node:
        def __init__(self, name, initial, final, to_nodes, from_nodes):
            self.name = name
            self.initial = initial
            self.final = final
            self.to_nodes = to_nodes
            self.from_nodes = from_nodes

    def __init__(self, reg):
        self.states = list(reg.states.keys())

        # Add terminal state D0
        self.states += ['D0']

        self.num_states = len(self.states)
        self.initial_state = 'S1' if 'S1' in self.states else 'S'
        self.final_states = ['S1', 'D0'] if 'S1' == self.initial_state else ['D0']

        self.transitions = []
        for state, values in reg.states.items():
            for non_term in values:
                if len(non_term) == 2:
                    self.transitions += [[state, non_term[0], non_term[1]]]
                elif non_term != 'ε':
                    self.transitions += [[state, non_term, 'D0']]

    # def __str__(self):
    #     resp = f'Total states: {self.num_states}\n' \
    #            f'# transitions: {len(self.transitions)}\n'
    #
    #     for transition in self.transitions:
    #         resp += f'{transition[0]} {transition[2]} {transition[1]}\n'
    #
    #     resp += f'Initial state: {self.initial_state}\n' \
    #             f'Final states: {self.final_states}\n'
    #
    #     return resp

    def __str__(self):
        resp = f'{self.num_states}\n' \
               f'{len(self.transitions)}\n'

        for transition in self.transitions:
            resp += f'{transition[0]} {transition[2]} {transition[1]}\n'

        resp += f'{self.initial_state}\n' \
                f'{len(self.final_states)}\n'

        for state in self.final_states:
            resp += f'{state}\n'

        return resp


def read_input(filename):
    parsed = {}

    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            line = line.split()
            line[1] = line[1].split('|')
            line[1][-1] = line[1][-1].replace('\n', '')
            parsed[line[0]] = line[1]

    return parsed


if __name__ == '__main__':
    files = ['input.txt']

    for file in files:
        parsed = read_input(file)

        reg = RegGr(parsed)
        print(reg)

        reg.remove_epsilon()
        print(reg)

        nfa = NFA(reg)
        with open('output.txt', 'w+') as f:
            print(nfa, file=f)
