#!/usr/bin/env python3
"""Validate Jamaican Intelligence YouTube source discovery register.

This gate checks discoverable metadata and release restrictions.
It never certifies actual speech content, creator rights, or consent.
"""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SRC = Path("research/youtube/speech_source_candidates_v0_8.csv")
OBS = Path("research/youtube/observation_intake_template.csv")
MINIMUM = 8
MANDATORY = {
    "source_id", "item_type", "video_id", "url", "creator_channel",
    "public_title", "genre", "scope", "discovery_evidence_url",
    "metadata_checked_date", "speech_review_status", "licence_notice",
    "transcript_reuse_permission", "audio_download_permission",
    "ai_training_permission", "speaker_consent_status",
    "research_priority", "record_status",
}
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)

def main(base):
    root = Path(base)
    errors = []
    fields, rows = read(root/SRC)
    obfields, observations = read(root/OBS)
    for missing in sorted(MANDATORY - set(fields)):
        errors.append("missing_column:" + missing)
    if len(rows) < MINIMUM:
        errors.append("too_few_source_leads")
    seen_ids, seen_links = set(), set()
    kinds = {"video":0, "channel":0}
    for i, r in enumerate(rows, 2):
        rid = r.get("source_id","")
        kind = r.get("item_type","")
        url = r.get("url","")
        if not rid.startswith("YT-") or rid in seen_ids:
            errors.append(f"row_{i}:invalid_or_duplicate_record_id")
        if url in seen_links:
            errors.append(f"row_{i}:duplicate_source_url")
        seen_ids.add(rid); seen_links.add(url)
        if kind not in kinds:
            errors.append(f"row_{i}:unknown_item_type")
        else: kinds[kind]+=1
        parsed=urlparse(url)
        if parsed.scheme!="https" or parsed.netloc.lower() not in {"www.youtube.com","youtube.com"}:
            errors.append(f"row_{i}:unexpected_source_host")
        if kind=="video":
            vid=r.get("video_id","")
            if not VIDEO_ID.fullmatch(vid):
                errors.append(f"row_{i}:invalid_video_id")
            if parsed.path!="/watch" or parse_qs(parsed.query).get("v") != [vid]:
                errors.append(f"row_{i}:video_url_id_mismatch")
            if r.get("speech_review_status")!="not_listened":
                errors.append(f"row_{i}:unsupported_speech_review_claim")
            if r.get("record_status")!="metadata_only":
                errors.append(f"row_{i}:video_not_discovery_only")
        elif kind=="channel":
            if r.get("video_id"):
                errors.append(f"row_{i}:channel_with_video_id")
            if not parsed.path.startswith("/@"):
                errors.append(f"row_{i}:channel_url_not_handle")
            if r.get("record_status")!="channel_discovery_only":
                errors.append(f"row_{i}:channel_not_discovery_only")
            if r.get("speech_review_status")!="not_applicable":
                errors.append(f"row_{i}:channel_bad_listening_status")
        for fld in ("transcript_reuse_permission","audio_download_permission","ai_training_permission"):
            if r.get(fld)!="not_granted":
                errors.append(f"row_{i}:{fld}_must_remain_not_granted_without_evidence")
        if r.get("speaker_consent_status")!="not_assessed":
            errors.append(f"row_{i}:unsourced_speaker_consent")
        if not r.get("creator_channel") or not r.get("public_title") or not r.get("discovery_evidence_url"):
            errors.append(f"row_{i}:missing_provenance")
        try:
            date.fromisoformat(r.get("metadata_checked_date",""))
        except (TypeError,ValueError):
            errors.append(f"row_{i}:invalid_metadata_check_date")
        if r.get("licence_notice")=="CC-BY-NC-4.0_in_description" and r.get("video_id")!="k7Earnq8sHw":
            errors.append(f"row_{i}:licence_notice_unsubstantiated_by_registry")
    if kinds["video"]<6 or kinds["channel"]<2:
        errors.append("unexpected_video_or_channel_counts")
    if observations:
        errors.append("intake_template_not_empty_release_prohibited")
    for req in ("observation_id","source_id","timestamp_seconds","original_nonverbatim_note",
                "actual_playback_confirmed","release_decision"):
        if req not in obfields:errors.append("missing_intake_column:"+req)
    status="PASS" if not errors else "FAIL"
    print(json.dumps({
        "status":status,
        "stage":"metadata_discovery_only",
        "video_leads":kinds["video"],
        "channel_leads":kinds["channel"],
        "observations_from_youtube":len(observations),
        "transcripts_or_audio_included":0,
        "verified_licensed_speech_samples":0,
        "disclaimer":"Automated checks cannot verify YouTube licence rights, the presence of speech, speaker consent or AI training rights.",
        "errors":errors
    },indent=2))
    return 1 if errors else 0

if __name__=="__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else "."))
