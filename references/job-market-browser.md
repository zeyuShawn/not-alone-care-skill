# Job Market Browser

Use this module for browser-based job-post collection under consent gates.

## Phase 1 Goal

Do not require the user to manually整理 large JD data.

Workflow:

- read user-provided links and open pages first,
- then support keyword-based browsing,
- normalize collected text into structured post JSON.

## Preferred Sources

- 智联招聘 and similar sites.
- User-provided job links.
- User-opened pages already visible in browser.

## Browser Collection Flow

1. Generate 2-4 query keywords from career profile.
2. Open site or user URL.
3. Read list/detail pages.
4. Capture title/company/city/salary/experience/education/responsibilities/skills/benefits/source URL.
5. Send raw output to `scripts/normalize_job_posts.py`.
6. Rank with `scripts/rank_job_fit.py`.
7. Return three classes: `稳妥尝试`, `值得补差`, `暂不建议`.

## Mandatory Consent Stops

Stop and confirm before:

- account login,
- captcha,
- resume upload,
- phone/contact form fill,
- saving personal resume/contact/account data,
- opening many pages likely to trigger anti-bot measures.

## Default Prohibitions

- No auto-apply.
- No auto-contact HR.
- No auto-edit resume.
- No auto-fill personal forms.
- No sending mental-health records to any external website.

## Failure Fallback Ladder

1. Extract visible text from opened page.
2. OCR from page/user screenshot.
3. Ask user for minimal copied snippets.
4. Fall back to generic role profile without company-specific claims.

Principle: ask minimal user effort; do not bounce cleanup burden back to user.
