# Public-Release Checklist

This checklist is a gate, not proof that release is safe.

## Content and privacy

- [x] No personal names, email addresses, phone numbers or home/work paths remain in the public tree; the repository URL is an intentional public pointer.
- [x] No private correspondence, schedules, timetables or deadline records remain.
- [x] No participant identities, consent records, raw recordings or identifiable images remain.
- [x] No official PDFs, assessment forms, guidance videos or displayed student examples are bundled.
- [x] Synthetic examples are clearly labelled as synthetic.
- [x] User-owned Managed Workspaces are separate from the reusable core.
- [x] Optional packs are explicitly identified, and the GSA Pack is described as independent rather than institutionally endorsed.

## Provenance and licensing

- [x] Every retained source has a provenance note or source locator.
- [x] Course-derived notes have a deliberate publication decision for this public edition.
- [x] Assessment guides and reflection-video protocols are operational paraphrases; no official PDFs, videos or student examples are bundled.
- [ ] Public papers and images have compatible reuse terms or are cited without redistribution.
- [x] The selected code/documentation licence is recorded.
- [x] The project is described as independent and not institutionally endorsed.

## Technical review

- [x] No absolute local paths or secrets remain in the public tree.
- [x] A clean clone can follow `docs/QUICKSTART.md` for the core workflow.
- [x] Core scripts run without private directories; OCR index dependencies are optional.
- [x] Links in README and documentation resolve.
- [x] Generated files, caches and dependencies are ignored.
- [x] The public branch is created from the cleaned tree rather than publishing the earlier private source-derived history.

## Final decision

Release status: v0.2.0 released and verified on the public `main` branch and GitHub release

Release: https://github.com/51younglowkey/Threading/releases/tag/v0.2.0

Reviewer:

Date:

- Optional OCR dependencies are intentionally not part of the core installation.
- Future updates must repeat the privacy, provenance and Git-history review.
