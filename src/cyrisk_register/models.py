"""Strict supplied-record contracts for non-authorizing Cyrisk register workflows."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

ID_PATTERN = r"^[a-z][a-z0-9_-]{2,63}$"
HASH_PATTERN = r"^[a-f0-9]{64}$"


class RegisterRecord(BaseModel):
    """Immutable strict record common to all register artifacts."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class RiskStatus(str, Enum):
    OPEN = "open"
    MONITORED = "monitored"
    CLOSURE_CLAIMED = "closure_claimed"


class ToleranceContext(RegisterRecord):
    """Supplied versioned tolerance threshold; not approved appetite evidence."""

    context_id: str = Field(pattern=ID_PATTERN)
    version: str = Field(pattern=r"^\d+\.\d+$")
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    threshold_central: Decimal = Field(ge=0)
    basis: str = Field(min_length=1, max_length=120)
    source_reference: str = Field(min_length=1, max_length=160)
    approved_authority_validated: bool = False

    @model_validator(mode="after")
    def reject_authority_assertion(self) -> ToleranceContext:
        if self.approved_authority_validated:
            raise ValueError("tolerance context cannot assert approved authority")
        return self


class RiskRecord(RegisterRecord):
    """Technical risk-register record with supplied context and no acceptance operation."""

    risk_id: str = Field(pattern=ID_PATTERN)
    scenario_reference: str = Field(pattern=ID_PATTERN)
    owner_reference: str = Field(min_length=1, max_length=160)
    status: RiskStatus = RiskStatus.OPEN
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    central_exposure: Decimal = Field(ge=0)
    tolerance_context_id: str = Field(pattern=ID_PATTERN)
    tolerance_context_version: str = Field(pattern=r"^\d+\.\d+$")
    review_due_on: date
    evidence_references: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_evidence_references(self) -> RiskRecord:
        if len(set(self.evidence_references)) != len(self.evidence_references):
            raise ValueError("evidence_references must be unique")
        return self


class ReviewObservation(RegisterRecord):
    """Supplied observation; reviewer reference does not establish authority."""

    review_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    reviewer_reference: str = Field(min_length=1, max_length=160)
    observed_on: date
    observation: str = Field(min_length=1, max_length=500)
    authority_validated: bool = False

    @model_validator(mode="after")
    def reject_authority_assertion(self) -> ReviewObservation:
        if self.authority_validated:
            raise ValueError("review observations cannot assert authority")
        return self


class ClosureRecord(RegisterRecord):
    """Claimed closure record with required evidence references and no verification semantics."""

    closure_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    claimed_on: date
    evidence_references: tuple[str, ...] = Field(min_length=1)
    remediation_verified: bool = False

    @model_validator(mode="after")
    def reject_verification_assertion(self) -> ClosureRecord:
        if self.remediation_verified:
            raise ValueError("closure records cannot assert remediation verification")
        if len(set(self.evidence_references)) != len(self.evidence_references):
            raise ValueError("closure evidence_references must be unique")
        return self


class RegisterRequest(RegisterRecord):
    """Supplied register/tolerance/review context for technical signal evaluation."""

    register_id: str = Field(pattern=ID_PATTERN)
    risk: RiskRecord
    tolerance: ToleranceContext
    reviews: tuple[ReviewObservation, ...] = ()
    closure: ClosureRecord | None = None

    @model_validator(mode="after")
    def validate_links(self) -> RegisterRequest:
        if self.risk.currency != self.tolerance.currency:
            raise ValueError("risk and tolerance currency must match")
        if self.risk.tolerance_context_id != self.tolerance.context_id:
            raise ValueError("risk tolerance context ID must match")
        if self.risk.tolerance_context_version != self.tolerance.version:
            raise ValueError("risk tolerance context version must match")
        if any(review.risk_id != self.risk.risk_id for review in self.reviews):
            raise ValueError("reviews must reference the request risk")
        if len({review.review_id for review in self.reviews}) != len(self.reviews):
            raise ValueError("review IDs must be unique")
        if self.closure is not None and self.closure.risk_id != self.risk.risk_id:
            raise ValueError("closure must reference the request risk")
        return self


class RegisterEvaluation(RegisterRecord):
    """Technical signal report; not a risk decision, escalation, or workflow action."""

    register_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    as_of: date
    central_above_tolerance: bool
    review_due: bool
    closure_claimed: bool
    manifest_hash: str = Field(pattern=HASH_PATTERN)
    limitations: str = Field(min_length=1, max_length=500)
