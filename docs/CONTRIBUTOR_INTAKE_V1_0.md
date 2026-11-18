# Jamaican Intelligence — Contributor Intake and Consent Gate v1.0

Date: 2026-11-18. **DRAFT POLICY, NOT AN ACTIVE INTAKE SERVICE.** No consent is implied, collected, or granted by these templates. Do not commit filled forms, voice files, contact details, identity documents, or business-owner submissions to this public repository.

## Three separately governed datasets

| Dataset | Acceptable pilot submissions | Mandatory safeguards |
|---|---|---|
| JAM-LANG | Original Patois forms, orthographic variants, original English gloss, contextual note, contributor-authored short example | Preserve original spelling; distinguish contributor testimony from independently reviewed usage; no assumed audio permission; separate AI-training opt-in |
| JAM-CULT | Factual cultural-history leads, self-authored descriptions, public source links, attributed contemporary practice | Distinguish documented history, oral tradition, interpretation, contemporary practice; respect community restrictions and traditional-knowledge governance |
| JAM-BIZ | Owner-authorized public business name, public service category, public business website and contact, parish, operating-status attestation | No personal contact details without explicit public-display authorization; owner claim is not COJ registration or independent operation verification |

## Minimal submission process (private, not yet deployed)

1. Show a clear notice identifying the Jamaican Intelligence project, dataset, intended uses, public visibility, retention, withdrawal contact and separate permissions.
2. Collect **only** the minimum details for the intended record. Assign a pseudonymous submission ID; keep contributor identity and consent evidence in restricted storage, separate from public data.
3. Record consent evidence including version of the notice, timestamp, scope, affirmative choices, method, and any restrictions. Blank/unknown consent = NOT GRANTED.
4. Verify provenance and rights: contributor must own original text or have documented authority to license it. Publicly viewable third-party media does not establish redistribution or AI-training rights.
5. Human reviewer checks accuracy, risk, and sensitivity. For culture, a relevant community review may be necessary; for businesses, verify owner authority, and separately distinguish **registered** from **currently operating**.
6. Publish only an approved, privacy-minimized derivative record under its own explicit rights status. Never publish the consent ledger or identifying evidence.
7. Process corrections and withdrawal requests with an audit trail. Withdrawal from future publication can be supported, but cannot guarantee recall of copies already downloaded or already-trained models.

## Independent consent choices

All boxes are **unchecked by default**. Each choice is separately recorded:
- Public display of contributed **original text**: opt in / not granted
- Public display of **business-facing contact information** (JAM-BIZ only): opt in / not granted
- Reuse of **original audio** (JAM-LANG only): opt in / not granted; consent from each relevant rights-holder/speaker needed
- **AI training** with the submitted content: opt in / not granted; must specify dataset, content type and permitted scope
- **Commercial reuse**: opt in / not granted; do not equate with public display
- **Third-party redistribution**: opt in / not granted

No single general checkbox authorizes all purposes. Consent is not necessarily the only legal basis for processing personal data; any alternative basis requires a documented legal review. The licence applicable to a submission must be explicit and compatible with its provenance; do not infer a Creative Commons licence.

## Record gates

Every public record must have: record ID, dataset, original claim/text, source URL or restricted-evidence reference, retrieval date, last-reviewed date, rights status, confidence, verification status, and publication decision. Missing evidence is represented as unknown/pending, never invented.

Public records must **not** include: personal emails/phone numbers without specific consent, home addresses, government identifiers, consent receipts, unpublished audio, raw third-party transcripts, or names of vulnerable speakers.

Review status sequence: `submitted` → `provenance_review` → `rights_review` → `content_review` → `approved_for_publication` or `rejected` / `on_hold`. The approval decision is a human action; schema checks cannot confer it.

## Rights and privacy references (policy research only)

- Office of the Information Commissioner, Jamaica: https://www.oic.gov.jm/
- Jamaica Data Protection Act, 2020 (verify the current consolidated law and commencement details with counsel): https://japarliament.gov.jm/
- Creative Commons licence guidance: https://creativecommons.org/share-your-work/cclicenses/
- YouTube Terms: https://www.youtube.com/t/terms

**Important:** This document is an operational design, not a legal opinion. Before real intake begins, designate a responsible controller, publish a proper privacy notice, agree on retention/deletion periods and access controls, and obtain Jamaican legal/privacy review as appropriate.

## Current blocker and next step

No secure intake endpoint or private consent-evidence store has been verified. Until one exists, do not solicit identifying information via public GitHub issues. Next implement a secure submission workflow and an audit trail, then conduct a small human-approved test with synthetic data before real contributors.
