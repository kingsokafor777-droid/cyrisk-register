from __future__ import annotations

import pytest
from pydantic import ValidationError

from cyrisk_register.models import (
    ClosureRecord,
    RegisterRequest,
    ReviewObservation,
    ToleranceContext,
)


def payload() -> dict[str, object]:
    return {
        "register_id": "register-one",
        "risk": {
            "risk_id": "risk-one",
            "scenario_reference": "scenario-one",
            "owner_reference": "synthetic-owner",
            "currency": "USD",
            "central_exposure": "100",
            "tolerance_context_id": "tolerance-one",
            "tolerance_context_version": "1.0",
            "review_due_on": "2099-01-01",
            "evidence_references": ["evidence-one"],
        },
        "tolerance": {
            "context_id": "tolerance-one",
            "version": "1.0",
            "currency": "USD",
            "threshold_central": "90",
            "basis": "synthetic basis",
            "source_reference": "synthetic-source",
        },
        "reviews": [],
        "closure": None,
    }


def test_authority_and_remediation_verification_assertions_are_rejected() -> None:
    with pytest.raises(ValidationError, match="approved authority"):
        ToleranceContext(
            context_id="tolerance-one",
            version="1.0",
            currency="USD",
            threshold_central="1",
            basis="synthetic",
            source_reference="synthetic",
            approved_authority_validated=True,
        )
    with pytest.raises(ValidationError, match="authority"):
        ReviewObservation(
            review_id="review-one",
            risk_id="risk-one",
            reviewer_reference="synthetic",
            observed_on="2099-01-01",
            observation="Synthetic.",
            authority_validated=True,
        )
    with pytest.raises(ValidationError, match="remediation verification"):
        ClosureRecord(
            closure_id="closure-one",
            risk_id="risk-one",
            claimed_on="2099-01-01",
            evidence_references=("evidence-one",),
            remediation_verified=True,
        )


def test_request_rejects_mismatched_links_duplicates_and_currency() -> None:
    record = payload()
    record["risk"]["currency"] = "CAD"  # type: ignore[index]
    with pytest.raises(ValidationError, match="currency"):
        RegisterRequest.model_validate(record)
    record = payload()
    record["reviews"] = [
        {
            "review_id": "review-one",
            "risk_id": "other-risk",
            "reviewer_reference": "synthetic",
            "observed_on": "2099-01-01",
            "observation": "Synthetic.",
        }
    ]
    with pytest.raises(ValidationError, match="request risk"):
        RegisterRequest.model_validate(record)
    record = payload()
    record["risk"]["evidence_references"] = ["evidence-one", "evidence-one"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="must be unique"):
        RegisterRequest.model_validate(record)


def test_request_rejects_context_review_and_closure_link_failures() -> None:
    with pytest.raises(ValidationError, match="closure evidence_references"):
        ClosureRecord(
            closure_id="closure-one",
            risk_id="risk-one",
            claimed_on="2099-01-01",
            evidence_references=("evidence-one", "evidence-one"),
        )
    record = payload()
    record["risk"]["tolerance_context_id"] = "other-context"  # type: ignore[index]
    with pytest.raises(ValidationError, match="context ID"):
        RegisterRequest.model_validate(record)
    record = payload()
    record["risk"]["tolerance_context_version"] = "2.0"  # type: ignore[index]
    with pytest.raises(ValidationError, match="context version"):
        RegisterRequest.model_validate(record)
    record = payload()
    review = {
        "review_id": "review-one",
        "risk_id": "risk-one",
        "reviewer_reference": "synthetic",
        "observed_on": "2099-01-01",
        "observation": "Synthetic.",
    }
    record["reviews"] = [review, review]
    with pytest.raises(ValidationError, match="review IDs"):
        RegisterRequest.model_validate(record)
    record = payload()
    record["closure"] = {
        "closure_id": "closure-one",
        "risk_id": "other-risk",
        "claimed_on": "2099-01-01",
        "evidence_references": ["evidence-one"],
    }
    with pytest.raises(ValidationError, match="closure must"):
        RegisterRequest.model_validate(record)
