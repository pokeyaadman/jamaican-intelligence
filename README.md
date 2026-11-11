# Jamaican Intelligence — Patois lexical beta v0.6.1

**Status:** Owner-attested research preview, prepared 11 November 2026.
**Hosting:** GitHub-ready repository package; GitHub publication has NOT been confirmed. See `docs/GITHUB_PUBLICATION_GUIDE.md`.
**Contents:** 30 source-attributed Jamaican Creole/Patois vocabulary records. The culture and business tables are intentionally empty in this beta.

## What “verified” means here

The project owner stated that the 55-record working dataset has been verified. That dataset-level attestation is recorded as `owner_verified`. The source forms were independently checked against the listed Wiktionary source in earlier research, but **no UWI linguist, cultural institution or business operator has yet endorsed these data**. The owner statement also does not establish third-party redistribution rights or that a listed business is currently operating.

The 30 language rows are released **only as an explicitly qualified beta preview** with their existing CC BY-SA 4.0 source conditions. Treat meanings, grammatical tags and variants as provisional until specialist review; do not use the dataset as a formal standard or authoritative corpus.

## Layout

- `data/JAM-LANG.csv`: 30 CC BY-SA 4.0 licensed-source lexical records, with provenance and owner attestation.
- `data/JAM-CULT.csv`: schema headers only; rights and specialist review remain incomplete.
- `data/JAM-BIZ.csv`: schema headers only; operating status and reuse terms remain incomplete.
- `ATTRIBUTION.md`: source, licence, adaptations and obligations.
- `docs/OWNER_ATTESTATION.md`: what the owner's confirmation does and does not establish.
- `docs/RELEASE_POLICY.md`: distinction between a beta preview and a full production dataset.
- `metadata/source_index.csv`: discovery/reference register, NOT a republication licence for every source.
- `tools/beta_release_gate.py`: machine-checkable safety/attribution gate for this preview.
- `tools/release_gate.py`: strict original full-production validator, retained for future releases.

## Validate the preview

```bash
python tools/beta_release_gate.py .
```

The strict production gate continues to require per-record evidence and approvals. Its policy has **not** been weakened by this beta release.

## Corrections and contacts

Before making a public GitHub repository, configure an issue or correction channel and obtain a final review of public metadata. No private consents, recordings or identifiable contributor records are included.

## GitHub maintenance

GitHub Actions run a metadata/attribution release gate and a checksum check on pushes and pull requests. Public issue reports are for non-sensitive corrections only; see `CONTRIBUTING.md`. These checks do not establish independent linguistic validation.
