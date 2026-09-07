# Viewer-facing internal brand promise QA

- rule: `viewer_facing_internal_brand_promise`
- classification: `INTERNAL_ONLY`
- viewer-facing expected count: `0`
- viewer-facing count: `3`
- status: **FAIL**

Internal planning/brand documents may contain the phrase. Viewer-facing scene text, prompts/text specs, subtitles, narration, CTA, thumbnail/end-card metadata, and overlay candidates may not.

## episode: C:\Codex\260829_youtube-anshin\episodes\002_myna_app\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests

### Violations
- `C:\Codex\260829_youtube-anshin\episodes\002_myna_app\episode.json` `scene[34].main_message`

## episode: C:\Codex\260829_youtube-anshin\episodes\003_line_renewal\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\004_nise_keisatsu\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\005_google_photos_delete\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\006_line_talk_backup\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests

### Violations
- `C:\Codex\260829_youtube-anshin\episodes\006_line_talk_backup\script.md` `file`

## episode: C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests

### Violations
- `C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login\script.md` `file`

## episode: C:\Codex\260829_youtube-anshin\episodes\008_investment_scam\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\009_windows11_24h2_support\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\010_myna_app_registration\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\011_myna_insurance_scam_call\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## episode: C:\Codex\260829_youtube-anshin\episodes\014_chiikawa_fleamarket_safety\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: script, subtitle, and overlay files
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none

## short: C:\Codex\260829_youtube-anshin\shorts\001_chatgpt_voice_input\short.json

- coverage: Shorts title/script/caption metadata
- coverage: Shorts render/ImageGen manifests and overlay files
- violations: none

## short: C:\Codex\260829_youtube-anshin\shorts\002_ai_suspicious_message\short.json

- coverage: Shorts title/script/caption metadata
- coverage: Shorts render/ImageGen manifests and overlay files
- violations: none

## short: C:\Codex\260829_youtube-anshin\shorts\003_mynumber_smartphone\short.json

- coverage: Shorts title/script/caption metadata
- coverage: Shorts render/ImageGen manifests and overlay files
- violations: none
