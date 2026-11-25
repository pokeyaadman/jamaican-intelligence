"""Synthetic-only release preview. No real intake, network, or publication."""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from validate_contributor_intake import validate

SCHEMA = Path(__file__).resolve().parents[1] / "metadata/contributor_intake_schema_v1_0.json"
TYPES = {"JAM-LANG": {"lexeme", "grammar"}, "JAM-CULT": {"oral_tradition", "documented_history", "contemporary_practice"}, "JAM-BIZ": {"business_owner_submission"}}
PUBLIC = ("dataset", "submission_type", "original_form", "english_gloss", "usage_context", "usage_example", "culture_claim_type", "business_registration_status", "business_operating_status", "source_reference", "source_retrieval_date", "last_reviewed_date", "rights_status", "verification_status", "confidence")

def preview(record, *, synthetic=False):
    if synthetic is not True or not isinstance(record, dict):
        raise ValueError("synthetic dictionaries only")
    if not str(record.get("submission_id", "")).startswith("SUB-TEST-"):
        raise ValueError("synthetic ID required")
    if any(not isinstance(v, str) for v in record.values()):
        raise ValueError("string fields only")
    schema = json.loads(SCHEMA.read_text())
    errors = validate(record, schema)
    if record.get("submission_type") not in TYPES.get(record.get("dataset"), set()):
        errors.append("dataset_type_mismatch")
    if record.get("public_release_decision") != "approved_by_human_reviewer":
        errors.append("release_not_approved")
    if record.get("withdrawal_status") not in ("none", "not_applicable"):
        errors.append("withdrawal_status_missing_or_blocked")
    if record.get("confidence") not in ("medium", "high"):
        errors.append("confidence_insufficient")
    try:
        retrieved = date.fromisoformat(record["source_retrieval_date"])
        reviewed = date.fromisoformat(record["last_reviewed_date"])
        if not retrieved <= reviewed <= date.today():
            errors.append("invalid_date_order")
    except (ValueError, KeyError):
        errors.append("invalid_dates")
    url = urlsplit(record.get("source_reference", ""))
    if url.scheme != "https" or url.hostname != "example.invalid" or url.username or url.password or url.query or url.fragment:
        errors.append("synthetic_public_source_required")
    if record.get("rights_status") == "verified_scope_specific_grant":
        for field in ("consent_public_text", "consent_redistribution"):
            if record.get(field) != "granted_scope_specific":
                errors.append("missing_scope:"+field)
        if record.get("consent_evidence_status") != "restricted_evidence_recorded":
            errors.append("missing_restricted_evidence")
    if record.get("dataset") == "JAM-BIZ":
        if record.get("consent_evidence_status") != "restricted_evidence_recorded":
            errors.append("owner_evidence_required")
        # v1.0 lacks business identity and independent verification evidence fields.
        errors.append("business_schema_incomplete")
    if record.get("dataset") == "JAM-CULT":
        # v1.0 lacks a culture description and community clearance evidence fields.
        errors.append("culture_schema_incomplete")
    if errors:
        return {"status":"hold", "errors":sorted(set(errors)), "public_preview":None}
    return {"status":"synthetic_preview_only", "public_preview":{k:record[k] for k in PUBLIC if k in record}, "publication_authorized":False}
