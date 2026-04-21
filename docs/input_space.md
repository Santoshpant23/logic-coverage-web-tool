# Input Space Model

## Primary input variables

- `predicate`: Boolean expression entered by the user
- `coverage_criterion`: the criterion highlighted in the UI

## Input characteristics and partitions

### A. Predicate validity

- valid predicate
- empty predicate
- invalid character present
- malformed operator usage
- mismatched parentheses

### B. Number of clauses

- one clause
- two clauses
- three or more clauses

### C. Operator usage

- only NOT
- includes AND
- includes OR
- includes implication
- includes XOR
- includes equivalence
- mixed operators
- nested parentheses

### D. Logical behavior

- satisfiable but not tautology
- tautology
- contradiction
- clause determines the predicate in some rows
- clause is inactive in some rows

### E. Criterion requested

- PC
- CC
- CoC
- GACC
- CACC
- RACC
- GICC
- RICC

## Risk-focused input notes

- Tautologies and contradictions are important because they create partial predicate coverage behavior.
- Mixed operators are important because precedence bugs are easy to introduce.
- Inactive-clause criteria require predicates where a clause can flip without changing the predicate.
- Larger clause counts matter because pair generation grows quickly with the truth-table size.
