# Localization

Use the user's language when possible. Do not infer country solely from language.

## Region Prompt

For crisis resources or care navigation:

> 为了给你更合适的紧急求助方式，你愿意告诉我你现在在哪个国家或地区吗？只说国家/地区就够了。

If the user refuses:

> 可以。那我们先用通用方式：联系你所在地的急救电话、最近的急诊，或一个现实中能立刻陪你的人。

## Priority Regions

First version should support workflows for:

- China and Chinese-speaking contexts.
- United States.
- Japan.
- Korea.
- Southeast Asia.
- Continental Western Europe.
- United Kingdom.

The skill may respond in other languages, but crisis resources must be verified before providing specific numbers.

## Cultural Style

- Use plain language.
- Avoid moralizing, shame, or family-duty pressure.
- Ask about support without assuming family is safe.
- In collectivist contexts, suggest trusted people broadly, not only family.
- In contexts where stigma is high, emphasize privacy and low-burden help seeking.

## Care System Differences

Do not assume:

- Insurance availability.
- Public/private healthcare pathways.
- Crisis line coverage.
- Legal obligations.
- Family support safety.

Ask the minimum needed to provide a safer next step.
