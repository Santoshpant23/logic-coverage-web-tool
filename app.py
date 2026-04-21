from __future__ import annotations

from flask import Flask, render_template, request

from logic_coverage import LogicCoverage, LogicCoverageError


app = Flask(__name__)

SAMPLE_PREDICATES = [
    "a & b",
    "(a & b) | c",
    "!(a | b)",
    "a ^ b",
    "a = b",
    "(a > b) & (!c | a)",
]

CRITERION_DETAILS = {
    "PC": {
        "title": "Predicate Coverage",
        "description": "Finds tests where the predicate is true and false.",
    },
    "CC": {
        "title": "Clause Coverage",
        "description": "Finds tests that make each clause true and false at least once.",
    },
    "CoC": {
        "title": "Combinatorial Coverage",
        "description": "Uses the full truth table over the detected clauses.",
    },
    "GACC": {
        "title": "General Active Clause Coverage",
        "description": "Pairs tests where the major clause determines the predicate.",
    },
    "CACC": {
        "title": "Correlated Active Clause Coverage",
        "description": "Requires the predicate result to differ across the active-clause pair.",
    },
    "RACC": {
        "title": "Restricted Active Clause Coverage",
        "description": "Requires fixed minor clauses while the major clause changes the predicate.",
    },
    "GICC": {
        "title": "General Inactive Clause Coverage",
        "description": "Pairs tests where the major clause flips but stays inactive.",
    },
    "RICC": {
        "title": "Restricted Inactive Clause Coverage",
        "description": "Inactive pairs with fixed minor clauses.",
    },
}


@app.route("/", methods=["GET", "POST"])
def index():
    predicate = request.form.get("predicate", "(a & b) | c").strip()
    focus_criterion = request.form.get("criterion", "RACC")
    error = None

    try:
        analysis = LogicCoverage(predicate).analyze(focus_criterion)
    except LogicCoverageError as exc:
        analysis = None
        error = str(exc)

    return render_template(
        "index.html",
        predicate=predicate,
        analysis=analysis,
        error=error,
        sample_predicates=SAMPLE_PREDICATES,
        criterion_details=CRITERION_DETAILS,
        criterion_options=list(CRITERION_DETAILS.keys()),
        focus_criterion=focus_criterion,
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
