#!/usr/bin/env python3
"""Synthetic unit tests only. No actual recordings or speech are present."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_annotation_pilot as validator

def test_row():
    return {
        "observation_id":"OBS-SYNTHETIC-001",
        "source_id":"YT-0001",
        "video_id":"xLas9oA1SFw",
        "timestamp_seconds":"12",
        "observed_lexeme_or_feature":"hypothetical grammar feature",
        "original_nonverbatim_note":"Synthetic test note; not derived from or attributed to any video recording.",
        "usage_register":"unknown",
        "code_switching_observed":"uncertain",
        "reviewer_role":"research_assistant",
        "reviewed_date":"2026-11-11",
        "actual_playback_confirmed":"yes",
        "transcript_reuse_permission":"not_granted",
        "original_audio_permission":"not_granted",
        "ai_training_permission":"not_granted",
        "second_source_reference":"",
        "independent_linguistic_review":"pending",
        "privacy_assessment":"pending_manual_review",
        "release_decision":"hold_review_pending",
        "restricted_evidence_reference":"",
        "linguistic_category":"grammar",
        "reviewer_code":"TEST_001"
    }

class TestReviewGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.videos,cls.config_errors=validator.validate_workbench(ROOT)

    def test_accurate_video_registry(self):
        self.assertEqual(len(self.videos),6)
        self.assertEqual(self.config_errors,[])

    def test_synthetic_record_metadata_is_valid(self):
        self.assertEqual(validator.validate_row(test_row(),self.videos),[])

    def test_unapproved_ai_training_is_blocked(self):
        row=test_row()
        row["ai_training_permission"]="granted"
        self.assertTrue(any("ai_training_permission" in error
                            for error in validator.validate_row(row,self.videos)))

    def test_mislabelled_release_is_blocked(self):
        row=test_row()
        row["release_decision"]="publish"
        self.assertIn("release_decision_premature_approval",
                      validator.validate_row(row,self.videos))

    def test_unknown_video_is_blocked(self):
        row=test_row()
        row["source_id"]="YT-9999"
        self.assertIn("unregistered_video_or_id_mismatch",
                      validator.validate_row(row,self.videos))

    def test_personal_email_is_blocked(self):
        row=test_row()
        row["original_nonverbatim_note"]+=" Someone's email is hidden@example.com"
        self.assertIn("possible_personal_identifier",
                      validator.validate_row(row,self.videos))

    def test_fake_playback_not_confirmed_is_blocked(self):
        row=test_row()
        row["actual_playback_confirmed"]="no"
        self.assertIn("playback_not_confirmed",
                      validator.validate_row(row,self.videos))

if __name__=="__main__":
    unittest.main()
