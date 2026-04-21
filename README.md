# Logic Coverage Web App

This project is a software testing class implementation of a **Logic Coverage Web App Tool** built around the Ammann and Offutt logic coverage criteria. The app parses propositional predicates without using `eval()`, generates a deterministic truth table, and reports concrete tests or independence pairs for:

- Predicate Coverage (PC)
- Clause Coverage (CC)
- Combinatorial Coverage (CoC)
- General Active Clause Coverage (GACC)
- Correlated Active Clause Coverage (CACC)
- Restricted Active Clause Coverage (RACC)
- General Inactive Clause Coverage (GICC)
- Restricted Inactive Clause Coverage (RICC)

## What the tool does

- validates Boolean predicates and reports clear syntax errors
- extracts clauses in stable first-appearance order
- evaluates predicates using a custom tokenizer and parser
- generates the full truth table
- identifies clause determination and inactive rows
- computes representative tests and test pairs for the coverage criteria
- renders the results in a browser-oriented Flask UI

## Supported syntax

- variables: `a`, `b`, `foo`, `clause_1`
- operators:
  - `!` for NOT
  - `&` or `&&` for AND
  - `|` or `||` for OR
  - `^` for XOR
  - `>` for implication
  - `=` for equivalence
- parentheses are supported
- whitespace is ignored

Operator precedence used by the parser is:

1. `!`
2. `&`
3. `|`
4. `^`
5. `>`
6. `=`

## Project structure

```text
app.py
logic_coverage.py
test_logic_coverage.py
requirements.txt
README.md
REPORT.md
docs/
  specifications.md
  input_space.md
  abstract_tests.md
templates/
  index.html
static/
  style.css
```

## Setup

```bash
python -m pip install -r requirements.txt
pytest -q
flask --app app run --debug
```

Then open `http://127.0.0.1:5000/`.

## Assumptions

1. Variables represent Boolean clauses.
2. Repeated occurrences of the same variable refer to the same clause.
3. The tool works on propositional logic only.
4. Coverage is computed from the full set of Boolean assignments over the detected clauses.
5. If a coverage criterion has no valid pair for a clause, the UI reports that no valid pair exists.

## Documentation for the assignment

- [docs/specifications.md](docs/specifications.md)
- [docs/input_space.md](docs/input_space.md)
- [docs/abstract_tests.md](docs/abstract_tests.md)
- [REPORT.md](REPORT.md)

## Mapping to the professor's prompt

1. Determine specifications:
   - [docs/specifications.md](docs/specifications.md)
2. Input space:
   - [docs/input_space.md](docs/input_space.md)
3. Abstract tests and corresponding inputs:
   - [docs/abstract_tests.md](docs/abstract_tests.md)
   - [test_logic_coverage.py](test_logic_coverage.py)
4. Write the app code:
   - [logic_coverage.py](logic_coverage.py)
   - [app.py](app.py)
   - [templates/index.html](templates/index.html)
5. Short report on the development process:
   - [REPORT.md](REPORT.md)
6. Class discussion:
   - not a code deliverable; the repo is prepared for demo and comparison in class
