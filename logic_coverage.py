from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any


BOOL_TEXT = {True: "T", False: "F"}


class LogicCoverageError(ValueError):
    """Raised when a predicate cannot be parsed or analyzed."""


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int


class Node:
    def evaluate(self, assignment: dict[str, bool]) -> bool:
        raise NotImplementedError

    def variables(self) -> list[str]:
        raise NotImplementedError


@dataclass(frozen=True)
class Variable(Node):
    name: str

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        return assignment[self.name]

    def variables(self) -> list[str]:
        return [self.name]


@dataclass(frozen=True)
class Not(Node):
    operand: Node

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        return not self.operand.evaluate(assignment)

    def variables(self) -> list[str]:
        return self.operand.variables()


@dataclass(frozen=True)
class Binary(Node):
    operator: str
    left: Node
    right: Node

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        left_value = self.left.evaluate(assignment)
        right_value = self.right.evaluate(assignment)

        if self.operator == "AND":
            return left_value and right_value
        if self.operator == "OR":
            return left_value or right_value
        if self.operator == "XOR":
            return left_value ^ right_value
        if self.operator == "IMPLIES":
            return (not left_value) or right_value
        if self.operator == "EQUIV":
            return left_value == right_value
        raise LogicCoverageError(f"Unsupported operator {self.operator!r}.")

    def variables(self) -> list[str]:
        return self.left.variables() + self.right.variables()


def tokenize(predicate: str) -> list[Token]:
    if not predicate or not predicate.strip():
        raise LogicCoverageError("Predicate cannot be empty.")

    tokens: list[Token] = []
    index = 0

    while index < len(predicate):
        char = predicate[index]

        if char.isspace():
            index += 1
            continue

        if char.isalpha() or char == "_":
            start = index
            index += 1
            while index < len(predicate) and (
                predicate[index].isalnum() or predicate[index] == "_"
            ):
                index += 1
            tokens.append(Token("IDENT", predicate[start:index], start))
            continue

        two_char = predicate[index : index + 2]
        if two_char == "&&":
            tokens.append(Token("AND", "&", index))
            index += 2
            continue
        if two_char == "||":
            tokens.append(Token("OR", "|", index))
            index += 2
            continue

        single_tokens = {
            "!": "NOT",
            "&": "AND",
            "|": "OR",
            "^": "XOR",
            ">": "IMPLIES",
            "=": "EQUIV",
            "(": "LPAREN",
            ")": "RPAREN",
        }
        if char in single_tokens:
            tokens.append(Token(single_tokens[char], char, index))
            index += 1
            continue

        raise LogicCoverageError(
            f"Invalid character {char!r} at position {index}. Supported operators are !, &, |, ^, >, =, and parentheses."
        )

    return tokens


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def parse(self) -> Node:
        expression = self.parse_equivalence()
        if self._peek() is not None:
            token = self._peek()
            raise LogicCoverageError(
                f"Unexpected token {token.value!r} at position {token.position}."
            )
        return expression

    def parse_equivalence(self) -> Node:
        node = self.parse_implication()
        while self._match("EQUIV"):
            node = Binary("EQUIV", node, self.parse_implication())
        return node

    def parse_implication(self) -> Node:
        node = self.parse_xor()
        if self._match("IMPLIES"):
            node = Binary("IMPLIES", node, self.parse_implication())
        return node

    def parse_xor(self) -> Node:
        node = self.parse_or()
        while self._match("XOR"):
            node = Binary("XOR", node, self.parse_or())
        return node

    def parse_or(self) -> Node:
        node = self.parse_and()
        while self._match("OR"):
            node = Binary("OR", node, self.parse_and())
        return node

    def parse_and(self) -> Node:
        node = self.parse_not()
        while self._match("AND"):
            node = Binary("AND", node, self.parse_not())
        return node

    def parse_not(self) -> Node:
        if self._match("NOT"):
            return Not(self.parse_not())
        return self.parse_primary()

    def parse_primary(self) -> Node:
        token = self._peek()
        if token is None:
            raise LogicCoverageError("Incomplete predicate. The expression ends too early.")

        if self._match("IDENT"):
            return Variable(token.value)

        if self._match("LPAREN"):
            node = self.parse_equivalence()
            if not self._match("RPAREN"):
                raise LogicCoverageError(
                    f"Unbalanced parentheses. Missing ')' for the group starting at position {token.position}."
                )
            return node

        raise LogicCoverageError(
            f"Unexpected token {token.value!r} at position {token.position}. Check operator placement and parentheses."
        )

    def _peek(self) -> Token | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def _match(self, kind: str) -> bool:
        token = self._peek()
        if token is None or token.kind != kind:
            return False
        self.index += 1
        return True


def ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


class LogicCoverage:
    CRITERIA = {
        "PC": "Predicate Coverage",
        "CC": "Clause Coverage",
        "CoC": "Combinatorial Coverage",
        "GACC": "General Active Clause Coverage",
        "CACC": "Correlated Active Clause Coverage",
        "RACC": "Restricted Active Clause Coverage",
        "GICC": "General Inactive Clause Coverage",
        "RICC": "Restricted Inactive Clause Coverage",
    }

    def __init__(self, predicate: str) -> None:
        self.predicate = predicate.strip()
        self.tokens = tokenize(self.predicate)
        self.ast = Parser(self.tokens).parse()
        self.clauses = ordered_unique(self.ast.variables())
        if not self.clauses:
            raise LogicCoverageError("Predicate must contain at least one clause.")
        self._truth_table_cache: list[dict[str, Any]] | None = None

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        missing = [name for name in self.clauses if name not in assignment]
        if missing:
            raise LogicCoverageError(
                f"Missing clause assignments for: {', '.join(missing)}."
            )
        return self.ast.evaluate(assignment)

    def format_assignment(self, assignment: dict[str, bool]) -> str:
        return ", ".join(f"{name}={BOOL_TEXT[assignment[name]]}" for name in self.clauses)

    def format_row(self, row: dict[str, Any]) -> str:
        return f"t{row['id']}: {self.format_assignment(row['assignment'])} => P={BOOL_TEXT[row['result']]}"

    def serialize_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": row["id"],
            "assignment": dict(row["assignment"]),
            "assignment_label": self.format_assignment(row["assignment"]),
            "result": row["result"],
            "label": self.format_row(row),
        }

    def generate_truth_table(self) -> list[dict[str, Any]]:
        if self._truth_table_cache is None:
            rows: list[dict[str, Any]] = []
            for index, values in enumerate(product([False, True], repeat=len(self.clauses)), start=1):
                assignment = dict(zip(self.clauses, values))
                rows.append(
                    {
                        "id": index,
                        "assignment": assignment,
                        "result": self.ast.evaluate(assignment),
                    }
                )
            self._truth_table_cache = rows
        return list(self._truth_table_cache)

    def classification(self) -> str:
        rows = self.generate_truth_table()
        if all(row["result"] for row in rows):
            return "tautology"
        if not any(row["result"] for row in rows):
            return "contradiction"
        return "satisfiable"

    def determines(self, clause: str, assignment: dict[str, bool]) -> bool:
        if clause not in self.clauses:
            raise LogicCoverageError(f"Unknown clause {clause!r}.")
        original_result = self.evaluate(assignment)
        flipped = dict(assignment)
        flipped[clause] = not flipped[clause]
        return self.evaluate(flipped) != original_result

    def determination_matrix(self) -> dict[str, Any]:
        rows = self.generate_truth_table()
        matrix: dict[str, Any] = {}
        for clause in self.clauses:
            clause_rows = []
            determining_count = 0
            inactive_count = 0
            for row in rows:
                determines = self.determines(clause, row["assignment"])
                if determines:
                    determining_count += 1
                else:
                    inactive_count += 1
                clause_rows.append(
                    {
                        **self.serialize_row(row),
                        "major_value": row["assignment"][clause],
                        "determines": determines,
                    }
                )
            matrix[clause] = {
                "determining_rows": determining_count,
                "inactive_rows": inactive_count,
                "rows": clause_rows,
            }
        return matrix

    def predicate_coverage(self) -> dict[str, Any]:
        rows = self.generate_truth_table()
        true_row = next((row for row in rows if row["result"]), None)
        false_row = next((row for row in rows if not row["result"]), None)
        selected_rows = [
            self.serialize_row(row)
            for row in [true_row, false_row]
            if row is not None
        ]

        return {
            "criterion": "PC",
            "title": self.CRITERIA["PC"],
            "satisfied": true_row is not None and false_row is not None,
            "selected_tests": selected_rows,
            "notes": self._predicate_notes(true_row, false_row),
        }

    def clause_coverage(self) -> dict[str, Any]:
        rows = self.generate_truth_table()
        requirements = {(clause, value) for clause in self.clauses for value in (False, True)}
        remaining = set(requirements)
        selected: list[dict[str, Any]] = []

        while remaining:
            best_row = None
            best_covers: set[tuple[str, bool]] = set()
            for row in rows:
                if row in selected:
                    continue
                covers = {
                    (clause, row["assignment"][clause]) for clause in self.clauses
                } & remaining
                if len(covers) > len(best_covers):
                    best_row = row
                    best_covers = covers
            if best_row is None:
                break
            selected.append(best_row)
            remaining -= best_covers

        by_clause: dict[str, Any] = {}
        for clause in self.clauses:
            true_row = next((row for row in selected if row["assignment"][clause]), None)
            false_row = next((row for row in selected if not row["assignment"][clause]), None)
            by_clause[clause] = {
                "true_test": self.serialize_row(true_row) if true_row else None,
                "false_test": self.serialize_row(false_row) if false_row else None,
                "satisfied": true_row is not None and false_row is not None,
            }

        return {
            "criterion": "CC",
            "title": self.CRITERIA["CC"],
            "satisfied": not remaining,
            "selected_tests": [self.serialize_row(row) for row in selected],
            "remaining_requirements": sorted(remaining),
            "by_clause": by_clause,
        }

    def combinatorial_coverage(self) -> dict[str, Any]:
        rows = self.generate_truth_table()
        return {
            "criterion": "CoC",
            "title": self.CRITERIA["CoC"],
            "satisfied": True,
            "selected_tests": [self.serialize_row(row) for row in rows],
            "row_count": len(rows),
        }

    def gacc(self) -> dict[str, Any]:
        return self._clause_pair_criterion("GACC", active=True, same_result=None, same_minor=False)

    def cacc(self) -> dict[str, Any]:
        return self._clause_pair_criterion("CACC", active=True, same_result=False, same_minor=False)

    def racc(self) -> dict[str, Any]:
        return self._clause_pair_criterion("RACC", active=True, same_result=False, same_minor=True)

    def gicc(self) -> dict[str, Any]:
        return self._clause_pair_criterion("GICC", active=False, same_result=True, same_minor=False)

    def ricc(self) -> dict[str, Any]:
        return self._clause_pair_criterion("RICC", active=False, same_result=True, same_minor=True)

    def analyze(self, focus_criterion: str = "PC") -> dict[str, Any]:
        criteria = {
            "PC": self.predicate_coverage(),
            "CC": self.clause_coverage(),
            "CoC": self.combinatorial_coverage(),
            "GACC": self.gacc(),
            "CACC": self.cacc(),
            "RACC": self.racc(),
            "GICC": self.gicc(),
            "RICC": self.ricc(),
        }
        focus = focus_criterion if focus_criterion in criteria else "PC"
        rows = self.generate_truth_table()
        return {
            "predicate": self.predicate,
            "clauses": self.clauses,
            "row_count": len(rows),
            "classification": self.classification(),
            "truth_table": [self.serialize_row(row) for row in rows],
            "determination_matrix": self.determination_matrix(),
            "criteria_results": criteria,
            "criteria_order": list(criteria.keys()),
            "focus_criterion": focus,
            "focus_result": criteria[focus],
        }

    def _predicate_notes(
        self, true_row: dict[str, Any] | None, false_row: dict[str, Any] | None
    ) -> list[str]:
        notes: list[str] = []
        if true_row is None:
            notes.append("The predicate never evaluates to true, so a true test does not exist.")
        if false_row is None:
            notes.append("The predicate never evaluates to false, so a false test does not exist.")
        if not notes:
            notes.append("One true test and one false test are enough to satisfy predicate coverage.")
        return notes

    def _same_minor_assignments(
        self, clause: str, left_row: dict[str, Any], right_row: dict[str, Any]
    ) -> bool:
        for variable in self.clauses:
            if variable == clause:
                continue
            if left_row["assignment"][variable] != right_row["assignment"][variable]:
                return False
        return True

    def _build_clause_pair(
        self, clause: str, false_row: dict[str, Any], true_row: dict[str, Any]
    ) -> dict[str, Any]:
        minors = [name for name in self.clauses if name != clause]
        fixed_minors = self._same_minor_assignments(clause, false_row, true_row)
        return {
            "major_clause": clause,
            "major_false": self.serialize_row(false_row),
            "major_true": self.serialize_row(true_row),
            "predicate_same": false_row["result"] == true_row["result"],
            "minor_clauses_fixed": fixed_minors,
            "minor_assignments": (
                {name: false_row["assignment"][name] for name in minors} if fixed_minors else None
            ),
        }

    def _clause_pair_criterion(
        self,
        criterion: str,
        *,
        active: bool,
        same_result: bool | None,
        same_minor: bool,
    ) -> dict[str, Any]:
        rows = self.generate_truth_table()
        by_clause: dict[str, Any] = {}

        for clause in self.clauses:
            false_rows = [
                row
                for row in rows
                if row["assignment"][clause] is False
                and self.determines(clause, row["assignment"]) is active
            ]
            true_rows = [
                row
                for row in rows
                if row["assignment"][clause] is True
                and self.determines(clause, row["assignment"]) is active
            ]

            pairs: list[dict[str, Any]] = []
            for false_row in false_rows:
                for true_row in true_rows:
                    predicate_same = false_row["result"] == true_row["result"]
                    minors_fixed = self._same_minor_assignments(clause, false_row, true_row)

                    if same_result is True and not predicate_same:
                        continue
                    if same_result is False and predicate_same:
                        continue
                    if same_minor and not minors_fixed:
                        continue

                    pairs.append(self._build_clause_pair(clause, false_row, true_row))

            by_clause[clause] = {
                "satisfied": bool(pairs),
                "pair_count": len(pairs),
                "representative_pair": pairs[0] if pairs else None,
                "pairs": pairs,
                "determining_test_count": len(true_rows) + len(false_rows),
                "explanation": self._clause_explanation(clause, criterion, active, pairs),
            }

        return {
            "criterion": criterion,
            "title": self.CRITERIA[criterion],
            "satisfied": all(details["satisfied"] for details in by_clause.values()),
            "by_clause": by_clause,
        }

    def _clause_explanation(
        self, clause: str, criterion: str, active: bool, pairs: list[dict[str, Any]]
    ) -> str:
        if pairs:
            if active:
                return f"{criterion} found valid independence pairs for major clause {clause}."
            return f"{criterion} found inactive pairs for major clause {clause}."
        if active:
            return f"No valid active-clause pair exists for major clause {clause} under {criterion}."
        return f"No valid inactive-clause pair exists for major clause {clause} under {criterion}."
