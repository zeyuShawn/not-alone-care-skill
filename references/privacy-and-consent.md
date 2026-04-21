# Privacy and Consent

Mental-health records are sensitive even when saved locally.

## Default Privacy Position

- Save only minimal structured summaries.
- Do not save raw conversation text by default.
- Ask before saving each event unless the user has configured explicit ongoing consent.
- Let the user skip, inspect, summarize, or delete records.
- Warn that local files may be visible to other users of the computer.

## Consent Before Saving

Use language like:

> 我可以把这次整理成一条本地 CSV 记录，方便以后看趋势。不会保存完整聊天原文。可以保存吗？

For high-sensitivity content:

> 这部分比较敏感。我可以只保存一个很粗的标签，比如“风险信号出现”，不保存细节。你愿意这样记录吗？

## No Consent

If the user declines:

- Do not save.
- Do not argue.
- Continue support normally.

## Delete Requests

If the user asks to delete records:

- Confirm the scope: today, a date range, a file, support contacts, or all local records.
- Use `scripts/delete_log_entries.py` for supported deletions.
- Do not delete unrelated files.

## Shared Computer Warning

Use when first initializing data:

> 这些记录会保存在你的电脑本地。如果这台电脑会被别人使用，建议谨慎保存敏感内容。

## Encryption

First version does not encrypt CSV files. If the user asks for stronger privacy, suggest system-level encrypted folders, encrypted archives, password managers, or a future encrypted storage option.
