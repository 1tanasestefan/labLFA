from collections import deque

FILE = 'nfa.txt'
f = open(FILE, 'r')
lines = f.readlines()

states = []
sigma = []
endingStates = []
rules = {}
startingState = ''
epsilon = 'ε'


def defineNFA():
    global states, rules, startingState, endingStates
    sz = len(lines)
    index = 0

    while index < sz:
        line = lines[index].strip().split(', ')
        if "[PassingStates]" in line:
            index += 1
            while lines[index][0] in "#/@\n":
                index += 1
            states = lines[index].strip().split(', ')
        elif "[EndingStates]" in line:
            index += 1
            while lines[index][0] in "#/@\n":
                index += 1
            endingStates = lines[index].strip().split(', ')
        elif "[Rules]" in line:
            index += 1
            while "END" not in lines[index]:
                if lines[index][0] not in "#/@\n":
                    line = lines[index].strip().split(', ')
                    state, symbol, nextState = line

                    if state not in rules:
                        rules[state] = {}
                    if symbol not in rules[state]:
                        rules[state][symbol] = []
                    rules[state][symbol].append(nextState)
                index += 1
        index += 1

    startingState = states[0]


def get_epsilon_closure(states_set):
    stack = list(states_set)
    closure = set(states_set)

    while stack:
        state = stack.pop()
        if state in rules and epsilon in rules[state]:
            for next_state in rules[state][epsilon]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure


def applyNFA(startState, inpt):
    current_states = get_epsilon_closure([startState])

    for symbol in inpt:
        next_states = set()
        for state in current_states:
            if state in rules and symbol in rules[state]:
                for next_state in rules[state][symbol]:
                    next_states.add(next_state)
        current_states = get_epsilon_closure(next_states)

    if any(state in endingStates for state in current_states):
        print("Accepted")
    else:
        print("Rejected")


defineNFA()
inpt = input("Input string: ").strip()
applyNFA(startingState, inpt)
