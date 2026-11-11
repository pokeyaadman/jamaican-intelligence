# Jamaican Intelligence — Human Speech Annotation Pilot v0.9

**Status: Research pilot only. No actual video was listened to or annotated by the assistant.** The workbench lets an authorized human reviewer create non-verbatim notes from official YouTube playback. It does not ingest, transcribe, download or store YouTube media.

## How to run

1. Download BOTH files **annotation_workbench.html** and **annotation_workbench.js** from this folder into the SAME folder on your computer.
2. Open annotation_workbench.html in a modern browser. It requires no installation, account, Python or API key.
3. Select one of the **six video leads**. The two channel-only leads from v0.8 are not eligible until individual episodes are recorded.
4. Choose **Open recording** or **Open at timestamp**. The site opens the video's official YouTube page in a new browser tab. Play normally; do not scrape or download it.
5. Only after listening, enter the **actual** time in seconds (for example 1:42 = 102). Describe a short lexical, grammar, phonological or code-switching feature **in your own words**.
6. Keep notes free of direct dialogue, full transcripts, song lyrics, private names, telephone numbers, email addresses and speaker identity claims.
7. Check the two attestations. They attest to the reviewing person's actions; **they do not establish linguistic expertise, owner approval or media reuse rights**.
8. Select **Export review-only CSV**. Notes live **only in the browser tab's memory** until explicitly downloaded. Reloading clears them; no backend server or browser storage is used.
9. Keep the exported CSV in **restricted storage** and provide it privately for human language and rights review. **Do not upload exports into the public GitHub repository.**

## Validation

From repository root:

~~~bash
python tools/validate_annotation_pilot.py .
python -m unittest discover -s tests -p "test_annotation_pilot.py"
node --check research/youtube/annotation_workbench.js
~~~

After a reviewer privately exports a CSV:

~~~bash
python tools/validate_annotation_pilot.py --input /path/to/PRIVATE-reviewer-export.csv
~~~

These checks enforce schema, source-ID consistency, timestamp, original-note length, privacy red flags, review status and rights fields. They **cannot determine whether audio was played, whether text was copied, whether the source was authentic, or whether a reviewer is qualified**.

## What a reviewer is NOT approving

The workbench always exports these restricted statuses:

- release_decision = hold_review_pending
- independent_linguistic_review = pending
- privacy_assessment = pending_manual_review
- transcript_reuse_permission = not_granted
- original_audio_permission = not_granted
- ai_training_permission = not_granted

Separate source-specific, purpose-specific rights evidence and qualified linguistic review are needed before publication or model training.

## Proposed first human review pilot

A first pilot may assign **two recordings per reviewer**: one source listed as informal/unscripted and one educational or interview. Aim for three to five short, independent, timestamped observations per suitable recording. This is a proposed plan, **not a claim that observations have already been collected**.

First verify actual content: teaching clips, commentary, music and edited performance must not be labelled spontaneous Jamaican speech. Diaspora language should be labelled appropriately, never assigned a parish from accent or appearance. The Wikitongues publisher description states CC BY-NC 4.0, which is not blanket permission for AI model training or commercial audio reuse.

## Privacy

Use only pseudonymous reviewer codes. The browser's local Export button is a deliberate file save, not an upload. Safeguard exports, avoid identifying speaker information, and delete files when no longer needed. This pilot excludes samples involving minors/vulnerable speakers unless a separate specialist ethics and consent review explicitly authorizes them.

## Release gate

The existing public 30-entry Patois beta remains unchanged. PR #2 stages 30 lexical candidates; PR #4 stages YouTube discovery metadata. This v0.9 pilot adds review infrastructure ONLY. Publication of linguistic observations requires a separate human-approved and rights-cleared change.

## Sources
- YouTube Terms of Service: https://www.youtube.com/t/terms
- YouTube Licence Types: https://support.google.com/youtube/answer/2797468
- Source rights matrix: research/youtube/source_rights_matrix_v0_8.csv
