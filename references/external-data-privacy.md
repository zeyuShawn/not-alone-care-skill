# External Data Privacy

Use this file whenever working with external websites, browser automation, OCR from web pages, or job-platform data.

## Core Firewall

- Mental-health records and labels must stay isolated from job/outing exports unless user explicitly authorizes sharing.
- Never transmit mental-health CSV content to third-party sites by default.
- Keep data minimization as default.

## Separate Storage Domains

Mental-health CSV:

- `event_log.csv`
- `daily_summary.csv`
- `support_contacts.csv`

ver2.1.0 non-clinical JSON:

- `outing_preferences.json`
- `career_profile.json`
- `job_posts_cache.json`
- `exports/roundtrip/*`

## Mandatory Consent Checkpoints

Require explicit confirmation before:

- login/account operations,
- captcha solving steps,
- personal info submission,
- resume upload/edit,
- revealing contact details,
- saving sensitive page snapshots,
- any operation that may trigger anti-crawl boundaries.

## Data Retention Policy

- Keep job cache deletable by default.
- Store only structured summary fields necessary for matching.
- Avoid raw full-page dumps when concise structured extraction is enough.
- If user revokes consent, support view/update/delete for new JSON stores.

## Red Lines

- No silent scraping that exceeds user intent.
- No auto posting/submitting.
- No hidden sharing of local private data.
- No reusing mental-health risk labels as hiring labels.
