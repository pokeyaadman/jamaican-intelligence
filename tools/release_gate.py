#!/usr/bin/env python3
"""Offline approval gate for Jamaican Intelligence production CSV exports.
Designed to fail closed; a missing approval log never authorizes publication.
This does not perform human, legal, privacy or factual review.
"""
import argparse, csv, json, sys
from pathlib import Path
from datetime import date

DATASETS = {
  "JAM-LANG": {"reviewer":"reviewer_id","date":"last_reviewed_date","status":"verification_status","rights":"licence_status","source":"source_id"},
  "JAM-CULT": {"reviewer":"reviewer_id","date":"last_reviewed_date","status":"verification_status","rights":"licence_status","source":"source_id"},
  "JAM-BIZ": {"reviewer":"reviewer_id","date":"last_verified_date","status":"verification_status","rights":"licence_status","source":"source_id"},
}
RIGHTS = {"open_licence","permission_granted","public_domain_confirmed"}
APPROVAL_KEYS = ("subject_review_approved","rights_review_approved","privacy_review_approved","release_manager_approved")

def read_rows(path):
    if not path.exists():
        raise RuntimeError(f"Missing file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def approved(value):
    return str(value or "").strip().lower() in {"yes","true","1","approved"}

def iso_date(value):
    try:
        date.fromisoformat(value)
        return True
    except (TypeError,ValueError):
        return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".",help="repository root")
    p.add_argument("--approval-log",default="",help="PRIVATE sign-off CSV; keep outside public repository")
    p.add_argument("--require-records",action="store_true",help="reject empty release")
    args=p.parse_args()
    root=Path(args.root)
    approvals={}
    if args.approval_log:
        for a in read_rows(Path(args.approval_log)):
            if a.get("record_id"):
                approvals[a["record_id"]]=a

    errors=[]; counts={}
    all_ids=set()
    for name,cols in DATASETS.items():
        rows=read_rows(root/"data"/(name+".csv"))
        counts[name]=len(rows)
        for row in rows:
            rid=row.get("record_id","").strip()
            why=[]
            if not rid or rid in all_ids: why.append("missing_or_duplicate_record_id")
            all_ids.add(rid)
            if row.get(cols["status"])!="verified": why.append("not_human_verified")
            if not row.get(cols["reviewer"]): why.append("reviewer_missing")
            if not iso_date(row.get(cols["date"])): why.append("review_date_missing_or_invalid")
            if not row.get(cols["source"]): why.append("provenance_missing")
            if row.get(cols["rights"]) not in RIGHTS: why.append("reuse_rights_not_cleared")
            if name=="JAM-BIZ":
                if row.get("operating_status")!="confirmed_operating":
                    why.append("current_operation_not_confirmed")
                if not iso_date(row.get("last_verified_date")):
                    why.append("business_verification_date_missing")
            if name=="JAM-LANG" and not row.get("permission_reference"):
                why.append("linguistic_attribution_or_license_reference_missing")

            approval=approvals.get(rid)
            if not approval:
                why.append("signed_approval_log_entry_missing")
            else:
                for k in APPROVAL_KEYS:
                    if not approved(approval.get(k)): why.append(k+"_missing")
                if approval.get("reviewer_id")!=row.get(cols["reviewer"]):
                    why.append("reviewer_id_not_matched")
                if approval.get("reviewed_date")!=row.get(cols["date"]):
                    why.append("review_date_not_matched")
                if name=="JAM-BIZ":
                    if not approval.get("business_operating_evidence"):
                        why.append("operating_evidence_missing")
            if why:
                errors.append({"record_id":rid,"dataset":name,"reasons":why})

    total=sum(counts.values())
    if args.require_records and total==0:
        errors.append({"reason":"empty_release"})
    outcome={"version":"0.5","total_records":total,"dataset_counts":counts,
             "invalid_records":len(errors),"status":"PASS" if not errors else "FAIL",
             "publication_warning":"PASS only means field gates passed; it is not independent proof of actual external review."}
    print(json.dumps(outcome, indent=2))
    if errors: print(json.dumps({"errors":errors[:50]},indent=2),file=sys.stderr)
    if total==0: print("INFO: metadata-only package; no production records.",file=sys.stderr)
    return 1 if errors else 0

if __name__=="__main__":
    sys.exit(main())
