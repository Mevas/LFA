import copy


class NFA:
    def __init__(self, num_states, alphabet, states, initial_state, final_states):
        self.num_states = num_states
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states

        self.current_state = self.initial_state

    def __str__(self):
        resp = f'Total states: {self.num_states}\n' \
               f'Alphabet: {self.alphabet}\n'

        for from_state, node in enumerate(self.states):
            for char, states in node.items():
                for to_state in states:
                    resp += f'{from_state} {to_state} {char}\n'

        resp += f'Initial state: {self.initial_state}\n' \
                f'Final states: {self.final_states}\n'

        return resp

    def is_in_final_state(self):
        return self.current_state in self.final_states

    def get_epsilon_closure(self):
        states_epsilon_closure = {}

        for node, state in enumerate(self.states):
            states_epsilon_closure[node] = state['$'] if '$' in state else []

        # Modify states_epsilon_closure by reference until it remains unchanged over an iteration
        while self.update_closure(states_epsilon_closure):
            pass

        for i in range(self.num_states):
            self.states[i]['$'] = states_epsilon_closure[i]

        return states_epsilon_closure

    def update_closure(self, states_epsilon_closure):
        # To keep track if the closure has changed over the past iteration or not
        has_changed = False
        for i in range(self.num_states):
            updated_closure = set()
            # Reunite the new closure with all closures in the epsilon states
            for state in states_epsilon_closure[i]:
                updated_closure |= states_epsilon_closure[state]
            # If it has changed, update the previous closure and mark the iteration as changed, to continue the while
            if updated_closure != states_epsilon_closure[i]:
                has_changed = True
                states_epsilon_closure[i] = updated_closure
        return has_changed

    def get_reached_states(self, states, char):
        # Function for getting the states that a list of states can reach, given a character
        reached_states = []
        for state in states:
            if char not in self.states[state]:
                continue
            reached_states += self.states[state][char]
        return set(reached_states)

    def remove_epsilon(self):
        new_nfa = self
        # Add the initial state as a final state if it's connected to one by an epsilon
        if len(set(self.final_states) & self.get_reached_states([self.initial_state], '$')):
            self.final_states.append(self.initial_state)
            self.final_states.sort()
        nfa_states = [{} for _ in range(self.num_states)]
        # Iterate over the non-epsilon characters in the alphabet
        for char in self.alphabet - {'$'}:
            for i, state in enumerate(self.states):
                # Get the states where you can get by using epsilon and the current character
                epsilon_reached = self.get_reached_states(self.get_reached_states(state['$'], char), '$')
                # If the traversal is empty, we skip updating the nfa states
                if not len(epsilon_reached):
                    continue
                nfa_states[i][char] = epsilon_reached

        # Update new states in the copy of the current instance
        new_nfa.states = nfa_states

        # Delete the epsilon char as it's not used anymore
        new_nfa.alphabet.remove('$')

        return new_nfa


def read_nfa(filename):
    with open(filename, 'r') as file:
        num_states = int(file.readline())
        num_transitions = int(file.readline())
        alphabet = set()

        states = [{'$': {i}} for i in range(num_states)]
        for _ in range(num_transitions):
            line = file.readline().strip().split()
            from_state = int(line[0])
            to_state = int(line[1])
            char = line[2]
            alphabet.add(char)

            # Create transition function
            if char not in states[from_state]:
                states[from_state][char] = {to_state}
            else:
                states[from_state][char].add(to_state)

        initial_state = int(file.readline())
        file.readline()
        final_states = list(map(int, file.readline().split()))

    return NFA(num_states, alphabet, states, initial_state, final_states)


if __name__ == '__main__':
    files = ['nfa.txt']

    for file in files:
        nfa = read_nfa(file)
        nfa.get_epsilon_closure()

        print(nfa)

        nfa.remove_epsilon()

        print(nfa)
