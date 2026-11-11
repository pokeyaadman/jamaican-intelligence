# Review workflow — v0.5

1. **Collection:** collect original contribution or licensed source; store URL, retrieved date and terms.
2. **Source check:** independently compare primary facts; record source relationships (same publisher vs second institution).
3. **Subject-matter review:** credentialed/fluent expert checks Patois, qualified cultural reviewer checks history/heritage,
   business owner or independent evidence confirms active trading. A named reviewer accepts responsibility.
4. **Rights and privacy:** clear reuse rights; preserve CC BY-SA for adapted Wiktionary content;
   avoid third-party audio and protected archives; review Data Protection Act issues.
5. **Approval log:** retain confidential `record_id`, four explicit approvals, reviewer ID/date,
   and business operating evidence where applicable. Never put signed documents or IDs in public exports.
6. **Publication:** run fail-closed `tools/release_gate.py` against release data with private signoff log;
   require both an automated pass and a real release manager's approval.
7. **Maintenance:** issue a versioned changelog, expose corrections/takedown route,
   recheck business status and preserve old versions with restrictions.

**No source appearance check or AI output is a substitute for a human approval or ownership permission.**
