"""Generate a sealed synthetic Cyrisk Register request."""

from __future__ import annotations

from pathlib import Path

from cyrisk_register.models import RegisterRequest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "fixtures" / "synthetic_register_request.json"

PAYLOAD = {
    "register_id": "register-synthetic",
    "risk": {
        "risk_id": "risk-synthetic-ransomware",
        "scenario_reference": "scenario-synthetic-ransomware",
        "owner_reference": "synthetic-risk-owner",
        "status": "open",
        "currency": "USD",
        "central_exposure": "250000",
        "tolerance_context_id": "tolerance-synthetic",
        "tolerance_context_version": "1.0",
        "review_due_on": "2098-01-01",
        "evidence_references": ["evidence-synthetic-one"],
    },
    "tolerance": {
        "context_id": "tolerance-synthetic",
        "version": "1.0",
        "currency": "USD",
        "threshold_central": "200000",
        "basis": "synthetic annual exposure context",
        "source_reference": "synthetic-governance-reference",
        "approved_authority_validated": False,
    },
    "reviews": [
        {
            "review_id": "review-synthetic-one",
            "risk_id": "risk-synthetic-ransomware",
            "reviewer_reference": "synthetic-reviewer",
            "observed_on": "2097-01-01",
            "observation": "Synthetic review observation; no authority assertion.",
            "authority_validated": False,
        }
    ],
    "closure": None,
}


def main() -> None:
    request = RegisterRequest.model_validate(PAYLOAD)
    TARGET.write_text(request.model_dump_json(indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
