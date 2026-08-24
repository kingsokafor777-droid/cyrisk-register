# Cyrisk Register

> **Deterministic risk-register workflow records and tolerance-context signals—not authorization, risk acceptance, entitlement validation, remediation execution, or an enterprise decision system.**

`cyrisk-register` stores supplied ownership references, scenario references, quantitative context,
appetite/tolerance thresholds, review observations, closure claims, and escalation signals at an
explicit caller-provided date. It is designed for technical traceability, not to replace the
governance decision process.

| Artifact | Deterministic purpose | Explicit non-claim |
|---|---|---|
| `RiskRecord` | Binds risk, scenario, owner reference, status, and supplied exposure context. | Does not accept or prioritize risk. |
| `ToleranceContext` | Declares a versioned threshold and basis. | Does not establish organizational appetite. |
| `ReviewObservation` | Records supplied reviewer text and date. | Does not validate reviewer authority. |
| `ClosureRecord` | Records a claimed closure and evidence references. | Does not verify remediation or authorize closure. |
| `RegisterEvaluation` | Flags threshold/date status from supplied records. | Does not escalate, notify, or decide. |

NIST treats cybersecurity risk registers as inputs to enterprise risk management and governance,
not substitutes for leadership decisions. [1] [2]

## Boundary

The package has no external systems, identity provider, database, scheduler, notifications,
approval workflow, cloud client, or remediation action. Deployers own authority validation,
tolerance approval, legal context, risk acceptance, remediation verification, and every
organizational decision.

## References

[1]: https://csrc.nist.gov/pubs/ir/8286/r1/final "NISTIR 8286 Rev. 1"
[2]: https://csrc.nist.gov/pubs/ir/8286/a/r1/final "NISTIR 8286A Rev. 1"
