# Abstract Tests

These test ideas were derived before implementation and then turned into unit tests.

## A. Parsing and evaluation

1. Single variable evaluates correctly.
   - Example: `a` with `a = True` should evaluate to `True`.
2. NOT evaluates correctly.
   - Example: `!a` with `a = False` should evaluate to `True`.
3. AND evaluates correctly.
   - Example: `a & b` with `a = True, b = False` should evaluate to `False`.
4. OR evaluates correctly.
   - Example: `a | b` with `a = False, b = True` should evaluate to `True`.
5. Implication evaluates correctly.
   - Example: `a > b` with `a = True, b = False` should evaluate to `False`.
6. XOR evaluates correctly.
   - Example: `a ^ b` with `a = True, b = False` should evaluate to `True`.
7. Equivalence evaluates correctly.
   - Example: `a = b` with `a = True, b = True` should evaluate to `True`.
8. Parentheses override precedence correctly.
   - Example: `a & (b | c)` should differ from `a & b | c` when assignments make grouping matter.

## B. Truth table

1. One clause produces 2 rows.
2. Two clauses produce 4 rows.
3. Three clauses produce 8 rows.
4. Each row contains all clause assignments and the predicate result.

## C. Predicate coverage

1. A regular predicate should provide one true row and one false row.
2. A tautology should have no false test.
3. A contradiction should have no true test.

## D. Clause coverage

1. Each clause should have at least one selected test where it is true.
2. Each clause should have at least one selected test where it is false.

## E. Active clause criteria

For simple predicates such as `a & b`:

1. GACC should find a valid pair for clause `a`.
2. CACC should find a pair where predicate results differ.
3. RACC should keep minor clauses fixed while the major clause flips.

## F. Inactive clause criteria

For simple predicates such as `a | b`:

1. GICC should find a pair where clause `a` flips but the predicate result stays the same.
2. RICC should keep minor clauses fixed while clause `a` flips and remains inactive.

## G. Invalid input handling

1. Empty predicate is rejected.
2. Invalid characters are rejected.
3. Bad syntax is rejected.
4. Unmatched parentheses are rejected.
