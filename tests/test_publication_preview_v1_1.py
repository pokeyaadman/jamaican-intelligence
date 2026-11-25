import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from publication_preview_v1_1 import preview

def fixture():
    return dict(submission_id="SUB-TEST-001", dataset="JAM-LANG", submission_type="lexeme", original_form="SYNTHETIC", english_gloss="TEST ONLY", usage_example="TEST ONLY", source_reference="https://example.invalid/test", source_retrieval_date="2026-11-18", last_reviewed_date="2026-11-25", rights_status="open_licence_verified", verification_status="human_verified", confidence="high", public_release_decision="approved_by_human_reviewer", consent_notice_version="TEST", consent_evidence_status="not_applicable_public_source", publication_approval_reference="TEST-PRIVATE", reviewer_code="TEST", withdrawal_status="not_applicable")

class GateTests(unittest.TestCase):
    def test_projection(self):
        result=preview(fixture(),synthetic=True)
        self.assertEqual(result["status"],"synthetic_preview_only")
        self.assertFalse(result["publication_authorized"])
        for key in ("submission_id","reviewer_code","publication_approval_reference","consent_evidence_status"):
            self.assertNotIn(key,result["public_preview"])
    def test_block_cases(self):
        for change in (dict(withdrawal_status="requested"),dict(rights_status="pending_review"),dict(public_release_decision="hold"),dict(source_reference="https://example.invalid/?token=secret"),dict(confidence="low"),dict(dataset="JAM-CULT"),dict(last_reviewed_date="2026-11-17"),dict(rights_status="verified_scope_specific_grant"),dict(dataset="JAM-BIZ",submission_type="business_owner_submission")):
            with self.subTest(change=change):
                self.assertEqual(preview(dict(fixture(),**change),synthetic=True)["status"],"hold")
    def test_real_input_blocked(self):
        with self.assertRaises(ValueError): preview(fixture())
        with self.assertRaises(ValueError): preview(dict(fixture(),submission_id="SUB-REAL-001"),synthetic=True)
