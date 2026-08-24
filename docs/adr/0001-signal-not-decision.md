# ADR 0001: Emit signals, not decisions

**Status:** Accepted

This component evaluates caller-supplied values against a caller-supplied tolerance context and
reports a signal. It cannot accept risk, authorize an exception, assign a remediation, notify a
person, or close a ticket. This preserves an auditable technical boundary between workflow records
and decision authority.
