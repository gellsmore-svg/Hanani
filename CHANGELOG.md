# Changelog

All notable changes to Hanani are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.1] — 2026-08-21

### Changed
- Replace the ``keturah @ git+…`` runtime pin with ``keturah>=0.4.0`` so the
  wheel is index-legal and aligns with Tirzah.

## [0.9.0] — 2026-08-08

Review action for `docs/review-2026-08-08.md` (0.8.0 baseline).

### Fixed
- **H2**: Layer-1 `audit_scores` store `null`/unassessed rather than fabricated
  `True` for all six criteria.
- **H1 / F1**: Offline rhetoric floor expanded with cues for common belief,
  ad hominem, expanded appeal to authority, and circular reasoning (plus
  `fallacy.appeal_to_common_belief` in the vocabulary).
- **F2 / M4**: `hanani rhetoric`, `reasoning`, and `ingest` print declared vs
  offline-detectable coverage instead of taxonomy size alone.
- **F3**: `hanani asssib` distinguishes schema-ready from operationally-wired.
- **F4 / M3**: confirmed non-zero exit when the milcah extra is missing
  (regression test added).
- **M1**: skipped unreadable JSONL lines are counted and shown in `corpus`.
- **L1**: CLAUDE.md test-count handoff note corrected.
- **L2 / M2**: store module documents append atomicity and full-file load limits.

### Added
- `pipeline.offline_cue_keys` / `rhetoric_floor_coverage` helpers.
- Tests for H1 probe sentences, unassessed audit scores, store skip counts,
  CLI coverage wording, debate exit code.

## [0.8.0]

Prior release (see git history).
