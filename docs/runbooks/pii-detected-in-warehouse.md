# Runbook — PII detected in the warehouse

**Severity: highest class. DPO owns the process from step 2.** Ties to
the incident process in `jolarca-infrastructure` and SECURITY.md.

## Steps

1. **Quarantine.** Pause downstream refresh of the affected marts;
   restrict query access to the affected tables (data platform owner,
   immediately).
2. **Notify the DPO** (`jolarca-compliance`) — before further technical
   action. The GDPR 72h assessment clock is the DPO's call.
3. **Scope.** Determine: which tables/columns, since when, how many
   rows (counts only — do not extract the values), which consumers
   read it. Use `scripts/scan-warehouse-pii.py --warehouse` for the
   sweep.
4. **Purge/repair.** Remove the offending data via a reviewed change:
   fix the pseudonymizer/contract defect first, then purge or
   re-pseudonymize the landed rows, then rebuild downstream marts.
5. **Root cause.** Which boundary failed — extract allow-list,
   pseudonymizer rule, or a model that re-introduced an identifier?
   The fix must close the class of failure, not the instance.
6. **Evidence.** Record timeline, scope counts, actions, and the DPO's
   notification decision. Evidence custody: `jolarca-compliance`.
7. **Verify.** Run `make anonymize-verify` and the pii-scan self-test;
   both must pass before the marts are un-paused.

## Never

- Do not quietly delete and move on — notification duty assessment must
  happen even when the fix looks trivial.
- Do not paste offending values into issues, chat, or this runbook's
  records.
