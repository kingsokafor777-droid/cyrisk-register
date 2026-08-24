"""Pure explicit-date register signal evaluator with no workflow side effects."""

from __future__ import annotations

from datetime import date

from cyrisk_core.canonical import content_hash

from cyrisk_register.models import RegisterEvaluation, RegisterRequest

LIMITATIONS = (
    "Technical signal from supplied records and supplied tolerance context only; not validation of "
    "authority, organizational appetite, evidence sufficiency, remediation, closure, escalation, "
    "or risk decision."
)


def evaluate(request: RegisterRequest, as_of: date) -> RegisterEvaluation:
    """Return deterministic threshold/date/closure signals for caller-provided records."""
    return RegisterEvaluation(
        register_id=request.register_id,
        risk_id=request.risk.risk_id,
        as_of=as_of,
        central_above_tolerance=request.risk.central_exposure > request.tolerance.threshold_central,
        review_due=as_of >= request.risk.review_due_on,
        closure_claimed=request.closure is not None,
        manifest_hash=content_hash(request.model_dump(mode="json")),
        limitations=LIMITATIONS,
    )
