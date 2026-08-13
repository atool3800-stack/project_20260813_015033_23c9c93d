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

_Last generated: 2026-08-13 11:20 UTC · Source: atool3800-stack/project_20260813_015033_23c9c93d_

### Overall Statistics

| Metric | Count |
| --- | ---: |
| Open compliance issues | 358 |
| United Kingdom (UK) | 104 |
| France (FR) | 118 |
| Germany (DE) | 136 |
| Priority P0 (critical) | 79 |
| Priority P1 (high) | 122 |
| Priority P2 (normal) | 157 |

### Priority Distribution by Country

| Country | P0 | P1 | P2 | Total |
| --- | ---: | ---: | ---: | ---: |
| United Kingdom (UK) | 22 | 36 | 46 | 104 |
| France (FR) | 25 | 42 | 51 | 118 |
| Germany (DE) | 32 | 44 | 60 | 136 |
| **Total** | **79** | **122** | **157** | **358** |

### High-Risk Open Items (P0 / P1)

#### United Kingdom (UK)

| # | Issue | Priority | Type | Assignee | Milestone | Updated |
| ---: | --- | --- | --- | --- | --- | --- |
| [23](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/23) | [UK] Update Record of Processing Activities for MHRA (Manchester NHS Partner) | P0 | documentation | atool3800-stack | GDPR Remediation 2026 | 2026-08-13 |
| [28](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/28) | [UK] Audit finding: unlogged data export (Manchester NHS Partner) | P0 | audit | atool3800-stack | 2026 Q4 Compliance Audit | 2026-08-13 |
| [55](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/55) | [UK] Incident: data breach notification at Manchester NHS Partner | P0 | incident | atool3800-stack | 2026 Q4 Compliance Audit | 2026-08-13 |
| [95](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/95) | [UK] Incident: unauthorised access attempt at London HQ | P0 | incident | atool3800-stack | Patient Safety & Incident Response | 2026-08-13 |
| [108](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/108) | [UK] Training: GDPR fundamentals for administrative staff (London HQ) | P0 | training | atool3800-stack | Staff Training & Awareness | 2026-08-13 |
| [110](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/110) | [UK] Audit finding: missing vendor assessment (London HQ) | P0 | audit | atool3800-stack | 2026 Q4 Compliance Audit | 2026-08-13 |
| [125](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/125) | [UK] Audit finding: weak password policy enforcement (Leeds Clinic) | P0 | audit | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [144](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/144) | [UK] Audit finding: missing vendor assessment (London HQ) | P0 | audit | atool3800-stack | 2026 Q4 Compliance Audit | 2026-08-13 |
| [152](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/152) | [UK] Incident: misconfigured access role at Manchester NHS Partner | P0 | incident | atool3800-stack | GDPR Remediation 2026 | 2026-08-13 |
| [184](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/184) | [UK] Update Data Protection Impact Assessment for CQC (Manchester NHS Partner) | P0 | documentation | atool3800-stack | Documentation & Records | 2026-08-13 |

#### France (FR)

| # | Issue | Priority | Type | Assignee | Milestone | Updated |
| ---: | --- | --- | --- | --- | --- | --- |
| [12](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/12) | [FR] Audit finding: outdated retention schedule (Toulouse Site) | P0 | audit | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [19](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/19) | [FR] Audit finding: incomplete audit trail (Lyon Clinic) | P0 | audit | — | 2026 Q3 Compliance Audit | 2026-08-13 |
| [37](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/37) | [FR] Audit finding: expired access rights (Toulouse Site) | P0 | audit | atool3800-stack | 2026 Q4 Compliance Audit | 2026-08-13 |
| [35](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/35) | [FR] Incident: phishing incident at Lyon Clinic | P0 | incident | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [45](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/45) | [FR] Incident: consent record discrepancy at Toulouse Site | P0 | incident | atool3800-stack | Patient Safety & Incident Response | 2026-08-13 |
| [81](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/81) | [FR] Training: medical device cybersecurity for IT (Toulouse Site) | P0 | training | — | Staff Training & Awareness | 2026-08-13 |
| [104](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/104) | [FR] Incident: audit-log gap at Toulouse Site | P0 | incident | atool3800-stack | GDPR Remediation 2026 | 2026-08-13 |
| [118](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/118) | [FR] Incident: lost unencrypted device at Lyon Clinic | P0 | incident | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [146](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/146) | [FR] Training: GDPR fundamentals for compliance (Lyon Clinic) | P0 | training | atool3800-stack | Staff Training & Awareness | 2026-08-13 |
| [150](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/150) | [FR] Incident: vendor security incident at Toulouse Site | P0 | incident | — | GDPR Remediation 2026 | 2026-08-13 |

#### Germany (DE)

| # | Issue | Priority | Type | Assignee | Milestone | Updated |
| ---: | --- | --- | --- | --- | --- | --- |
| [14](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/14) | [DE] Training: consent management for administrative staff (Frankfurt Hospital) | P0 | training | atool3800-stack | Staff Training & Awareness | 2026-08-13 |
| [32](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/32) | [DE] Incident: unauthorised access attempt at Frankfurt Hospital | P0 | incident | atool3800-stack | Patient Safety & Incident Response | 2026-08-13 |
| [43](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/43) | [DE] Incident: phishing incident at Munich Site | P0 | incident | — | GDPR Remediation 2026 | 2026-08-13 |
| [50](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/50) | [DE] Incident: misconfigured access role at Hamburg Clinic | P0 | incident | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [66](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/66) | [DE] Update Access Control Policy for ISO 13485 (Berlin HQ) | P0 | documentation | — | GDPR Remediation 2026 | 2026-08-13 |
| [93](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/93) | [DE] Incident: consent record discrepancy at Munich Site | P0 | incident | — | GDPR Remediation 2026 | 2026-08-13 |
| [101](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/101) | [DE] Incident: unauthorised access attempt at Hamburg Clinic | P0 | incident | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [105](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/105) | [DE] Incident: consent record discrepancy at Munich Site | P0 | incident | — | 2026 Q4 Compliance Audit | 2026-08-13 |
| [134](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/134) | [DE] Training: third-party risk for administrative staff (Berlin HQ) | P0 | training | atool3800-stack | Staff Training & Awareness | 2026-08-13 |
| [137](https://github.com/atool3800-stack/project_20260813_015033_23c9c93d/issues/137) | [DE] Incident: consent record discrepancy at Hamburg Clinic | P0 | incident | atool3800-stack | Patient Safety & Incident Response | 2026-08-13 |
<!-- WEEKLY-COMPLIANCE-END -->

## Operations

- **Owner:** DevOps / Compliance Engineering
- **Review cadence:** weekly (Monday), plus ad-hoc on incident escalations
- **Source automation:** `scripts/weekly_compliance_sync.py`
  (git + GitHub API only, Python standard library, no external services)

For questions about the automation, please open an issue tagged `documentation`.
