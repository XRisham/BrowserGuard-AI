from dataclasses import dataclass
from urllib.parse import urlparse
import fnmatch

WEIGHTS = {"text": 0.35, "image": 0.35, "keyword": 0.15, "domain": 0.15}
THRESHOLDS = {"LOW": (0.78, 0.9), "MEDIUM": (0.62, 0.82), "HIGH": (0.45, 0.7), "STRICT": (0.3, 0.55)}
# These neutral, synthetic test tokens make rule behavior testable without explicit material.
RISK_TOKENS = {"unsafe_test": 1.0, "sensitive_test": 0.55, "harmful_test": 0.85}


def matches(domain: str, entries: list[str]) -> bool:
    return any(fnmatch.fnmatch(domain, item.lstrip(".")) or domain == item.lstrip("*.") for item in entries)


@dataclass(frozen=True)
class SafetyResult:
    decision: str
    score: float
    signals: dict[str, float]


def evaluate(url: str, text: str, text_score: float, image_score: float, sensitivity: str, blocklist: list[str], allowlist: list[str]) -> SafetyResult:
    domain = urlparse(url).hostname or ""
    if matches(domain, blocklist):
        return SafetyResult("BLOCK", 1.0, {"text": text_score, "image": image_score, "keyword": 0.0, "domain": 1.0})
    if sensitivity != "STRICT" and matches(domain, allowlist):
        return SafetyResult("ALLOW", 0.0, {"text": text_score, "image": image_score, "keyword": 0.0, "domain": 0.0})
    lowered = text.lower()
    keyword = max((score for token, score in RISK_TOKENS.items() if token in lowered), default=0.0)
    domain_score = 0.0
    signals = {"text": text_score, "image": image_score, "keyword": keyword, "domain": domain_score}
    score = sum(signals[name] * WEIGHTS[name] for name in WEIGHTS)
    warn, block = THRESHOLDS[sensitivity]
    return SafetyResult("BLOCK" if score >= block else "WARN" if score >= warn else "ALLOW", round(score, 4), signals)
