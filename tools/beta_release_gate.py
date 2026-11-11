#!/usr/bin/env python3
"""Validate Jamaican Intelligence's provisional lexical preview.
Passing this check proves metadata/attribution completeness, NOT external linguistic accuracy.
"""
import csv, json, sys
from pathlib import Path
from datetime import date

REQUIRED=["record_id","headword_or_phrase","meaning_en","source_id","source_url",
"retrieved_date","licence_status","licence_url","verification_class",
"owner_attestation_id","independent_linguistic_review","release_stage"]
def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    f=root/"data"/"JAM-LANG.csv"
    with f.open(encoding="utf-8-sig",newline="") as inp:
        rd=csv.DictReader(inp); rows=list(rd); cols=rd.fieldnames or []
    errors=[]; seen=set()
    if not rows:errors.append("preview_is_empty")
    for field in REQUIRED:
        if field not in cols:errors.append("missing_column_"+field)
    for i,r in enumerate(rows,2):
        rid=r.get("record_id","")
        for field in REQUIRED:
            if not r.get(field):errors.append(f"row_{i}:{field}_blank")
        if rid in seen:errors.append(f"row_{i}:duplicate_id")
        seen.add(rid)
        if r.get("licence_status")!="CC-BY-SA-4.0":errors.append(f"row_{i}:bad_license")
        if r.get("licence_url")!="https://creativecommons.org/licenses/by-sa/4.0/":errors.append(f"row_{i}:bad_license_url")
        if r.get("source_url")!="https://en.wiktionary.org/wiki/Appendix:Jamaican_Creole_Swadesh_list":
            errors.append(f"row_{i}:unexpected_source")
        if r.get("verification_class")!="owner_verified":errors.append(f"row_{i}:not_owner_attested")
        if r.get("independent_linguistic_review")!="pending":errors.append(f"row_{i}:expert_status_misleading")
        if r.get("release_stage")!="owner_attested_beta":errors.append(f"row_{i}:not_beta")
        try:date.fromisoformat(r.get("retrieved_date",""))
        except ValueError:errors.append(f"row_{i}:bad_date")
    for name in ["JAM-CULT","JAM-BIZ"]:
        with (root/"data"/f"{name}.csv").open(encoding="utf-8-sig",newline="") as fp:
            excluded=list(csv.DictReader(fp))
        if excluded:errors.append(f"unauthorised_{name}_rows:{len(excluded)}")
    outcome={"stage":"owner_attested_beta","lexical_records":len(rows),
             "institutional_review":"pending","business_and_culture_public_records":0,
             "metadata_status":"PASS" if not errors else "FAIL",
             "qualification":"A passing script does not prove linguistic accuracy, expert verification, or publication online.",
             "errors":errors[:50]}
    print(json.dumps(outcome,indent=2))
    return 1 if errors else 0
if __name__=="__main__":sys.exit(main())
