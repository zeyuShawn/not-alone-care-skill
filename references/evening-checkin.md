# Evening Check-In

Use this for nightly check-ins. Keep it short and gentle.

## Default Prompt

```text
晚上了，我们不用完整复盘。你只要给我三个数字就好：

心情 0-10：
焦虑 0-10：
精力 0-10：

如果愿意，再说一句今天最重的事。
```

## Lower-Burden Version

If the user is exhausted:

> 如果连数字也不想填，可以只回一个词。比如：累、怕、空、烦、麻木。我会按这个帮你整理一条很短的记录。

## Optional Expansion

Only if the user has capacity:

- 今天有没有一个有帮助的小动作？
- 明天只放一个很小的锚点，是什么？
- 是否要保存到本地记录？

## Daily Summary

If user consents, use `scripts/append_daily_summary.py`.

Keep summary non-diagnostic:

```text
今天整体偏低，焦虑中等，精力不足。主要触发点是 __。有帮助的小动作是 __。明天的锚点是 __。
```

## Stop Conditions

Stop check-in and route to `crisis-protocol.md` if the user mentions:

- Not wanting to live.
- Self-harm or suicide plans.
- Harm to others.
- Overdose or dangerous medication use.
- Severe panic that feels unsafe.
- Hallucinations, delusions, or severe disorientation.
