# Logic Coverage Web App

This is a small web app for the logic coverage homework. It takes a Boolean predicate, builds the truth table, and shows coverage results for:

- Predicate Coverage (PC)
- Clause Coverage (CC)
- Combinatorial Coverage (CoC)
- General Active Clause Coverage (GACC)
- Correlated Active Clause Coverage (CACC)
- Restricted Active Clause Coverage (RACC)
- General Inactive Clause Coverage (GICC)
- Restricted Inactive Clause Coverage (RICC)

## Run

```bash
python -m pip install -r requirements.txt
pytest -q test_logic_coverage.py -p no:cacheprovider
flask --app app run --debug
```

Then open `http://127.0.0.1:5000/`.

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

Precedence used by the parser:

1. `!`
2. `&`
3. `|`
4. `^`
5. `>`
6. `=`

## Files

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

## Notes

1. Variables represent Boolean clauses.
2. Repeated occurrences of the same variable refer to the same clause.
3. The tool works on propositional logic only.
4. Coverage is computed from the full set of Boolean assignments over the detected clauses.
5. If a coverage criterion has no valid pair for a clause, the UI reports that no valid pair exists.

## Assignment docs

- [docs/specifications.md](docs/specifications.md)
- [docs/input_space.md](docs/input_space.md)
- [docs/abstract_tests.md](docs/abstract_tests.md)
- [REPORT.md](REPORT.md)
