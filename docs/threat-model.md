# Threat Model

| Threat | Example | Mitigation and boundary |
|---|---|---|
| Unauthorized acceptance | A register row is treated as a signed decision. | No acceptance field or approval operation exists. |
| Time ambiguity | Review status varies by runtime date. | Caller supplies an explicit `as_of` date. |
| Authority overstatement | A reviewer reference is trusted as entitlement. | Authority assertions are rejected. |
| Closure overclaim | A claimed closure is treated as verified remediation. | Output names it `closure_claimed`. |
| Threshold ambiguity | Different scales are silently compared. | Currency and tolerance basis must match. |
