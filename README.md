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
## Weekly Compliance Audit Summary

_Last generated: 2026-09-14 11:37 UTC · Source: atool3800-stack/project_20260813_015033_23c9c93d_

### Overall Statistics

| Metric | Count |
| --- | ---: |
| Open compliance issues | 0 |
| United Kingdom (UK) | 0 |
| France (FR) | 0 |
| Germany (DE) | 0 |
| Priority P0 (critical) | 0 |
| Priority P1 (high) | 0 |
| Priority P2 (normal) | 0 |

### Priority Distribution by Country

| Country | P0 | P1 | P2 | Total |
| --- | ---: | ---: | ---: | ---: |
| United Kingdom (UK) | 0 | 0 | 0 | 0 |
| France (FR) | 0 | 0 | 0 | 0 |
| Germany (DE) | 0 | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** | **0** |

### High-Risk Open Items (P0 / P1)

#### United Kingdom (UK)

_No open high-priority items._

#### France (FR)

_No open high-priority items._

#### Germany (DE)

_No open high-priority items._
<!-- WEEKLY-COMPLIANCE-END -->

## Operations

- **Owner:** DevOps / Compliance Engineering
- **Review cadence:** weekly (Monday), plus ad-hoc on incident escalations
- **Source automation:** `scripts/weekly_compliance_sync.py`
  (git + GitHub API only, Python standard library, no external services)

For questions about the automation, please open an issue tagged `documentation`.
