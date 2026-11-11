#!/usr/bin/env python3
"""Cross-check public YouTube source metadata against rights decisions.
This enforces conservative data-state consistency, not legal sufficiency of licences.
"""
import csv
import json
import sys
from pathlib import Path
from datetime import date

BASE=Path("research/youtube")
SOURCE=BASE/"speech_source_candidates_v0_8.csv"
RIGHTS=BASE/"source_rights_matrix_v0_8.csv"
RIGHT_COLS=(
 "transcript_storage_permission",
 "transcript_public_release_permission",
 "audio_download_permission",
 "audio_public_release_permission",
 "text_ai_training_permission",
 "speech_ai_training_permission",
 "commercial_reuse_permission",
)
OUTREACH={"unrequested","requested_pending","clarification_needed",
          "granted_limited","declined","withdrawn","expired"}
def records(filename):
    with filename.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def main(root):
    p=Path(root)
    sources=records(p/SOURCE)
    decisions=records(p/RIGHTS)
    errors=[]
    source_ids={s.get("source_id","") for s in sources}
    decision_ids={d.get("source_id","") for d in decisions}
    if len(decision_ids)!=len(decisions):errors.append("duplicate_rights_ids")
    if source_ids!=decision_ids:
        errors.append("source_rights_ids_do_not_match")
    if len(sources)!=8: errors.append("expected_8_discovery_sources")
    for r in decisions:
        rid=r.get("source_id","")
        status=r.get("outreach_status","")
        if status not in OUTREACH:errors.append(rid+":invalid_outreach_status")
        if r.get("source_citation_allowed")!="yes_link_only":
            errors.append(rid+":unsupported_citation_claim")
        if status=="requested_pending" and not r.get("last_outreach_date"):
            errors.append(rid+":missing_outreach_date")
        if status=="unrequested" and r.get("last_outreach_date"):
            errors.append(rid+":unrequested_date_conflict")
        if r.get("last_outreach_date"):
            try:date.fromisoformat(r["last_outreach_date"])
            except ValueError:errors.append(rid+":invalid_outreach_date")
        for col in RIGHT_COLS:
            v=r.get(col)
            if v not in ("not_granted","granted"):
                errors.append(rid+":"+col+"_invalid_status")
            if v=="granted":
                if not r.get("rights_evidence_reference"):
                    errors.append(rid+":"+col+"_missing_evidence")
                if status not in ("granted_limited",):
                    errors.append(rid+":"+col+"_inconsistent_outreach_status")
                if col in ("audio_download_permission","audio_public_release_permission","speech_ai_training_permission") and r.get("speaker_participant_consent")!="documented":
                    errors.append(rid+":"+col+"_requires_participant_consent_review")
        if r.get("source_citation_allowed")=="yes_link_only":
            # A public URL is not permission to republish the media or a transcript.
            if not r.get("status_checked_date"):
                errors.append(rid+":missing_checked_date")
        if status=="requested_pending" and any(r.get(c)=="granted" for c in RIGHT_COLS):
            errors.append(rid+":pending_cannot_be_granted")
    result={"status":"PASS" if not errors else "FAIL",
            "source_count":len(sources),
            "rights_rows":len(decisions),
            "requested_pending_source_count":sum(r.get("outreach_status")=="requested_pending" for r in decisions),
            "rights_granted_count":sum(r.get(c)=="granted" for r in decisions for c in RIGHT_COLS),
            "not_a_legal_opinion":True,
            "errors":errors}
    print(json.dumps(result,indent=2))
    return 1 if errors else 0

if __name__=="__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else "."))
