# Specifications

## Purpose

The tool accepts a propositional predicate and analyzes it using logic coverage criteria from the Ammann and Offutt software testing material.

## Functional requirements

1. The system shall accept a Boolean predicate as a text input.
2. The system shall validate syntax before running any coverage analysis.
3. The system shall reject empty input, invalid characters, malformed operator use, and unbalanced parentheses with a clear message.
4. The system shall extract clauses in deterministic order.
5. The system shall generate the full truth table for the predicate.
6. The system shall evaluate the predicate without using `eval()`.
7. The system shall report:
   - Predicate Coverage (PC)
   - Clause Coverage (CC)
   - Combinatorial Coverage (CoC)
   - General Active Clause Coverage (GACC)
   - Correlated Active Clause Coverage (CACC)
   - Restricted Active Clause Coverage (RACC)
   - General Inactive Clause Coverage (GICC)
   - Restricted Inactive Clause Coverage (RICC)
8. The system shall identify when a clause determines the predicate for a specific assignment.
9. The system shall display concrete tests or independence pairs rather than only returning covered/not-covered flags.
10. The system shall present results in a browser-friendly format.

## Non-functional requirements

1. Output shall be deterministic and stable for the same input.
2. The parser shall ignore whitespace.
3. The implementation shall separate analysis logic from UI code.
4. The project shall include automated tests that demonstrate the TDD process.

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
