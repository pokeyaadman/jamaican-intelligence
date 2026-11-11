# GitHub publication guide — v0.6.1

This is a ready-to-upload **GitHub public beta candidate**. Its creation does **not** mean it has been pushed or deployed. Before making it public, a maintainer should review source attribution, public metadata and publication scope.

## Suggested GitHub repository

`jamaican-intelligence` (suggested name only; no repository creation is claimed).

## Web workflow

1. In GitHub, choose **New repository**, enter `jamaican-intelligence` (or your preferred name), set visibility **Public**, and create it. Do not select a generic repository-wide licence that might conflict with dataset-specific rights.
2. Extract this ZIP locally; upload **the extracted files and directories** to the repository root. Do not upload the ZIP as the sole repo content.
3. Confirm GitHub Actions is enabled and the **Dataset beta checks** workflow passes on the initial commit.
4. Read `ATTRIBUTION.md`, `LICENSES/JAM-LANG-CC-BY-SA-4.0.md` and `docs/OWNER_ATTESTATION.md` before attaching any public release tag.
5. Optionally create a GitHub Release tagged `v0.6.1-beta`, clearly labelled a provisional, owner-attested lexical research preview.
6. Keep `JAM-CULT.csv` and `JAM-BIZ.csv` header-only until qualified reviews, source rights and business-status checks are recorded.
7. Configure a private takedown/contact method outside public Issues before soliciting private submissions. Do not put consent records in the repository.

## Verification scope

- The automated gate validates metadata and limited release eligibility, **not** linguistic accuracy, institutional endorsement, or every licence issue.
- The owner affirmed the 55-record working dataset, but no third party has yet answered the initial review requests as of the source run.
- The 30 licensed-source Patois words can be previewed with clear warnings; no culture/business data are public in this package.
