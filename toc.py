class Grammar:
    def __init__(self, productions):
        self.productions = self.parse_productions(productions)
        self.first = {}
        self.follow = {}
        self.predictive_table = {}
        self.start_symbol = list(self.productions.keys())[0]
        self.terminals = set()  # Set for terminals
        self.non_terminals = set(self.productions.keys())  # Set for non-terminals
        
        # Determine terminals
        self.determine_terminals()
        self.print_terminals_and_non_terminals()

    def determine_terminals(self):
        for lhs, rules in self.productions.items():
            for rule in rules:
                for symbol in rule:
                    if symbol not in self.non_terminals and symbol !="'":
                        self.terminals.add(symbol)
        self.terminals.add('$')  # Add '$' explicitly

    def print_terminals_and_non_terminals(self):
        print("Terminals:", self.terminals)
        print("Non-terminals:", self.non_terminals)
        
    def parse_productions(self, productions):
        rules = {}
        for production in productions.split(";"):
            production = production.strip()
            print(production)
            if "->" not in production:
                continue

            lhs, rhs = production.split("->")
            lhs = lhs.strip()
            rhs = rhs.strip().split("|")

            rules[lhs] = [r.strip().split() for r in rhs if r.strip()]

        print("\nRules:")
        for i in rules:
            print(f"\tRule for {i}:")
            for j, rule in enumerate(rules[i]):
                print(f"\t  {j+1}. {i} -> {' '.join(rule)}")
            print()
        return rules

    def remove_left_recursion(self):
        new_rules = {}
    
        for lhs in self.productions:
            rules = self.productions[lhs]
            alpha = []
            beta = []
    
            # Separate rules into alpha and beta
            for rule in rules:
                
                if rule[0][0] == lhs:  # Check for left recursion
                    #print("found",rule)
                    a=rule[0][1:]
                    #print("a=",a)
                    alpha.append(a)  # Add to alpha if left recursive
                    #print("alpha=",alpha)
                   
                else:
                    beta.append(rule)  # Add to beta otherwise
    
            # If left recursion exists
            if alpha:
                new_non_terminal = f"{lhs}'"
                new_rules[lhs] = [b + [new_non_terminal] for b in beta]
             
                stri=""
                for a in alpha:
                    stri += f"{a}"
              #  print("String:",stri)
                stri+= f"{new_non_terminal}"
                new_rules[new_non_terminal] =  [stri]+ [['ε']]
            else:
                new_rules[lhs] = rules  # No left recursion, keep original rules
        
        self.productions = new_rules
    
        # Print updated rules
        print("\nRemoved Left Recursion New Rules:")
       
        for lhs in self.productions:
            rules = self.productions[lhs]
            for rule in rules:
                print(f"\t{lhs} -> {' '.join(rule)}")
        self.non_terminals = set(self.productions.keys())  # Update non-terminals
        self.determine_terminals()  # Recalculate terminals
        self.print_terminals_and_non_terminals()  # Print updated sets



    def remove_common_prefixes(self):
        new_rules = {}
        for lhs in self.productions:
            rules = self.productions[lhs]
            prefixes = {}
            
            
            for rule in rules:
                prefix = tuple(rule)  # Convert the list to a tuple
                if prefix not in prefixes:
                    prefixes[prefix] = []
                prefixes[prefix].append(rule)
                
            new_rules[lhs] = []
    
            for prefix, grouped_rules in prefixes.items():
                if len(grouped_rules) > 1:
                    new_non_terminal = f"{lhs}'"
                    new_rules[lhs] = [list(prefix)]  # Common prefix rule
                    new_rules[new_non_terminal] = [r[len(prefix):] for r in grouped_rules]
                else:
                    new_rules[lhs].append(grouped_rules[0])  # Keep original if no common prefix
    
        print("\nRemoved Common Prefixes New Rules:")
        """for i in new_rules:
            print(f"\tRule for {i}:")
            for j, rule in enumerate(new_rules[i]):
                print(f"\t  {j+1}. {i} -> {' '.join(rule)}")
            print()"""
        for lhs in self.productions:
            rules = self.productions[lhs]
            for rule in rules:
                print(f"\t{lhs} -> {' '.join(rule)}")
       
            
        self.productions = new_rules
        self.non_terminals = set(self.productions.keys())  # Update non-terminals
        self.determine_terminals()  # Recalculate terminals
        self.print_terminals_and_non_terminals()  # Print updated sets


    def compute_first(self):
        print("FIRST of Nonterm:")
        
        for symbol in self.productions:
            self.first[symbol] = set()  # Initialize the set for the non-terminal

        changed = True
        while changed:
            changed = False
            for symbol in self.productions:
                for production in self.productions[symbol]:
                    before_update = len(self.first[symbol])  # Initialize before_update here
                    for sym in production:
                        if sym in self.productions:  # Non-terminal
                            self.first[symbol].update(self.first[sym] - {'ε'})
                            if 'ε' not in self.first[sym]:
                                break  # Stop if we found a terminal or a non-terminal without ε
                        else:  # Terminal
                            self.first[symbol].add(sym)
                            break
                    else:
                        # If we reached here, it means all symbols were nullable
                        self.first[symbol].add('ε')
                    
                    # Check if the FIRST set has changed
                    if len(self.first[symbol]) > before_update:
                        changed = True

        # Print FIRST sets for debugging
        for symbol in self.productions:
            print(symbol, ":", self.first[symbol])
                

   
    def compute_follow(self):
        print("\nFOLLOW of Nonterm:")
        for symbol in self.productions:
            self.follow[symbol] = set()  # Initialize empty FOLLOW set
    
        # Add end marker ($) to the FOLLOW set of the start symbol
        self.follow[self.start_symbol].add('$')
    
        changed = True
        while changed:
            changed = False
    
            for lhs in self.productions:
                for production in self.productions[lhs]:
                    for i in range(len(production)):
                        current_symbol = production[i]
                        if current_symbol in self.productions:  # Check if the symbol is a non-terminal
                            if i + 1 < len(production):  # There is a symbol after the current non-terminal
                                next_sym = production[i + 1]  # Get the next symbol
    
                                # Rule 1: If A -> pBq, then FOLLOW(B) = FIRST(q) except ε
                                if next_sym in self.productions:  # If next symbol is a non-terminal
                                    new_follow = self.first[next_sym] - {'ε'}
    
                                    if 'ε' in self.first[next_sym]:
                                        new_follow.update(self.follow[lhs])
    
                                    if new_follow - self.follow[current_symbol]:
                                        self.follow[current_symbol].update(new_follow)
                                        changed = True
    
                                else:  # Next symbol is a terminal
                                    if next_sym not in self.follow[current_symbol] and next_sym != "'":  # Add terminal to FOLLOW(B)
                                        self.follow[current_symbol].add(next_sym)
                                        changed = True
                            else:  # If it's the last symbol in the production
                                # Rule 2: If A -> pB, then FOLLOW(A) = FOLLOW(B)
                                if self.follow[lhs] - self.follow[production[i]]:
                                    self.follow[current_symbol].update(self.follow[lhs])
                                    changed = True
    
                        # Check for situations where we should add a specific terminal to FOLLOW(current_symbol)
                        if i < len(production) - 1 and production[i + 1] == ')':
                            self.follow[current_symbol].add(')')
    
        # Print FOLLOW sets for debugging
        for symbol in self.productions:
            print(symbol, ":", self.follow[symbol])
            
        self.print_terminals_and_non_terminals()  # Print updated sets


    def compute_first_for_production(self, production): #for predictve table purpose
        first_set = set()
        for sym in production:
            if sym in self.productions:  # Non-terminal
                first_set.update(self.first[sym])
                if 'ε' not in self.first[sym]:
                    break
            else:  # Terminal
                first_set.add(sym)
                break
        else:
            first_set.add('ε')  # If all symbols are nullable
        return first_set
    
    def construct_predictive_table(self):
        print("Constructing Predictive Parsing Table:\n")
        # Initialize the predictive table
        self.predictive_table = {lhs: {terminal: "nil" for terminal in self.terminals} for lhs in self.productions}
        
    
        for lhs in self.productions:
            for production in self.productions[lhs]:
                first_set = self.compute_first_for_production(production)  # Compute FIRST for the right-hand side
                print(production, first_set)
    
                # Rule 1: Fill in the table using FIRST
                for terminal in first_set:
                    # if terminal != 'ε':  # Exclude ε
                    self.predictive_table[lhs][terminal] = production
    
                # Rule 2: Handle ε in FIRST and fill with FOLLOW
                if 'ε' in first_set:
                    for terminal in self.follow[lhs]:
                        self.predictive_table[lhs][terminal] = production
                    
                    # Include $ if it's in the FOLLOW set
                    if '$' in self.follow[lhs]:
                        self.predictive_table[lhs]['$'] = production
    
        # Formatted output of the predictive parsing table and Grammar
       
        print("\nPredictive Parsing Table:")
        terminals = sorted(self.terminals)  # Make sure to use the full set of terminals
        
        # Print header
        print("   ", end="")
        for terminal in (terminals ):
            print(f"{terminal:>10}", end="")
        print()
    
        # Print table contents
        for lhs in self.predictive_table:
            print(f"{lhs:>2}:", end="")
            for terminal in terminals:
                production = self.predictive_table[lhs].get(terminal, "nil")  # Default to "nil" if no production
                production_str = ' '.join(production) if isinstance(production, list) else production
                print(f"{production_str:>10}", end="")
            print()

  

class PredictiveParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.stack = []
        self.input_string = []
        
    def handle_error(self, top):
        print(f"\nError: No rule for {top} with input '{self.input_string[0]}'.")
        self.panic_mode_recovery()  # Call panic mode recovery

    def panic_mode_recovery(self):
        while self.input_string and self.input_string[0] not in self.grammar.follow[self.stack[-1]]:
            print(f"Skipping: {self.input_string[0]}")
            self.input_string.pop(0)  # Skip the current input symbol

    def parse(self, input_string):
        #The input string to parse:
        print("\nParsing : ",end="")
        print(' '.join(input_string))
            
            
            
        self.stack = [self.grammar.start_symbol] # Add end marker to stack
        self.input_string = input_string + ['$']  # Add end marker

        while self.stack:
            top = self.stack.pop()
            print(f"\n*Stack: {''.join(self.stack)}\t Input: {''.join(self.input_string)}\t Top: {top}")

            #Empty string
            if top == '$' and self.input_string[0] == '$':
                return "Input parsed successfully."
        
            # Just remove epsilon from stack
            if top == 'ε':  
                continue

            # Case: Non-terminal
            if top in self.grammar.productions: 
                current_input = self.input_string[0]
                if current_input in self.grammar.predictive_table[top]:
                    production = self.grammar.predictive_table[top][current_input]
                    if production == "nil":
                        return f"\nError: No production for {top} with input '{current_input}'"

                    print("\n>>Production found",production)
                    if production != ['ε']:
                        self.stack.extend(reversed(production))  # Push production to stack
                    # print(f"\n*Stack: {''.join(self.stack)}\t Input: {''.join(self.input_string)}\t Top: {top}")
                else:
                    return f"\nError: No rule for {top} with input '{current_input}'"
                
             # Case: Terminal Match - cancels out
            elif top == self.input_string[0]: 
                print("\n>>Match found ", top)
                self.input_string.pop(0)
                
            else:
                return f"\nError: Expected '{top}', found '{self.input_string[0]}'"

        return "Input not fully consumed." if self.input_string[0] != '$' else "Input parsed successfully."


# Example usage

print("Given Grammar: ")
prod = "S->( L )|a; L-> L, S|S"   #Take care of Input method always!

grammar = Grammar(prod)
grammar.remove_left_recursion() #DONE
grammar.remove_common_prefixes()    #DONE

grammar.compute_first() #DONE
grammar.compute_follow()    #DONE 
grammar.construct_predictive_table()    #DONE 

input_string = ["(", "a", ",", "a", ")"]

parser = PredictiveParser(grammar)
result = parser.parse(input_string)     #DONE
print(result)


"""
E -> T E';
E' -> + T E' | ε                ;
T -> F T';
T' -> * F T' | ε ;
F -> i | ( E );
"""    