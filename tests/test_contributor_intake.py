import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate_contributor_intake import validate
SCHEMA=json.loads((ROOT/"metadata/contributor_intake_schema_v1_0.json").read_text())

def synthetic():
    return dict(submission_id="SUB-TEST-00001",dataset="JAM-LANG",
      submission_type="lexeme",source_reference="https://example.org/test",
      source_retrieval_date="2026-11-18",last_reviewed_date="2026-11-18",
      rights_status="pending_review",verification_status="unverified",
      confidence="unknown",public_release_decision="hold",
      consent_notice_version="v1.0",consent_evidence_status="missing",
      consent_public_text="not_granted",consent_audio_reuse="not_granted",
      consent_ai_training="not_granted",consent_commercial_reuse="not_granted",
      consent_redistribution="not_granted",withdrawal_status="none")
class TestConsent(unittest.TestCase):
    def test_draft_without_grants(self):
        self.assertEqual(validate(synthetic(),SCHEMA),[])
    def test_no_unverified_publication(self):
        r=synthetic();r["public_release_decision"]="approved_by_human_reviewer"
        self.assertIn("publication_rights_unverified",validate(r,SCHEMA))
    def test_no_training_without_evidence(self):
        r=synthetic();r["consent_ai_training"]="granted_scope_specific"
        self.assertIn("scope_specific_consent_evidence_missing:consent_ai_training",validate(r,SCHEMA))
    def test_no_audio_without_evidence(self):
        r=synthetic();r["consent_audio_reuse"]="granted_scope_specific"
        self.assertIn("scope_specific_consent_evidence_missing:consent_audio_reuse",validate(r,SCHEMA))
    def test_no_private_field(self):
        r=synthetic();r["personal_email"]="person@example.com"
        self.assertIn("prohibited_sensitive_field:personal_email",validate(r,SCHEMA))
    def test_no_business_without_owner_consent(self):
        r=synthetic();r["dataset"]="JAM-BIZ";r["submission_type"]="business_owner_submission"
        r["public_release_decision"]="approved_by_human_reviewer"
        self.assertIn("business_owner_publication_consent_required",validate(r,SCHEMA))
if __name__=="__main__":unittest.main()
