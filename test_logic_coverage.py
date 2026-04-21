import pytest

from logic_coverage import LogicCoverage, LogicCoverageError, tokenize


def test_tokenizer_normalizes_multi_character_operators():
    tokens = tokenize("a && b || !c")
    assert [token.kind for token in tokens] == ["IDENT", "AND", "IDENT", "OR", "NOT", "IDENT"]


@pytest.mark.parametrize(
    ("predicate", "assignment", "expected"),
    [
        ("a", {"a": True}, True),
        ("!a", {"a": False}, True),
        ("a & b", {"a": True, "b": False}, False),
        ("a | b", {"a": False, "b": True}, True),
        ("a > b", {"a": True, "b": False}, False),
        ("a ^ b", {"a": True, "b": False}, True),
        ("a = b", {"a": True, "b": True}, True),
        ("!(a | b)", {"a": False, "b": False}, True),
        ("a & b | c", {"a": True, "b": True, "c": False}, True),
        ("a & (b | c)", {"a": True, "b": False, "c": True}, True),
    ],
)
def test_predicate_evaluation(predicate, assignment, expected):
    assert LogicCoverage(predicate).evaluate(assignment) is expected


def test_clause_order_is_first_appearance_stable():
    coverage = LogicCoverage("(z & a) | z | b")
    assert coverage.clauses == ["z", "a", "b"]


@pytest.mark.parametrize(
    "predicate",
    ["", "   ", "a % b", "(a & b", "a & & b", ")a("],
)
def test_invalid_predicates_raise_clear_errors(predicate):
    with pytest.raises(LogicCoverageError):
        LogicCoverage(predicate)


def test_truth_table_row_counts_match_clause_count():
    assert len(LogicCoverage("a").generate_truth_table()) == 2
    assert len(LogicCoverage("a & b").generate_truth_table()) == 4
    assert len(LogicCoverage("a & b & c").generate_truth_table()) == 8


def test_truth_table_rows_include_assignments_and_result():
    row = LogicCoverage("a > b").generate_truth_table()[0]
    assert set(row) == {"id", "assignment", "result"}
    assert set(row["assignment"]) == {"a", "b"}


def test_predicate_coverage_handles_regular_tautology_and_contradiction():
    regular = LogicCoverage("a & b").predicate_coverage()
    tautology = LogicCoverage("a | !a").predicate_coverage()
    contradiction = LogicCoverage("a & !a").predicate_coverage()

    assert regular["satisfied"] is True
    assert tautology["satisfied"] is False
    assert contradiction["satisfied"] is False
    assert len(regular["selected_tests"]) == 2
    assert len(tautology["selected_tests"]) == 1
    assert len(contradiction["selected_tests"]) == 1


def test_clause_coverage_selects_rows_that_cover_true_and_false_for_each_clause():
    result = LogicCoverage("a & b").clause_coverage()

    assert result["satisfied"] is True
    assert len(result["selected_tests"]) >= 2
    assert result["by_clause"]["a"]["true_test"] is not None
    assert result["by_clause"]["a"]["false_test"] is not None
    assert result["by_clause"]["b"]["true_test"] is not None
    assert result["by_clause"]["b"]["false_test"] is not None


def test_combinatorial_coverage_returns_the_full_truth_table():
    coverage = LogicCoverage("a ^ b").combinatorial_coverage()
    assert coverage["satisfied"] is True
    assert coverage["row_count"] == 4
    assert len(coverage["selected_tests"]) == 4


def test_determines_identifies_when_a_clause_changes_the_predicate():
    coverage = LogicCoverage("a & b")
    assert coverage.determines("a", {"a": True, "b": True}) is True
    assert coverage.determines("a", {"a": False, "b": False}) is False


def test_active_clause_criteria_return_expected_pairs_for_simple_and():
    coverage = LogicCoverage("a & b")

    gacc = coverage.gacc()["by_clause"]["a"]
    cacc = coverage.cacc()["by_clause"]["a"]
    racc = coverage.racc()["by_clause"]["a"]

    assert gacc["satisfied"] is True
    assert cacc["satisfied"] is True
    assert racc["satisfied"] is True

    cacc_pair = cacc["representative_pair"]
    racc_pair = racc["representative_pair"]

    assert cacc_pair["major_false"]["result"] != cacc_pair["major_true"]["result"]
    assert racc_pair["minor_clauses_fixed"] is True
    assert racc_pair["major_false"]["assignment"]["b"] == racc_pair["major_true"]["assignment"]["b"]


def test_inactive_clause_criteria_return_expected_pairs_for_simple_or():
    coverage = LogicCoverage("a | b")

    gicc = coverage.gicc()["by_clause"]["a"]
    ricc = coverage.ricc()["by_clause"]["a"]

    assert gicc["satisfied"] is True
    assert ricc["satisfied"] is True

    pair = ricc["representative_pair"]
    assert pair["major_false"]["result"] == pair["major_true"]["result"]
    assert pair["minor_clauses_fixed"] is True
    assert pair["major_false"]["assignment"]["b"] == pair["major_true"]["assignment"]["b"] == True


def test_analyze_builds_complete_summary():
    analysis = LogicCoverage("(a & b) | c").analyze("RACC")

    assert analysis["focus_criterion"] == "RACC"
    assert analysis["row_count"] == 8
    assert set(analysis["criteria_results"]) == {
        "PC",
        "CC",
        "CoC",
        "GACC",
        "CACC",
        "RACC",
        "GICC",
        "RICC",
    }
