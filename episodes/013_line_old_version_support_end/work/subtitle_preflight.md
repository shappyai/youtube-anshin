# Subtitle preflight

Episode: 013_line_old_version_support_end
Cues: 74
Safe width: 1800px (72px font measurement when available)

## FAIL

- なし

## WARN

- なし

## tts_reading_leakage

- result: PASS
- fail count: 0

## japanese_semantic_line_break

- policy: sentence meaning > bunsetsu integrity > modifier relation > visual balance > 72px
- long cues are split in time; font is not reduced to force a fit
- unnatural_japanese_line_break: 0
- word_split: 0
- conjugation_split: 0
- particle_or_auxiliary_orphan: 0
- orphan_particle_auxiliary: 0
- result: PASS

## Summary

- result: PASS
- fail count: 0
- warn count: 0
- cue text is read from episode.json; no character-count auto-splitting is performed
