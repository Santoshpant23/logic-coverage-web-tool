# Abstract Tests

## A. Parsing and evaluation

1. `a` with `a = True` should be `True`.
2. `!a` with `a = False` should be `True`.
3. `a & b` with `a = True, b = False` should be `False`.
4. `a | b` with `a = False, b = True` should be `True`.
5. `a > b` with `a = True, b = False` should be `False`.
6. `a ^ b` with `a = True, b = False` should be `True`.
7. `a = b` with `a = True, b = True` should be `True`.
8. Parentheses should override precedence.

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

Using a simple predicate such as `a & b`:

1. GACC should find a valid pair for clause `a`.
2. CACC should find a pair where the predicate result changes.
3. RACC should keep the minor clauses fixed.

## F. Inactive clause criteria

Using a simple predicate such as `a | b`:

1. GICC should find a pair where clause `a` flips but the predicate result stays the same.
2. RICC should keep the minor clauses fixed.

## G. Invalid input handling

1. Empty predicate is rejected.
2. Invalid characters are rejected.
3. Bad syntax is rejected.
4. Unmatched parentheses are rejected.
