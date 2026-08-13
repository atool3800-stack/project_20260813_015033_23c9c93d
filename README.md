# EU Healthcare Compliance Audit Tracker

This repository is the single source of truth for **medical compliance & audit
todos** across our European operations. We are a large European healthcare
organisation (HQ in Germany, branches in the United Kingdom and France,
1000+ employees) operating under GDPR, national health-data regulations
(UK GDPR / DPA 2018, French CNIL, German BDSG) and medical-device / clinical
compliance frameworks (MDR, ISO 13485, GxP).

## How issues are organised

Every open issue is labelled with:

| Dimension | Labels |
| --- | --- |
| Country | `UK`, `FR`, `DE` |
| Priority | `P0` (critical), `P1` (high), `P2` (normal) |
| Type | `documentation`, `audit`, `training`, `incident` |

Issues are additionally grouped into milestones (e.g. quarterly audit cycles,
GDPR remediation, clinical data governance, patient-safety incident response).

## Weekly compliance summary

Every Monday the **Weekly Compliance Audit Sync** workflow
(`.github/workflows/weekly-compliance-sync.yml`) fetches all open issues via
the GitHub API, recomputes the statistics below and opens a pull request with
the refreshed summary. **Do not edit the block between the two markers below
manually** - it is regenerated automatically.

<!-- WEEKLY-COMPLIANCE-START -->
<!-- WEEKLY-COMPLIANCE-END -->

## Operations

- **Owner:** DevOps / Compliance Engineering
- **Review cadence:** weekly (Monday), plus ad-hoc on incident escalations
- **Source automation:** `scripts/weekly_compliance_sync.py`
  (git + GitHub API only, Python standard library, no external services)

For questions about the automation, please open an issue tagged `documentation`.
