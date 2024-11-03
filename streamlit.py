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
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Validate Grammar"):
            try:
                # Create grammar instance
                grammar = Grammar(grammar_input)
                
                # Basic validation
                if not grammar.productions:
                    st.error("Empty or invalid grammar!")
                    return

                # Check if grammar is properly formed
                valid = True
                validation_messages = []

                # Check if all non-terminals have productions
                for nt in grammar.non_terminals:
                    if nt not in grammar.productions:
                        valid = False
                        validation_messages.append(f"Non-terminal {nt} has no productions")

                if valid:
                    st.success("Grammar is valid for LL(1) parsing!")
                    st.session_state.grammar = grammar  # Store grammar in session state
                    
                    # Show validation details
                    with st.expander("See Validation Details"):
                        st.write("Terminals:", grammar.terminals)
                        st.write("Non-terminals:", grammar.non_terminals)
                        st.write("Productions:", grammar.productions)
                else:
                    st.error("Grammar Validation Failed:")
                    for msg in validation_messages:
                        st.write(f"- {msg}")
                    
            except Exception as e:
                st.error(f"Error during grammar validation: {str(e)}")
    
    with col2:
        if st.button("Continue with Grammar"):
            try:
                grammar = Grammar(grammar_input)
                st.session_state.grammar = grammar
                st.success("Proceeding with the grammar processing.")
            except Exception as e:
                st.error(f"Error processing grammar: {str(e)}")

    if 'grammar' in st.session_state:
        grammar = st.session_state.grammar

        # Display initial grammar
        st.subheader("Initial Grammar")
        for lhs, rules in grammar.productions.items():
            st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")

        # Create tabs for different operations
        tab1, tab2, tab3 = st.tabs(["Grammar Transformations", "Sets Computation", "Parsing"])

        with tab1:
            # Buttons for grammar conversion
            if st.button("Remove Left Recursion"):
                grammar.remove_left_recursion()
                st.success("Left recursion removed!")
                st.subheader("Grammar after Left Recursion Removal")
                for lhs, rules in grammar.productions.items():
                    st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")

            if st.button("Remove Common Prefixes"):
                grammar.remove_common_prefixes()
                st.success("Common prefixes removed!")
                st.subheader("Grammar after Common Prefix Removal")
                for lhs, rules in grammar.productions.items():
                    st.write(f"{lhs} -> {' | '.join([' '.join(rule) for rule in rules])}")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Compute FIRST"):
                    grammar.compute_first()
                    st.success("FIRST sets computed!")
                    st.subheader("FIRST Sets")
                    for symbol, first_set in grammar.first.items():
                        st.write(f"FIRST({symbol}) = {first_set}")

            with col2:
                if st.button("Compute FOLLOW"):
                    grammar.compute_follow()
                    st.success("FOLLOW sets computed!")
                    st.subheader("FOLLOW Sets")
                    for symbol, follow_set in grammar.follow.items():
                        st.write(f"FOLLOW({symbol}) = {follow_set}")

            if st.button("Construct Predictive Table"):
                grammar.construct_predictive_table()
                st.success("Predictive parsing table constructed!")
                st.subheader("Predictive Parsing Table")
                
                # Create a dataframe for better visualization
                terminals = sorted(grammar.terminals)
                table_data = []
                for lhs in grammar.predictive_table:
                    row = [lhs]
                    for terminal in terminals:
                        production = grammar.predictive_table[lhs].get(terminal, "nil")
                        if isinstance(production, list):
                            production = ' '.join(production)
                        row.append(production)
                    table_data.append(row)
                
                # Display the table
                st.table([['Non-terminal'] + terminals] + table_data)

        with tab3:
            # Input for parsing
            input_string = st.text_input("Enter input string to parse (e.g., ( a , a ) ):")
            
            if st.button("Parse Input"):
                if input_string.strip():
                    parser = PredictiveParser(grammar)
                    result = parser.parse(input_string.split())
                    st.write("Parsing Result:", result)

                    # Display parsing steps
                    if hasattr(parser, 'stack'):
                        st.write("Final Stack:", parser.stack)
                    if hasattr(parser, 'input_string'):
                        st.write("Remaining Input:", parser.input_string)
                else:
                    st.warning("Please enter an input string to parse.")

if __name__ == "__main__":
    main()