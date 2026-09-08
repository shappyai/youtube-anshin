# Viewer-facing internal brand promise QA

- rule: `viewer_facing_internal_brand_promise`
- classification: `INTERNAL_ONLY`
- viewer-facing expected count: `0`
- viewer-facing count: `0`
- status: **PASS**

Internal planning/brand documents may contain the phrase. Viewer-facing scene text, prompts/text specs, subtitles, narration, CTA, thumbnail/end-card metadata, and overlay candidates may not.

## episode: C:\Codex\260829_youtube-anshin\episodes\015_google_2fa_check\episode.json

- coverage: episode title/description metadata
- coverage: scene renderer text and ImageGen prompt/generated-text metadata
- coverage: narration and subtitle canonical text
- coverage: CTA/end-card canonical text
- coverage: subtitle and overlay files; narration is checked from episode.json
- coverage: publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests
- violations: none
