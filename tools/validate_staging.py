#!/usr/bin/env python3
"""Fail-closed validation for Jamaican Creole STAGING candidates, not linguistic certification."""
import csv
import json
import sys
from pathlib import Path

SOURCE_URL = "https://en.wiktionary.org/wiki/Appendix:Jamaican_Creole_Swadesh_list"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
EXPECTED = {
 19:"sum",20:"kopl",21:"anieda",25:"fuo",26:"faib",27:"laaj",29:"waid",
 31:"hebi",32:"smaal",33:"shaat",34:"naro",35:"liin",38:"piipl",
 40:"waif",41:"ozban",44:"animal",45:"fish",46:"bod",49:"siniek",
 50:"worm",52:"faris",53:"tik",55:"siid",56:"liif",57:"ruut",
 58:"baak",59:"flowaz",60:"graas",61:"ruop",62:"skin"
}
NEEDED = {
 "record_id","headword_or_phrase","meaning_en","part_of_speech","source_id",
 "source_url","retrieved_date","licence_status","licence_url","verification_class",
 "owner_attestation_id","independent_linguistic_review","release_stage","source_list_number"
}
def load(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)
def main(root):
    base = Path(root)
    headers, rows = load(base/"staging"/"JAM-LANG-candidates-v0.7.csv")
    _, published = load(base/"data"/"JAM-LANG.csv")
    taken = {r["record_id"] for r in published}
    public_forms = {r["headword_or_phrase"].casefold() for r in published}
    errors=[]
    for missing in NEEDED-set(headers):
        errors.append("missing_column:"+missing)
    if len(rows)!=30:
        errors.append("expected_30_candidates")
    seen_ids=set(); seen_forms=set(); seen_source_numbers=set()
    for n,r in enumerate(rows, start=31):
        record=r.get("record_id","")
        form=r.get("headword_or_phrase","")
        key=form.casefold()
        srcnum=r.get("source_list_number","")
        if record!=f"LANG-{n:06d}": errors.append(record+":unexpected_id")
        if record in seen_ids or record in taken: errors.append(record+":duplicate_id")
        if key in public_forms or key in seen_forms: errors.append(record+":duplicate_headword")
        if not r.get("meaning_en") or not r.get("part_of_speech"): errors.append(record+":missing_gloss_or_pos")
        if r.get("source_id")!="SRC-0019" or r.get("source_url")!=SOURCE_URL:errors.append(record+":wrong_source")
        if r.get("licence_status")!="CC-BY-SA-4.0" or r.get("licence_url")!=LICENSE_URL:errors.append(record+":wrong_license")
        if r.get("verification_class")!="source_checked_unreviewed":errors.append(record+":premature_verification")
        if r.get("owner_attestation_id"):errors.append(record+":unexpected_owner_attestation")
        if r.get("independent_linguistic_review")!="pending":errors.append(record+":invalid_expert_status")
        if r.get("release_stage")!="staging_only":errors.append(record+":unexpected_release_stage")
        if not r.get("retrieved_date"):errors.append(record+":missing_retrieval_date")
        try:
            list_number=int(srcnum)
        except (ValueError,TypeError):
            errors.append(record+":invalid_source_index")
            list_number=-1
        if EXPECTED.get(list_number)!=form: errors.append(record+":unmatched_source_index_and_form")
        if list_number in seen_source_numbers: errors.append(record+":duplicate_source_index")
        seen_ids.add(record); seen_forms.add(key); seen_source_numbers.add(list_number)
    result={"status":"PASS" if not errors else "FAIL",
            "stage":"source_checked_unreviewed",
            "candidate_count":len(rows),
            "existing_published_count":len(published),
            "expert_reviews_received_for_candidates":0,
            "warning":"This validates file structure, review labeling and source transcription only; human linguistic approval remains necessary.",
            "errors":errors}
    print(json.dumps(result,indent=2))
    return 1 if errors else 0
if __name__=="__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else "."))
