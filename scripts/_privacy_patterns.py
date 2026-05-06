from __future__ import annotations

import re
from typing import List

SENSITIVE_TERMS = [
    "自伤",
    "自杀",
    "轻生",
    "suicide",
    "self-harm",
    "overdose",
    "抑郁",
    "焦虑",
    "panic",
    "危机",
]

ADDRESS_PATTERNS = [
    r"\b\d{11}\b",
    r"\b\d{2,3}-\d{7,8}\b",
    r"\d+\.\d{5,}\s*,\s*\d+\.\d{5,}",
    r"(?:路|街|道|号)\s*\d+",
]


def scrub_sensitive_text(value: object) -> str:
    text = str(value or "")
    for term in SENSITIVE_TERMS:
        text = re.sub(term, "[敏感信息已移除]", text, flags=re.IGNORECASE)
    for pattern in ADDRESS_PATTERNS:
        text = re.sub(pattern, "[敏感定位已移除]", text)
    return text.strip()


def find_sensitive_text(text: str) -> List[str]:
    lower = text.lower()
    found = [term for term in SENSITIVE_TERMS if term.lower() in lower]
    return sorted(set(found))


def find_precise_patterns(text: str) -> List[str]:
    hits: List[str] = []
    for pattern in ADDRESS_PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    return hits
