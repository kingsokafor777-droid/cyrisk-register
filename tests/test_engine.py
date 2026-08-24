from __future__ import annotations

from datetime import date
from pathlib import Path

from cyrisk_register.engine import evaluate
from cyrisk_register.models import ClosureRecord, RegisterRequest

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_register_request.json"


def request() -> RegisterRequest:
    return RegisterRequest.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def test_explicit_date_evaluation_emits_only_technical_signals() -> None:
    result = evaluate(request(), date(2099, 1, 1))
    assert result.central_above_tolerance is True
    assert result.review_due is True
    assert result.closure_claimed is False
    assert "not validation of authority" in result.limitations


def test_closure_claim_changes_manifest_and_signal() -> None:
    baseline = evaluate(request(), date(2099, 1, 1))
    payload = request().model_dump(mode="json")
    payload["closure"] = ClosureRecord(
        closure_id="closure-synthetic-one",
        risk_id="risk-synthetic-ransomware",
        claimed_on=date(2099, 1, 1),
        evidence_references=("evidence-synthetic-one",),
    ).model_dump(mode="json")
    result = evaluate(RegisterRequest.model_validate(payload), date(2099, 1, 1))
    assert result.closure_claimed is True
    assert result.manifest_hash != baseline.manifest_hash
