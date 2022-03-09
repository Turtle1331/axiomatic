# Axiomatic

Adventures in type checking and automated theorem proving

## Theory

Due to the Curry-Howard correspondence, Hilbert-style proofs in intuitionistic implicational propositional calculus correspond to type inhabitations in SK combinator calculus. Therefore, we can verify constructive proofs in propositional logic using a type checker for SK combinator expressions. Type inference automatically fills in the verbose details of the proof.

See [`formal_system.md`](./notes/formal_system.md) and [`resources.md`](./notes/frmal_system.md) for details.

## Status

- Zeroth-order (propositional) logic
  - SK combinator calculus
    - [x] type checking
    - [ ] type inference
  - Simply typed lambda calculus
    - [ ] type checking
    - [ ] type inference for simply typed lambda calculus
- First-order logic
  - [ ] figure out which decuctive systems/type systems to use
  - [ ] quantification (generics? polymorphism? dependent types?)
  - [ ] Peano arithmetic
- Usability
  - [ ] CLI demo interface
  - [ ] formula parsing
  - [ ] loading proofs from files
  - [ ] importing definitions/proofs

## Catalog

- `first-attempt.py`: tried using Python `typing` for ADT, datatypes got too confusing, abandoned
- `partial-unifier.py`: tried again using Python tuples, ended up making a one-sided unifier, capable of verifying propositional logic proofs, automatic modus ponens types but manual axiom types
- `formula-parser.rs`: started working on a parser for implicational formulas, partially as an exercise in learning how lexers and parsers work
