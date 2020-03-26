class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

        self.current_state = self.initial_state

    def __str__(self):
        return f'Total states: {self.states}\n' \
               f'Alphabet: {self.alphabet}\n' \
               f'Transitions: {self.transitions}\n' \
               f'Initial state: {self.initial_state}\n' \
               f'Final states: {self.final_states}\n'

    def is_in_final_state(self):
        return self.current_state in self.final_states

    def check_if_member(self, string):
        step = 0
        queue = [(step, self.initial_state)]

        while queue:
            step, self.current_state = queue.pop(0)

            # Daca se afla intr-o stare finala si a ajuns la pasul final, atunci este acceptat
            if self.is_in_final_state() and step >= len(string):
                return True

            # Verificam daca incearca sa faca un pas care ar rezulta intr-o eroare
            if step >= len(string):
                continue

            # Adaugam la coada urmatoarele stari de parcurs
            for state in self.transitions.get(self.current_state, {}).get(string[step], []):
                queue.append((step + 1, state))

        # Daca nu a returnat niciodata True, inseamna ca nu a fost acceptat
        return False

    def generate_solutions(self, n):
        queue = [('', self.initial_state)]
        solutions = []

        while queue:
            # Daca avem destule solutii sau intra intr-o bulca infinita, iesim si returnam
            if len(solutions) >= n or len(queue) >= n * 10:
                break

            word, self.current_state = queue.pop(0)

            # Daca am gasit un cuvant care se afla intr-o stare finala si nu e duplicat, il adaugam la solutii
            if self.is_in_final_state() and word not in solutions:
                solutions.append(word)

            # Adaugam la coada urmatoarele stari de parcurs
            for char, states in self.transitions.get(self.current_state, {}).items():
                for state in states:
                    queue.append((word + char, state))

        return solutions


def read_nfa(filename):
    with open(filename, 'r') as file:
        states = int(file.readline())
        num_transitions = int(file.readline())

        transitions = {}
        for _ in range(num_transitions):
            line = file.readline().strip().split()
            from_state = int(line[0])
            to_state = int(line[1])
            char = line[2]

            # Cream functia de tranzitie
            chars = transitions.get(from_state, {}).get(char, [])
            transitions[from_state] = {**transitions.get(from_state, {}), char: [*chars, to_state]}

        initial_state = int(file.readline())
        file.readline()  # Nu avem nevoie de numarul de stari finale in python, deci trecem peste
        final_states = list(map(int, file.readline().split()))

        num_tests = int(file.readline())
        tests = []
        for _ in range(num_tests):
            tests.append(file.readline().strip())

    # Cream o instanta a obiectului NFA
    return NFA(states, '', transitions, initial_state, final_states), tests


if __name__ == '__main__':
    files = ['nfa1.txt', 'nfa2.txt', 'nfa3.txt', 'nfa4.txt']  # Pentru noi teste doar trebuie adaugat un nou fisier / editat unul deja existent

    for file in files:
        nfa, tests = read_nfa(file)

        # print(nfa)

        # Subpunctul a) si b)
        print(file)
        for test in tests:
            print(1 if nfa.check_if_member(test) else 0)

        # Subpunctul c)
        print(nfa.generate_solutions(100), '\n')
