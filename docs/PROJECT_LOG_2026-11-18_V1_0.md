# Jamaican Intelligence — Project log and backlog

## 2026-11-18 | Research governance milestone v1.0 (draft)

**Completed in this branch:** contributor intake and consent policy; JSON-ready private intake schema; header-only private consent-register template; validation tests. **Zero new submitted records, zero permissions granted, zero new public records.** Existing public language dataset remains unchanged.

**Prior work observed:** main contains the earlier beta; draft PR #2 stages additional lexemes, draft PR #4 stages YouTube metadata and draft PR #6 stages an annotation workbench. These are not evidence of new human approvals or cleared audio.

**Quality limitations:** The policy and schema are designs, not a deployed intake system. A file header does not prove a permission grant. Legal and community review have not occurred. Registration checks are distinct from evidence that a business is currently operating.

## Prioritized backlog

| Priority | Task | Exit criterion | Status |
|---|---|---|---|
| P0 | Separate consent choices and private evidence model | Reviewable policy, schema, and tests | Draft delivered |
| P0 | Privacy/legal and cultural-community governance review | Named responsible reviewers, approved notice, retention/access controls | Blocked: human decision |
| P0 | Secure private submission endpoint and restricted ledger | Tested with synthetic submissions; no personal data in public repo | Not started |
| P1 | Native Jamaican Creole review of PR #2 lexical candidates | Each approved entry has cited gloss, context, rights, reviewer evidence | Pending |
| P1 | Source-rights and speaker review for PR #4/#6 video leads | Scope-specific permission; no copied media without rights | Pending |
| P1 | JAM-CULT pilot provenance review | Distinct claim types, authoritative source, community restrictions | Pending |
| P1 | JAM-BIZ owner-authorized pilot | At least 3 voluntarily submitted, permissioned, independently checked records | Pending |
| P2 | Public release of approved additions | Human sign-off, reproducible validation, versioned changelog | Pending |

## Next run

Implement a synthetic-data-only intake validator and controlled publication-export gate; then evaluate one authoritative, rights-compatible cultural source and one business-source verification workflow without bulk scraping.
