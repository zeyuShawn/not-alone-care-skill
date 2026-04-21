# Support Network

Use this file for trusted contacts and help-message drafting.

## File

Use `support_contacts.csv` for contacts the user explicitly allows storing.

Fields:

```csv
name_or_alias,relationship,contact_method,available_time,preferred_for,notes,consent_to_use
```

## Boundaries

- Do not automatically contact anyone.
- Do not show full contact details unless needed and user agrees.
- Do not frame one person as the user's only support.
- Do not use a contact marked `consent_to_use=false`.
- In immediate danger, emergency services may be more appropriate than a contact.

## Add Contact Prompt

> 你可以存一个现实中能联系的人，只写称呼也可以。这个记录会保存在本地，不会自动发送任何消息。

## Crisis Message Draft

```text
我现在状态很危险，不太适合一个人待着。你能不能现在联系我，或者过来陪我一会儿？如果你联系不上我，请帮我联系紧急帮助。
```

## Lower-Risk Message Draft

```text
我今天状态不太好，不一定需要你解决什么。你有空的话，可以陪我聊几句吗？
```

## Care Appointment Support

```text
我最近情绪/焦虑已经影响睡眠和日常功能。我想预约一次专业评估，但现在有点难组织。你能不能帮我一起预约或陪我去？
```

## Choosing a Contact

Prefer contacts who are:

- Available now.
- Calm and nonjudgmental.
- Geographically near if immediate safety is involved.
- Appropriate for the current issue.

If no contact is available, use local emergency services, crisis lines, urgent clinic, emergency department, or a public safe place.

## Contact Retrieval

Use `scripts/manage_support_contacts.py list` to show available contacts without exposing `contact_method`.

Use `scripts/manage_support_contacts.py show --name <alias>` for contact details without `contact_method`.

Use `scripts/manage_support_contacts.py show --name <alias> --include-contact-method` only after the user explicitly agrees to reveal the contact method for the current task.
