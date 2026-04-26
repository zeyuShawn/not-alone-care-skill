# Local Code Career Profile

Use this module to extract evidence-based career signals from authorized local code projects.

Goal: answer "what capability is already evidenced" without exaggeration.

## Input Boundary

- Scan only explicitly authorized directories.
- Do not read secrets/private accounts/chat history/browser cache.
- Default skip:
  - `.env`
  - secret/key files
  - `node_modules`
  - virtual environments
  - large caches
  - archives

## Extracted Evidence

- language and framework footprint,
- project types (script/web/data/automation/plugin/research tooling),
- tooling and engineering signals (tests, CI, packaging, db usage),
- code scale/activity (file count, structure, recency),
- portfolio-ready evidence (what was built, what problem solved, which tech used),
- intersection and gaps versus target roles.

## Career Profile Schema

Target file: `~/not_alone_care_data/career_profile.json`

```json
{
  "version": 1,
  "updated_at": "YYYY-MM-DDTHH:MM:SS",
  "consent": true,
  "sources": [
    {
      "type": "local_code",
      "path_alias": "project_a",
      "scanned_at": "YYYY-MM-DDTHH:MM:SS"
    }
  ],
  "current_role": "",
  "target_roles": [],
  "skills_evidenced": [],
  "skills_to_verify": [],
  "project_evidence": [],
  "constraints": {
    "location": "",
    "salary_floor": "",
    "remote_preference": "",
    "energy_load_limit": ""
  },
  "avoid": [],
  "notes_summary": ""
}
```

## Matching Output Requirement

Job-fit output must explain reasoning, not just scores:

- `稳妥尝试`: high overlap, manageable gaps.
- `值得补差`: direction fit, needs one targeted补差 action.
- `暂不建议`: mismatch with constraints/risk/workload.

Each job must include one low-burden action.
