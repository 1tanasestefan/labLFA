FILE_PATH = 'pda.txt' 

states = []
input_alphabet = []
stack_alphabet = []
ending_states = []
rules = {}
starting_state = ''
start_stack_symbol = ''

def define_pda(file_path):
    global states, input_alphabet, stack_alphabet, rules, starting_state, start_stack_symbol, ending_states

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{file_path}' nu a fost gasit.")
        return

    index = 0
    while index < len(lines):
        line = lines[index].strip()

        if not line or line.startswith('#'):
            index += 1
            continue

        if "[States]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            states = [s.strip() for s in lines[index].strip().split(',')]
        elif "[InputAlphabet]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            input_alphabet = [s.strip() for s in lines[index].strip().split(',')]
        elif "[StackAlphabet]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            stack_alphabet = [s.strip() for s in lines[index].strip().split(',')]
        elif "[StartingState]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            starting_state = lines[index].strip()
        elif "[StartStackSymbol]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            start_stack_symbol = lines[index].strip()
        elif "[EndingStates]" in line:
            index += 1
            while lines[index].strip().startswith('#') or not lines[index].strip():
                index += 1
            ending_states = [s.strip() for s in lines[index].strip().split(',')]
        elif "[Rules]" in line:
            index += 1
            while "END" not in lines[index]:
                if lines[index].strip().startswith('#') or not lines[index].strip():
                    index += 1
                    continue
                
                parts = [p.strip() for p in lines[index].strip().split(',')]
                if len(parts) == 5:
                    state, in_symbol, stack_top, next_state, push_symbols = parts
                    
                    rule_key = (state, in_symbol, stack_top)
                    if rule_key not in rules:
                        rules[rule_key] = []
                    
                    rules[rule_key].append((next_state, push_symbols))
                
                index += 1
        
        index += 1

def apply_pda(input_str):
    visited = set()

    def check_path(current_state, input_index, stack):
        
        if input_index == len(input_str) and current_state in ending_states:
            return True

        config = (current_state, input_index, tuple(stack))
        if config in visited:
            return False
        visited.add(config)

        if input_index < len(input_str):
            current_symbol = input_str[input_index]
            stack_top = stack[-1] if stack else ''
            
            key = (current_state, current_symbol, stack_top)
            if key in rules:
                for next_state, push_symbols in rules[key]:
                    new_stack = stack[:-1] # Pop
                    if push_symbols != 'e':
                        for char in reversed(push_symbols):
                            new_stack.append(char)
                    
                    print(f"({current_state}, {input_str[input_index:]}, {''.join(stack)}) -> ({next_state}, {input_str[input_index+1:]}, {''.join(new_stack)})")
                    if check_path(next_state, input_index + 1, list(new_stack)):
                        return True

        stack_top = stack[-1] if stack else ''
        key = (current_state, 'e', stack_top)
        if key in rules:
            for next_state, push_symbols in rules[key]:
                new_stack = stack[:-1] # Pop
                if push_symbols != 'e':
                    for char in reversed(push_symbols):
                        new_stack.append(char)
                
                print(f"({current_state}, {input_str[input_index:]}, {''.join(stack)}) -> Epsilon -> ({next_state}, {input_str[input_index:]}, {''.join(new_stack)})")
                if check_path(next_state, input_index, list(new_stack)):
                    return True

        return False

    initial_stack = [start_stack_symbol]
    is_accepted = check_path(starting_state, 0, initial_stack)

    if is_accepted:
        print(f"\nCuvantul '{input_str}' este ACCEPTAT.")
    else:
        print(f"\nCuvantul '{input_str}' este RESPINS.")

define_pda(FILE_PATH)

print("--- PDA Definition Loaded ---")
print(f"States: {states}")
print(f"Starting State: {starting_state}")
print(f"Ending States: {ending_states}")
print(f"Rules: {rules}")
print("---------------------------\n")


user_input = input("Introduceti cuvantul de testat: ")
apply_pda(user_input)