FILE = 'D:/afacultate/An I Sem II/Limbaje Formale si Automate/Laboratoare/lfa.txt'
f = open(FILE, 'r')
lines = f.readlines()

states = inpt = sigma = endingStates = []
rules = {}
startingState = 0

def defineDFA():
    global states, inpt, rules, startingState, endingStates
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
                while lines[index][0] in "#/@\n":
                    index += 1
                if lines[index][0] not in "#/@\n":
                    line = lines[index].strip().split(', ')
                    state, symbol, nextState = line

                    if state not in states and state not in endingStates:
                        print(f"Warning: State '{state}' in rules is not defined in [PassingStates] or [EndingStates]")

                    if state not in rules:
                        rules[state] = {symbol: nextState}
                    else:
                        rules[state][symbol] = nextState
                
                index += 1

        index += 1
    
    startingState = states[0]

def applyDFA(state, depth=0):
    while depth < len(inpt):
        currentRule = inpt[depth]

        while state not in rules or currentRule not in rules[state]:
            if currentRule not in rules[state]:
                print(f"No such rule as {currentRule} for state {state}")
            if state not in rules:
                print(f"No such {state} in defined states")
            depth += 1
            if depth >= len(inpt): 
                break
            currentRule = inpt[depth]

        if depth >= len(inpt):
            break  

        nextState = rules[state][currentRule]
        if nextState not in states and nextState not in endingStates:
            print(f"Cannot pass to {nextState} (not defined)")
            depth += 1
        else:
            print(f"{state} -> {nextState}")
            state = nextState
            depth += 1

    if state in endingStates:
        print(f'Accepted (ended in {state})')
    else:
        print(f'Rejected (ended in {state})')

defineDFA()
inpt = input().split()
applyDFA(startingState)
