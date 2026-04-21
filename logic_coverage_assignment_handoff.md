# Logic Coverage Web App Homework Handoff

## Purpose of this document
This file is a complete handoff brief for another coding model or coding agent such as Codex. It explains the class context, the book/topic context, what the homework is asking for, how to interpret the assignment, what to build, what to avoid, what reference repo is most useful, and how to structure the work using test-driven development.

The goal is **not** to blindly copy a classmate's repo. The goal is to build **my own version** of the homework in a way that fits the course and can be explained clearly in class.

---

## Course context
- Course: **Software Testing**
- Main topics recently covered: **graph coverage, logic coverage, input space partitioning / input domain modeling, abstract tests, and TDD-style thinking**
- Book being followed: **Ammann and Offutt, _Introduction to Software Testing_**
- Earlier homework in this class was much simpler and involved writing code for **simple paths and prime paths** in a graph.
- This new homework is harder because it moves from graph structure to **logic coverage criteria** and requires a more careful requirements/testing process.

This matters because the solution should look like a course project based on Ammann/Offutt ideas, not just a random truth-table calculator.

---

## The assignment, in plain English
The homework prompt says the class will implement a **Logic Coverage Web App Tool** based on the **Offutt website specifications**, and the goal is to use a **Test Driven Development approach**.

The stated steps are:

1. Determine Specifications  
2. Input Space  
3. Abstract Tests and corresponding Inputs  
4. Write the app code  
5. Write a short report on how the development process went  
6. Discuss tools in class and move toward one class version

### What that likely means
This is **not just a coding homework**.
It is a mini software-testing process assignment.
The expected deliverables are likely:
- a written specification / requirements section
- an input space model or input partitioning section
- abstract tests created before implementation
- the app implementation
- automated tests
- a short process report about TDD and requirement clarification

---

## Best interpretation of what to build
The safest interpretation is:

> Build a small web app that accepts a Boolean predicate, analyzes it according to logic coverage criteria from Ammann/Offutt, and presents the coverage-related results. Use TDD, so tests should drive the implementation rather than coding everything first.

### Core user story
A user types a predicate such as:
- `a & b`
- `(a & b) | c`
- `a > b`
- `a ^ b`
- `a = b`
- `!(a | b)`

The app should then:
1. validate the expression
2. identify the clauses / variables
3. generate the relevant assignments / truth table
4. compute logic coverage results for one or more criteria
5. show the output clearly in the browser

---

## Important scope judgment
There are two possible scopes:

### Scope A: small version
Only support:
- Predicate Coverage (PC)
- Clause Coverage (CC)
- Combinatorial Coverage (CoC)

### Scope B: Offutt-style logic coverage version
Support:
- Predicate Coverage (PC)
- Clause Coverage (CC)
- Combinatorial Coverage (CoC)
- General Active Clause Coverage (GACC)
- Correlated Active Clause Coverage (CACC)
- Restricted Active Clause Coverage (RACC)
- General Inactive Clause Coverage (GICC)
- Restricted Inactive Clause Coverage (RICC)

### Recommendation
Use **Scope B** unless the professor explicitly said otherwise.

Reason:
- The assignment says this is based on the **Offutt website specifications**.
- Ammann/Offutt logic coverage coverage is not just PC/CC/CoC.
- A simple truth table tool would likely be too shallow if the class has already reached logic coverage in the book.

If time becomes tight, it is okay to implement in stages:
1. parser + truth table
2. PC/CC/CoC
3. active clause criteria
4. inactive clause criteria

---

## Classmate repo analysis

## 1) Kacy's repo
Repo: `https://github.com/kacytran1122/logic-coverage_tool/`

### What it does
- browser-based UI
- takes a Boolean expression
- extracts uppercase variables
- generates all combinations
- evaluates the expression with JavaScript `eval()`
- reports:
  - Predicate Coverage
  - Clause Coverage
  - Combinatorial Coverage
- displays the truth table

### What is useful in Kacy's repo
- simple UI idea
- basic flow: input -> evaluate -> render truth table
- okay as a minimal starting picture of what a web app could look like

### What is weak / likely not enough
- only does PC, CC, CoC
- uses `eval()`, which is fragile and not ideal for a software testing class project
- clause extraction is simplistic
- always generates the full truth table first, so CoC is automatically satisfied by construction
- does not really model the richer Offutt logic coverage criteria
- not a strong example of a true test-first design process

### Conclusion on Kacy
Use only as a **very rough UI idea**. Do **not** use this as the main technical model.

---

## 2) Shuja's repo
Repo: `https://github.com/shuja-waraich-03/Logic_Coverage_App`

### Why this repo is more relevant
Shuja's repo is much closer to what this assignment probably wants. It is structured like a small software project instead of just a browser demo.

### Repo structure
- `app.py` -> Flask web interface
- `logic_coverage.py` -> core logic coverage computations
- `test_logic_coverage.py` -> automated tests
- `templates/` -> HTML UI
- `requirements.txt`

### Logic supported in Shuja's repo
The core engine claims support for these operators:
- `!` = NOT
- `&` or `&&` = AND
- `|` or `||` = OR
- `>` = implication
- `^` = XOR
- `=` = equivalence

### Coverage criteria supported in Shuja's repo
The core engine includes methods for:
- truth table generation
- predicate coverage
- clause coverage
- combinatorial coverage
- GACC
- CACC
- RACC
- GICC
- RICC

### Why it is the better reference
- much closer to Offutt-style logic coverage scope
- separates UI from coverage logic
- includes automated tests
- better fit for a TDD-oriented homework

---

## How my version should be better than Shuja's
Do not just reproduce Shuja's repo. Improve it in the following ways.

### 1) Better requirements documentation
The assignment explicitly asks for:
- specifications
- input space
- abstract tests and corresponding inputs

So the final submission should contain those clearly and separately.

### 2) Make TDD visible
The project should visibly show:
- tests were thought through before implementation
- parser/evaluator tests
- truth-table tests
- criterion-specific tests
- invalid-input tests

### 3) Be clearer about assumptions
State assumptions such as:
- each variable name is a clause
- repeated variable occurrences are allowed or disallowed
- variables are Boolean only
- expressions use these exact operators
- whitespace is ignored
- parentheses are supported

### 4) Improve error handling
The app should give clear messages for:
- empty input
- invalid characters
- malformed expressions
- unbalanced parentheses
- unknown or unsupported syntax

### 5) Avoid unsafe evaluation
Prefer a custom tokenizer + parser + evaluator over `eval()`.

### 6) Keep output deterministic and explainable
Examples:
- list clauses in a stable order
- generate truth-table rows in a predictable order
- return clearly named test pairs for each criterion

### 7) Avoid repeated unnecessary recomputation where possible
If the truth table is generated many times, cache it.
This is not the main grading point, but it makes the implementation cleaner.

### 8) Write a stronger short report
Explain how TDD changed the process, what failed first, and what became clearer because tests were written early.

---

## What the finished project should probably include

## Functional requirements
The app should:
1. accept a Boolean predicate as input
2. validate syntax
3. extract clauses / variables
4. generate the truth table for all clause assignments
5. compute the selected logic coverage criterion
6. display results in a readable browser view
7. handle bad input gracefully

## Minimum criteria to support
At minimum, support:
- PC
- CC
- CoC

## Recommended criteria to support
Strongly recommended:
- PC
- CC
- CoC
- GACC
- CACC
- RACC
- GICC
- RICC

## Suggested UI elements
- text box for predicate input
- criterion dropdown or buttons
- run/analyze button
- error message area
- clauses detected
- truth table output
- criterion-specific result section

---

## Assumptions to state explicitly in the submission
These assumptions should appear in comments, README, or report.

1. Variables represent Boolean clauses.
2. Variable names are identifiers like `a`, `b`, `c`, or `foo` if the parser supports longer names.
3. The supported operators are only the ones documented.
4. Parentheses are supported.
5. Whitespace is ignored.
6. The tool works on propositional logic expressions only.
7. Coverage is computed from the full set of Boolean assignments over detected clauses.
8. If a criterion has no valid pair for a clause, the app should report `None`, `not possible`, or an equivalent clear message.

---

## Input space model
This should be included as part of the homework write-up.

## Input variables
The main input variable is:
- `predicate`: a Boolean expression string entered by the user

Additional state / selection input:
- `coverage_criterion`: which coverage rule the user wants to compute

## Input characteristics and blocks

### A) Predicate validity
- valid predicate
- empty predicate
- invalid character(s)
- mismatched parentheses
- malformed operator usage

### B) Number of clauses
- one clause
- two clauses
- three or more clauses

### C) Operator usage
- only NOT
- AND present
- OR present
- implication present
- XOR present
- equivalence present
- mixed operators
- nested parentheses

### D) Logical behavior of the predicate
- satisfiable, not tautology
- tautology
- contradiction
- predicate where a clause determines the predicate in some assignments
- predicate where a clause is inactive in some assignments

### E) Criterion requested
- PC
- CC
- CoC
- GACC
- CACC
- RACC
- GICC
- RICC

---

## Abstract tests that should exist before coding
These should be written as test ideas first, then implemented as unit tests.

## A) Parsing / evaluation tests
1. single variable evaluates correctly
2. NOT evaluates correctly
3. AND evaluates correctly
4. OR evaluates correctly
5. implication evaluates correctly
6. XOR evaluates correctly
7. equivalence evaluates correctly
8. parentheses override precedence correctly

### Example abstract tests
- Predicate: `a`
  - Input assignment: `a = True`
  - Expected: `True`

- Predicate: `!a`
  - Input assignment: `a = False`
  - Expected: `True`

- Predicate: `a & b`
  - Input assignment: `a = True, b = False`
  - Expected: `False`

- Predicate: `a > b`
  - Input assignment: `a = True, b = False`
  - Expected: `False`

- Predicate: `a = b`
  - Input assignment: `a = True, b = True`
  - Expected: `True`

## B) Truth table tests
1. one clause produces 2 rows
2. two clauses produce 4 rows
3. three clauses produce 8 rows
4. every row has all clause assignments plus the predicate result

## C) Predicate coverage tests
1. predicate with both true and false rows should return one of each
2. tautology should have no false test
3. contradiction should have no true test

## D) Clause coverage tests
1. for each clause, the output should identify at least one row where that clause is true and one where it is false

## E) Active clause criteria tests
For simple predicates such as `a & b` or `a | b`:
1. GACC should produce determining true/false tests for each major clause when possible
2. CACC should ensure the predicate value differs between the two tests
3. RACC should keep minor clauses fixed while major clause flips

## F) Inactive clause criteria tests
For simple predicates such as `a | b`:
1. GICC should produce tests where the major clause does not determine the predicate
2. RICC should keep minor clauses fixed while major clause flips and remains inactive

## G) Invalid input tests
1. empty predicate rejected
2. invalid character rejected
3. bad syntax rejected
4. unmatched parentheses rejected

---

## Suggested implementation strategy
Use TDD in stages.

## Stage 1: project skeleton
Create the files:
- `logic_coverage.py` or `logicCoverage.js`
- `test_logic_coverage.py` or equivalent
- `app.py` + templates, or browser files if using JS only
- `README.md`
- `REPORT.md`

## Stage 2: tokenizer and parser tests first
Write tests for:
- valid tokenization
- invalid token detection
- evaluation of each operator
- parentheses handling

Then implement tokenizer and parser.

## Stage 3: truth table tests first
Write tests for number of rows and row structure.
Then implement truth table generation.

## Stage 4: PC / CC / CoC tests first
Write tests for simple predicates.
Then implement those criteria.

## Stage 5: determination helper
Create a helper concept like:
- a clause determines the predicate for an assignment if flipping that clause changes the predicate value

Write tests around that helper.

## Stage 6: GACC / CACC / RACC
Write simple expected tests on `a & b` and `a | b`.
Then implement.

## Stage 7: GICC / RICC
Write expected tests on cases where a clause can be inactive.
Then implement.

## Stage 8: web UI
Only after the engine is working, connect it to the browser.

This ordering makes the project look like actual TDD instead of UI-first coding.

---

## Recommended tech stack
If there is no language restriction, prefer:
- **Python** for core logic
- **pytest** for tests
- **Flask** for a minimal web UI

Why:
- easier to express unit tests clearly
- easier to separate logic from UI
- easier to show TDD process
- Shuja's repo already gives a useful structure

If the class strongly expects browser-only JavaScript, then still keep the same design idea:
- one module for core logic
- one module for tests
- one file for UI glue

---

## Suggested project structure

```text
logic-coverage-app/
├── app.py
├── logic_coverage.py
├── test_logic_coverage.py
├── requirements.txt
├── README.md
├── REPORT.md
└── templates/
    └── index.html
```

Optional extras:
- `static/style.css`
- `docs/specifications.md`
- `docs/input_space.md`
- `docs/abstract_tests.md`

If the professor wants a single combined report, those docs can be folded into one final report.

---

## Suggested design of core engine
The core engine should probably expose a class like:

```python
class LogicCoverage:
    def __init__(self, predicate: str): ...
    def generate_truth_table(self): ...
    def predicate_coverage(self): ...
    def clause_coverage(self): ...
    def combinatorial_coverage(self): ...
    def gacc(self): ...
    def cacc(self): ...
    def racc(self): ...
    def gicc(self): ...
    def ricc(self): ...
```

### Internal helpers
- tokenizer
- parser / evaluator
- clause extraction
- `_determines(clause, assignment)` helper
- maybe truth table caching

---

## Important conceptual note for the agent / coder
Do not reduce this project to just "print the truth table".

The interesting part is the **coverage criteria**.
The app should help answer questions like:
- which tests satisfy PC?
- which tests satisfy CC?
- what pair of tests satisfies RACC for clause `a`?
- when is a clause inactive?

This is the part that makes it a software testing assignment rather than a Boolean calculator.

---

## Expected report content
The short report should probably answer these questions:

### 1) How development went
- What tests were written first?
- What failed initially?
- Which parts were hardest?

### 2) Did all tests pass initially?
- No, not all tests should pass initially in TDD.
- Mention that parser/evaluator and active clause criteria were the main sources of early failing tests.

### 3) Did TDD improve requirements understanding?
- Yes.
- Example: writing tests forced clarification on supported operators, invalid syntax handling, and what exactly counts as a satisfying test pair for active/inactive clause coverage.

### 4) How is this different from the graph coverage tool?
Suggested answer:
- the graph tool started from node/edge structure and path generation
- this tool starts from expression grammar, operator semantics, truth assignments, and clause-determination logic
- the graph tool was more structural in a graph sense, while this one is more semantic/logical

---

## Concrete quality bar for the final answer / code
The final project should have these properties:

### Must-have
- working parser/evaluator for supported operators
- automated tests
- web app UI
- clear criteria outputs
- short report

### Strongly preferred
- explicit specs section
- explicit input space section
- abstract tests listed clearly
- no use of `eval()`
- clear error messages
- stable output ordering

### Nice to have
- truth table displayed in HTML table
- criterion selection dropdown
- clean formatting of assignments and test pairs
- caching of truth table

---

## Common mistakes to avoid
1. **Only implementing PC/CC/CoC** when the assignment likely expects the fuller Offutt logic coverage family.
2. Using **`eval()`** in JavaScript or Python for expression evaluation.
3. Starting with UI and only later trying to invent tests.
4. Forgetting to define the **input space** and **abstract tests** in writing.
5. Failing to explain the development process in the report.
6. Returning only booleans like `covered = true/false` instead of showing the actual assignments or test pairs.
7. Ignoring malformed input cases.
8. Copying a classmate's repo structure without understanding the logic.

---

## Suggested acceptance checklist
Before calling the homework done, check all of these:

- [ ] I have a written specification section.
- [ ] I have a written input space / partitioning section.
- [ ] I have abstract tests listed before implementation details.
- [ ] I have automated unit tests.
- [ ] The app validates malformed expressions.
- [ ] The app displays clauses and truth table.
- [ ] The app computes PC, CC, and CoC.
- [ ] The app computes GACC, CACC, RACC, GICC, and RICC, or I can justify why the assignment scope is smaller.
- [ ] The report explains how TDD affected development.
- [ ] I can explain the project in class without relying on copied code.

---

## Recommended plan for Codex or another coding agent
Use this as the direct instruction set.

### Task for the coding agent
Build a clean, original logic coverage web app for a Software Testing course based on Ammann and Offutt logic coverage concepts.

### Required deliverables
1. a core logic engine
2. automated tests written in a TDD-friendly structure
3. a small web UI
4. a short report file
5. a README that explains how to run the app and tests

### Constraints
- do not copy classmate code directly
- use Shuja's repo only as a scope/reference model
- produce code that is easy for a student to understand and explain
- prefer clarity over cleverness
- include good comments, but not excessive AI-sounding commentary
- use simple variable names and readable functions
- no `eval()` unless absolutely unavoidable, and if used, clearly explain why (prefer not to use it)

### Suggested implementation order
1. create test file with parser/evaluator tests
2. implement tokenizer and parser
3. add truth-table tests and implementation
4. add PC/CC/CoC tests and implementation
5. add determination helper tests and implementation
6. add GACC/CACC/RACC tests and implementation
7. add GICC/RICC tests and implementation
8. add Flask UI
9. add README and report

### Style requirements
- code should be beginner-readable
- logic functions should be separate from UI code
- test names should clearly state what they check
- outputs should be deterministic
- error messages should be understandable

---

## Optional stronger version
If there is enough time, the project can be made stronger by adding:
- a dropdown to choose which criterion to display
- a section that explains in English why a returned test pair satisfies the criterion
- highlighting rows in the truth table that are selected as satisfying tests
- export or copyable report output

These are nice improvements but are not necessary unless the homework rubric rewards polish.

---

## If there is ambiguity about scope
If later course materials show that only a subset of criteria is required, scale down gracefully.

Recommended fallback order:
1. PC / CC / CoC
2. GACC / CACC / RACC
3. GICC / RICC

But unless the professor said otherwise, assume the full Offutt-style logic coverage family is expected.

---

## Final instruction to any coding assistant
Do not just give me code.
First produce:
1. specifications
2. input space model
3. abstract tests and corresponding concrete inputs

Then generate the code and tests.
Then generate a short process report.

The whole output should look like a real Software Testing assignment submission built with TDD, not like a hacked-together truth table demo.
