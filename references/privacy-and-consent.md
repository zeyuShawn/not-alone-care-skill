# Privacy and Consent

Mental-health records are sensitive even in local storage.

## Default Privacy Position

- Save minimal structured summaries.
- Do not save raw conversation text by default.
- Ask before saving each entry unless ongoing consent is configured.
- Allow inspect/update/validate/dry-run delete/delete at user request.
- Validate score ranges, date formats, known fields, and JSON structure before relying on local records.
- Warn about shared-device visibility risk.

## Storage Isolation Rule

Mental-health CSV and ver2.1.0 non-clinical JSON must stay separated.

Mental-health CSV:

- `event_log.csv`
- `daily_summary.csv`
- `support_contacts.csv`

ver2.1.0 JSON:

- `outing_preferences.json`
- `career_profile.json`
- `job_posts_cache.json`
- `exports/roundtrip/*`

Do not write outing/career/job payloads into mental-health CSV.

## Consent Before Saving

Example:

> 我可以把这次整理成一条本地记录，只保存必要摘要，不存完整聊天原文。可以保存吗？

For high sensitivity:

> 这部分比较敏感。我可以只保存一个粗粒度标签，不保存细节。你愿意吗？

If user declines, do not save and continue support.

## External Sharing Prohibition

Without explicit consent, do not send local mental-health records to:

- job platforms,
- browser forms,
- third-party apps,
- public links.

## Deletion Requests

- Confirm scope (single date/range/file/contact/all).
- Use `scripts/delete_log_entries.py --dry-run` before destructive CSV deletions when practical.
- Use `--confirm YES` for destructive CSV deletions.
- For JSON data, delete only requested keys/files.
- Never delete unrelated files.

## Encryption Note

Current version does not add built-in file encryption.
If user needs stronger privacy, recommend encrypted folders/system-level encryption.

## Career and Job Data

- Browser-collected job posts and normalized job caches require explicit local-save consent.
- Local code analysis stores project aliases by default; absolute paths should be saved only when the user explicitly opts in.
- Treat career constraints, salary floors, locations, and job-search queries as sensitive even though they are separated from mental-health CSV logs.
