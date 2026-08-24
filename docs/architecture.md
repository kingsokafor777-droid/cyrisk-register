# Architecture

The package is pure and local-first. A caller supplies a register record, tolerance context,
observations, closure claim, and explicit `as_of` date. The evaluator reports only derived signals
such as `within_tolerance`, `review_due`, and `closure_claimed`; it never sends an escalation or
changes status.

| Stage | Deterministic operation | Boundary |
|---|---|---|
| Record | Validate IDs, ownership references, and supplied range context. | No identity or authorization validation. |
| Context | Compare supplied central value to declared threshold. | No appetite approval or decision. |
| Review | Identify supplied review due date. | No reviewer authentication. |
| Closure | Retain a closure claim and evidence IDs. | No remediation verification. |
