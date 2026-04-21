# Crisis Resources

This file is a verification protocol and schema. Do not invent or rely on unverified hotline numbers.

## Rule

Before providing a specific crisis hotline, text line, or chat service, verify it from an official or highly reliable current source when possible. Crisis resources change by region and date.

If no verified region-specific resource is available, advise:

- local emergency number;
- nearest emergency department;
- urgent mental-health service if known;
- trusted person nearby;
- local search terms in the user's language.

## Resource Schema

```yaml
country_or_region:
language:
emergency_number:
crisis_hotline:
text_or_chat_option:
official_source_url:
last_verified:
notes:
```

## Verified Starter Entries

Last verified: 2026-04-21. Re-verify before use when browsing is available, especially for non-emergency hotlines.

```yaml
- country_or_region: United States and territories
  language: English; Spanish options; voice interpretation may support additional languages
  emergency_number: "911 for life-threatening emergencies"
  crisis_hotline: "988 Suicide & Crisis Lifeline"
  text_or_chat_option: "Call or text 988; chat via 988lifeline.org; Spanish text: AYUDA to 988"
  official_source_url: "https://988lifeline.org/get-help/"
  last_verified: "2026-04-21"
  notes: "Free, confidential, 24/7 support for emotional distress or suicidal crisis."

- country_or_region: United Kingdom
  language: English
  emergency_number: "999 or A&E if someone is in danger"
  crisis_hotline: "Samaritans 116 123; NHS 111 mental health option for urgent but non-emergency help"
  text_or_chat_option: "Text SHOUT to 85258 for 24/7 crisis text support"
  official_source_url: "https://www.nhs.uk/every-mind-matters/urgent-support/"
  last_verified: "2026-04-21"
  notes: "NHS states 999/A&E for danger, NHS 111 for urgent non-emergency mental health help, and lists Samaritans and Shout."

- country_or_region: China mainland
  language: Chinese
  emergency_number: "110/120 for immediate public safety or medical emergency; use local emergency services when in danger"
  crisis_hotline: "12356 national unified psychological assistance hotline"
  text_or_chat_option: ""
  official_source_url: "https://www.nhc.gov.cn/yzygj/c100068/202412/49a1a65386cd4be582d4702fd0926ee8.shtml"
  last_verified: "2026-04-21"
  notes: "NHC set 12356 as the national unified psychological assistance number; local implementation and service hours may vary, with at least 18 hours/day required by the notice."

- country_or_region: Japan
  language: Japanese; some services offer foreign-language guidance
  emergency_number: "119 for medical/fire emergency; 110 for police emergency"
  crisis_hotline: "#いのちSOS 0120-061-338; よりそいホットライン 0120-279-338; いのちの電話 0120-783-556 / 0570-783-556"
  text_or_chat_option: "MHLW lists SNS/chat相談 options on まもろうよこころ"
  official_source_url: "https://www.mhlw.go.jp/mamorouyokokoro/?s=04"
  last_verified: "2026-04-21"
  notes: "#いのちSOS and よりそいホットライン are listed as 24-hour; いのちの電話 has limited freephone hours and paid Navi Dial."

- country_or_region: South Korea
  language: Korean
  emergency_number: "119 for rescue/medical emergency; 112 for police emergency"
  crisis_hotline: "109 suicide prevention counseling hotline"
  text_or_chat_option: "MOHW announced SNS counseling provision; verify current channel before use."
  official_source_url: "https://www.mohw.go.kr/board.es?act=view&bid=0027&list_no=1479607&mid=a10503000000"
  last_verified: "2026-04-21"
  notes: "MOHW states 109 began operation on 2024-01-01 and can connect to emergency dispatch and mental health welfare centers."

- country_or_region: Singapore
  language: English; local languages may vary by service
  emergency_number: "995 or 999 for immediate danger or urgent assistance"
  crisis_hotline: "Samaritans of Singapore 1767"
  text_or_chat_option: "24-hour CareText via WhatsApp: 9151 1767"
  official_source_url: "https://www.sos.org.sg/"
  last_verified: "2026-04-21"
  notes: "SOS states hotline and CareText are 24-hour; emergency services are 995 or 999 for immediate danger."

- country_or_region: France
  language: French
  emergency_number: "112 for European emergency; 15 SAMU, 17 police, 18 fire in France"
  crisis_hotline: "3114 national suicide prevention number"
  text_or_chat_option: ""
  official_source_url: "https://3114.fr/"
  last_verified: "2026-04-21"
  notes: "3114 is free, 24/7, available across metropolitan and overseas France, and piloted by the health ministry."

- country_or_region: Germany
  language: German
  emergency_number: "112 for emergency medical/fire; 110 for police"
  crisis_hotline: "TelefonSeelsorge: 0800 1110111 / 0800 1110222 / 116 123"
  text_or_chat_option: "Mail and chat via telefonseelsorge.de / online.telefonseelsorge.de"
  official_source_url: "https://www.telefonseelsorge.de/"
  last_verified: "2026-04-21"
  notes: "TelefonSeelsorge lists phone, mail, chat, local counseling, and crisis/suicide-prevention support; calls are free."
```

## Verification Criteria

Prefer:

- Government health or emergency service websites.
- Official crisis-line websites.
- National health service websites.
- Major public health institutions.

Avoid:

- Old blog posts.
- Unsourced lists.
- Forum answers.
- Search snippets without official confirmation.

## Safe Generic Wording

If region unknown:

> I do not want to give you the wrong number. If you might hurt yourself soon, call the emergency number where you are, go to the nearest emergency department, or ask someone nearby to call emergency help. If you tell me your country or region, I can help look for the right crisis option.

## Starter Regions To Verify Later

Keep this section as a checklist, not as a hotline list:

- China mainland, Hong Kong, Taiwan, Macau.
- United States.
- Japan.
- South Korea.
- Singapore, Malaysia, Thailand, Philippines, Vietnam, Indonesia.
- United Kingdom.
- France, Germany, Netherlands, Belgium, Switzerland, Austria, Spain, Italy, Portugal, Ireland, Nordic countries.
