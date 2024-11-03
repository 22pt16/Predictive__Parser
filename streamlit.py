import streamlit as st
from graphviz import Digraph
from toc import Grammar, PredictiveParser

def visualize_parse_tree(parse_tree):
    dot = Digraph()
    for parent, children in parse_tree:
        dot.node(parent, parent)
        for child in children:
            dot.node(child, child)
            dot.edge(parent, child)
    return dot

def main():
    st.title("Grammar Parser and Visualizer")

    # Input for grammar
    grammar_input = st.text_area("Enter your grammar (e.g., S->( L )|a; L-> L, S|S):")
    
    if st.button("Validate Grammar"):
        try:
            grammar = Grammar(grammar_input)
            st.success("Grammar is valid!")
            st.session_state.grammar = grammar  # Store grammar in session state
        except Exception as e:
            st.error(f"Invalid grammar format: {str(e)}")

    if 'grammar' in st.session_state:
        grammar = st.session_state.grammar

        # Display initial grammar
        st.subheader("Initial Grammar")
        for lhs, rules in grammar.productions.items():
            st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")

        # Buttons for grammar conversion
        if st.button("Remove Left Recursion"):
            grammar.remove_left_recursion()
            st.success("Left recursion removed!")
            st.subheader("Grammar after Left Recursion Removal")
            for lhs, rules in grammar.productions.items():
                st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")
            st.write("Terminals:", grammar.terminals)
            st.write("Non-terminals:", grammar.non_terminals)

        if st.button("Remove Common Prefixes"):
            grammar.remove_common_prefixes()
            st.success("Common prefixes removed!")
            st.subheader("Grammar after Common Prefix Removal")
            for lhs, rules in grammar.productions.items():
                st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")
            st.write("Terminals:", grammar.terminals)
            st.write("Non-terminals:", grammar.non_terminals)

        if st.button("Compute FIRST"):
            grammar.compute_first()
            st.success("FIRST sets computed!")
            st.subheader("FIRST Sets")
            for symbol, first_set in grammar.first.items():
                st.write(f"FIRST({symbol}) = {first_set}")

        if st.button("Compute FOLLOW"):
            grammar.compute_follow()
            st.success("FOLLOW sets computed!")
            st.subheader("FOLLOW Sets")
            for symbol, follow_set in grammar.follow.items():
                st.write(f"FOLLOW({symbol}) = {follow_set}")

        if st.button("Construct Predictive Table"):
            grammar.construct_predictive_table()
            st.success("Predictive parsing table constructed!")
            st.write("Terminals:", grammar.terminals)
            st.write("Non-terminals:", grammar.non_terminals)
            st.subheader("Predictive Parsing Table")
            for lhs, row in grammar.predictive_table.items():
                for terminal, production in row.items():
                    if production != "nil":
                        st.write(f"M[{lhs}, {terminal}] = {' '.join(production)}")

        # Display terminals and non-terminals
        st.subheader("Terminals and Non-terminals")
        st.write("Terminals:", grammar.terminals)
        st.write("Non-terminals:", grammar.non_terminals)

        #Display Grammar
        st.subheader("Grammar")
        print("\nGrammar:")
        for lhs in grammar.productions:
            rules = grammar.productions[lhs]
            for rule in rules:
                st.write(f"\t{lhs} -> {' '.join(rule)}")
                print(f"\t{lhs} -> {' '.join(rule)}")


        # Input for parsing
        input_string = st.text_input("Enter input string to parse (e.g., ( a , a ) ):")
        
        if st.button("Parse Input"):
            parser = PredictiveParser(grammar)
            result = parser.parse(input_string.split())
            st.write(result)

            # Visualize parse tree
            if hasattr(parser, 'parse_tree') and parser.parse_tree:
                dot = visualize_parse_tree(parser.parse_tree)
                dot.render('parse_tree', format='png', cleanup=True)
                st.image('parse_tree.png')

            # Display stack and input
            st.subheader("Stack and Input during Parsing")
            if hasattr(parser, 'stack'):
                st.write("Final Stack:", parser.stack)
            if hasattr(parser, 'input_string'):
                st.write("Remaining Input:", parser.input_string)

if __name__ == "__main__":
    main()

