# Specifications

The tool takes a propositional predicate and analyzes it using logic coverage criteria from Ammann and Offutt.

## What it should do

1. Accept a Boolean predicate as input.
2. Check for bad input before running analysis.
3. Reject empty input, invalid characters, bad operator usage, and unbalanced parentheses with a clear error.
4. Extract the clauses in a stable order.
5. Generate the full truth table.
6. Evaluate the predicate without using `eval()`.
7. Show results for:
   - PC
   - CC
   - CoC
   - GACC
   - CACC
   - RACC
   - GICC
   - RICC
8. Show when a clause determines the predicate.
9. Show actual tests or test pairs, not just covered / not covered.
10. Display the results in the web page.

## Extra assumptions

1. Output should stay consistent for the same input.
2. Whitespace is ignored.
3. Logic code is separate from UI code.
4. There are automated tests for the main behavior.

## Supported input grammar

- clauses: identifiers beginning with a letter or `_`
- operators:
  - `!`
  - `&` or `&&`
  - `|` or `||`
  - `^`
  - `>`
  - `=`
- grouping: `(` and `)`

## Assumptions

1. Variables are Boolean clauses.
2. Repeated variable names refer to the same clause.
3. The predicate language is propositional only.
4. Coverage is derived from the full truth table over the detected clauses.
5. If a coverage criterion has no valid pair for a clause, the result is reported as not possible for that clause.
