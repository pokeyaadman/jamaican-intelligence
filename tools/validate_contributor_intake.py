#!/usr/bin/env python3
"""Validate synthetic/private intake metadata. NEVER publish real intake JSON."""
import argparse
import json
import re
from datetime import date
from pathlib import Path

SCHEMA_PATH = Path("metadata/contributor_intake_schema_v1_0.json")

def validate(record, schema):
    errors=[]
    fields=schema["fields"]
    for k in schema["required"]:
        if not record.get(k):
            errors.append("missing:"+k)
    for key, value in record.items():
        if key not in fields:
            errors.append("unknown_field:"+key)
            continue
        spec=fields[key]
        if "values" in spec and value not in spec["values"]:
            errors.append("invalid_value:"+key)
        if spec.get("type")=="date_iso":
            try: date.fromisoformat(value)
            except (ValueError,TypeError): errors.append("invalid_date:"+key)
        if spec.get("pattern") and not re.fullmatch(spec["pattern"],str(value)):
            errors.append("invalid_format:"+key)
    dataset=record.get("dataset")
    if dataset=="JAM-LANG" and record.get("public_release_decision")=="approved_by_human_reviewer":
        for k in ("original_form","english_gloss","usage_example"):
            if not record.get(k): errors.append("language_publication_missing:"+k)
    if dataset=="JAM-CULT" and record.get("public_release_decision")=="approved_by_human_reviewer":
        if record.get("culture_claim_type") in (None,"not_applicable"):
            errors.append("culture_claim_type_required")
    if dataset=="JAM-BIZ" and record.get("public_release_decision")=="approved_by_human_reviewer":
        if record.get("consent_public_text")!="granted_scope_specific":
            errors.append("business_owner_publication_consent_required")
    if record.get("public_release_decision")=="approved_by_human_reviewer":
        if record.get("rights_status") not in ("verified_scope_specific_grant","public_domain_verified","open_licence_verified"):
            errors.append("publication_rights_unverified")
        if record.get("verification_status")!="human_verified":
            errors.append("human_verification_missing")
        if record.get("consent_evidence_status") not in ("restricted_evidence_recorded","not_applicable_public_source"):
            errors.append("consent_evidence_missing")
        if not record.get("publication_approval_reference"):
            errors.append("approval_reference_missing")
        if record.get("withdrawal_status") in ("requested","actioned"):
            errors.append("withdrawn_or_withdrawing")
    for key in ("consent_ai_training","consent_audio_reuse","consent_redistribution"):
        if record.get(key)=="granted_scope_specific" and record.get("consent_evidence_status")!="restricted_evidence_recorded":
            errors.append("scope_specific_consent_evidence_missing:"+key)
    for key in record:
        if re.search(r"(email|phone|address|birth|government_id|full_name)",key,re.I):
            errors.append("prohibited_sensitive_field:"+key)
    return sorted(set(errors))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--schema",default=str(SCHEMA_PATH))
    p.add_argument("--input",help="Local synthetic or restricted JSON file. Never commit personal data.")
    args=p.parse_args()
    schema=json.loads(Path(args.schema).read_text(encoding="utf-8"))
    if not args.input:
        print(json.dumps({"status":"SCHEMA_LOADED","version":schema["schema_version"],"fields":len(schema["fields"]),"record_count":0}))
        return 0
    payload=json.loads(Path(args.input).read_text(encoding="utf-8"))
    records=payload if isinstance(payload,list) else [payload]
    failures=[{"index":i,"errors":e} for i,r in enumerate(records) if (e:=validate(r,schema))]
    print(json.dumps({"status":"PASS" if not failures else "FAIL","records":len(records),"failures":failures},indent=2))
    return int(bool(failures))
if __name__=="__main__":
    raise SystemExit(main())
