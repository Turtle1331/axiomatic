# [Formal system](https://en.wikipedia.org/wiki/Formal_system)

## Components

- alphabet
  - finite set of symbols
  - includes operators, constants, variables, etc.
  - formulas are strings of symbols
- grammar
  - defines well-formed formulas inductively
- axiom schemas
  - axiom schemas are substitution schemes for generating well-formed formulas
- inference rules
  - theorems are formulas that can be derived from axioms by inference rules
  - theorems can be defined inductively as either substitutions of axiom schemes or applications of inference rules


## Examples

### Intuitionistic implicational propositional calculus

- alphabet: {'A', 'B', 'C', ..., 'Z', 'bot', ' -> ', '(', ')'}
- grammar:
  - constant := 'A' | 'B' | 'C' | ... | 'Z'
  - formula := constant | '(' formula ' -> ' formula ')' 
- axiom schemes:
  - K: (a -> (b -> a)) for well-formed formulas a, b
  - S: ((a -> (b -> c)) -> ((a -> b) -> (a -> c))) for well-formed formulas a, b
- inference rules:
  - modus ponens: (a -> b), a |- b for well-formed formulas a, b
    - i.e. given well-formed formulas a and b, if (a -> b) and a are theorems, then b is a theorem

