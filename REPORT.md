# Short Report

I started this homework from the tests instead of from the UI. First I wrote tests for parsing and evaluating predicates, then tests for truth table generation, and after that tests for the coverage criteria. Once the logic was working, I connected it to a small Flask web app.

No, the tests did not pass at first. The first failures were around invalid syntax, operator handling, and the active and inactive clause rules. That helped because it forced me to be more specific about what inputs the tool should accept and what should count as a valid pair of tests.

TDD did improve the requirements process. Writing the tests early made me define the supported operators, precedence, error cases, and how to handle cases where a criterion is not possible for a clause. Without that, it would have been easy to stop at a truth table and miss the actual logic coverage part.

This was different from the graph coverage tool. In the graph assignment, I was working more structurally. I could use DFS to generate simple paths and then identify the prime paths from those results. In this assignment, the harder part was parsing predicates, evaluating Boolean assignments, and checking whether flipping one clause changes the predicate. So this one was less about traversal and more about logic semantics.

The final submission includes the app code, automated tests, the specification section, input space, abstract tests, and this short report.
