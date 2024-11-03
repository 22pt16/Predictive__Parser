
# 🔍 LL(1) Predictive Parser Generator

## 📖 Overview

This project implements an LL(1) Predictive Parser Generator, a powerful tool for compiler design and language processing.
It automates the creation of predictive parsers from context-free grammars, offering a suite of features for grammar analysis and transformation.

## 🎯 Purpose

The primary goals of this project are:

1. To simplify the process of creating LL(1) parsers
2. To provide tools for grammar analysis and transformation
3. To offer an educational resource for understanding parsing techniques

## ✨ Key Features

- **Grammar Transformation**
  - Left Recursion Elimination
  - Common Prefix Removal
- **Set Computation**
  - FIRST and FOLLOW set generation
  - LL(1) Parsing Table construction
- **Parsing Capabilities**
  - Input string validation
  - Error detection and recovery

## 🛠️ How It Works

1. **Grammar Input**: The user provides a context-free grammar.
2. **Grammar Transformation**: The system applies transformations to make the grammar suitable for LL(1) parsing.
3. **Set Computation**: FIRST and FOLLOW sets are generated for all non-terminals.
4. **Table Construction**: An LL(1) parsing table is created based on the computed sets.
5. **Parsing**: The generated parser can validate input strings against the grammar.

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository:
git clone https://github.com/22pt16/Predictive__Parser.git

### Usage

1. Navigate to the Repository
 >> pip install streamlit  
2. Run the main script:
 >> streamlit run streamlit.py



2. Follow the prompts to input your grammar and test strings.

## 📊 Sample Workflow

1. Input a grammar (e.g., `E -> T E' ; E' -> + T E' | ε ; T -> F T' ; T' -> * F T' | ε ; F -> ( E ) | id`)
2. View the transformed grammar
3. Examine the generated FIRST and FOLLOW sets
4. Inspect the LL(1) parsing table
5. Test input strings for validity


⭐ Star this repository if you find it helpful!
