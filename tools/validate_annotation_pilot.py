#!/usr/bin/env python3
"""Validate local human-review CSVs and the annotation tool configuration.

This program checks metadata consistency only. It cannot listen to videos,
authenticate reviewers, or certify copyrights, consent, or linguistic accuracy.
Observation CSVs should stay in restricted storage, NOT public GitHub.
"""
import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

FIELDS = {
    "observation_id", "source_id", "video_id", "timestamp_seconds",
    "observed_lexeme_or_feature", "original_nonverbatim_note",
    "usage_register", "code_switching_observed", "reviewer_role",
    "reviewed_date", "actual_playback_confirmed", "transcript_reuse_permission",
    "original_audio_permission", "ai_training_permission",
    "second_source_reference", "independent_linguistic_review",
    "privacy_assessment", "release_decision", "restricted_evidence_reference",
    "linguistic_category", "reviewer_code",
}
ROLES = {"research_assistant", "native_speaker", "linguist", "other"}
CATEGORIES = {"vocabulary", "grammar", "phonology", "code_switching", "discourse", "other"}
REGISTERS = {"unknown", "informal_conversation", "interview", "education", "scripted", "other"}
EMAIL = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.I)
PHONE = re.compile(r"(?:\+?\d[\s().-]*){8,}")

def load_csv(file):
    with Path(file).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return set(reader.fieldnames or []), list(reader)

def load_video_registry(root):
    _, rows = load_csv(Path(root) / "research/youtube/speech_source_candidates_v0_8.csv")
    videos = {r["source_id"]: r["video_id"] for r in rows if r["item_type"] == "video"}
    if len(videos) != 6 or len(rows) != 8:
        raise ValueError("expected six video leads and two channel leads")
    return videos

def validate_row(r, videos):
    issues = []
    record = r.get("observation_id", "")
    source = r.get("source_id", "")
    note = r.get("original_nonverbatim_note", "").strip()
    feature = r.get("observed_lexeme_or_feature", "").strip()
    if not record.startswith("OBS-"):
        issues.append("invalid_observation_id")
    if source not in videos or r.get("video_id") != videos.get(source):
        issues.append("unregistered_video_or_id_mismatch")
    try:
        second = int(r.get("timestamp_seconds", ""))
        if not (0 <= second <= 86400):
            issues.append("timestamp_out_of_bounds")
    except ValueError:
        issues.append("timestamp_not_an_integer")
    if not 2 <= len(feature) <= 100:
        issues.append("feature_length_out_of_bounds")
    if not 20 <= len(note) <= 240:
        issues.append("nonverbatim_note_length_out_of_bounds")
    if EMAIL.search(feature + " " + note) or PHONE.search(feature + " " + note):
        issues.append("possible_personal_identifier")
    if r.get("reviewer_role") not in ROLES:
        issues.append("invalid_reviewer_role")
    if r.get("linguistic_category") not in CATEGORIES:
        issues.append("invalid_linguistic_category")
    if r.get("usage_register") not in REGISTERS:
        issues.append("invalid_usage_register")
    if r.get("code_switching_observed") not in {"yes", "no", "uncertain"}:
        issues.append("invalid_code_switching_value")
    if not re.fullmatch(r"[A-Za-z0-9_-]{2,16}", r.get("reviewer_code", "")):
        issues.append("invalid_anonymous_reviewer_code")
    try:
        date.fromisoformat(r.get("reviewed_date", ""))
    except ValueError:
        issues.append("invalid_review_date")
    if r.get("actual_playback_confirmed") != "yes":
        issues.append("playback_not_confirmed")
    for field in ("transcript_reuse_permission", "original_audio_permission", "ai_training_permission"):
        if r.get(field) != "not_granted":
            issues.append(field + "_unexpected_grant")
    for name, expected in (
        ("independent_linguistic_review", "pending"),
        ("privacy_assessment", "pending_manual_review"),
        ("release_decision", "hold_review_pending"),
    ):
        if r.get(name) != expected:
            issues.append(name + "_premature_approval")
    if r.get("restricted_evidence_reference"):
        issues.append("private_evidence_reference_not_for_public_staging")
    ref = r.get("second_source_reference", "")
    if ref:
        parsed = urlparse(ref)
        if parsed.scheme != "https" or not parsed.netloc:
            issues.append("second_source_must_be_public_https_url")
    return issues

def validate_workbench(root):
    root=Path(root)
    _,source_rows=load_csv(root/"research/youtube/speech_source_candidates_v0_8.csv")
    videos=load_video_registry(root)
    js=(root/"research/youtube/annotation_workbench.js").read_text(encoding="utf-8")
    html=(root/"research/youtube/annotation_workbench.html").read_text(encoding="utf-8")
    match = dict(re.findall(r'id:"(YT-\d{4})",\s*video:"([A-Za-z0-9_-]{11})"', js))
    errors=[]
    if match != videos:
        errors.append("workbench_video_links_do_not_match_source_registry")
    if 'src="./annotation_workbench.js"' not in html:
        errors.append("workbench_script_not_linked")
    for key in ("hold_review_pending", "pending_manual_review", "not_granted"):
        if key not in js:
            errors.append("missing_hold_state_"+key)
    # Releasing CSVs of observations to GitHub is not authorized by this phase.
    forbidden = list((root/"research/youtube/reviewer_exports").glob("*.csv"))
    if forbidden:
        errors.append("reviewer_exports_must_be_kept_out_of_public_repository")
    return videos, errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", help="Private reviewer CSV to inspect; do not commit it to GitHub")
    args=parser.parse_args()
    try:
        videos,errors=validate_workbench(args.root)
    except (OSError,ValueError) as e:
        print(json.dumps({"status":"FAIL", "errors":[str(e)]}))
        return 1
    total=0
    if args.input:
        try:
            headers, rows = load_csv(args.input)
        except OSError as e:
            print(json.dumps({"status":"FAIL","errors":[str(e)]}))
            return 1
        total=len(rows)
        for col in sorted(FIELDS-headers):
            errors.append("missing_column:"+col)
        seen=set()
        if not rows:
            errors.append("no_review_observations")
        for i,row in enumerate(rows,2):
            rid=row.get("observation_id","")
            if rid in seen: errors.append("duplicate_observation_id:"+rid)
            seen.add(rid)
            errors.extend("line_"+str(i)+":"+e for e in validate_row(row,videos))
    print(json.dumps({
        "status":"PASS" if not errors else "FAIL",
        "configured_videos":len(videos),
        "reviewer_observations_checked":total,
        "production_releases_authorized":0,
        "warning":"A passing check does not prove a recording was played, consent was granted, speech was accurate, or a reviewer is qualified.",
        "errors":errors
    },indent=2))
    return bool(errors)

if __name__=="__main__":
    raise SystemExit(main())
