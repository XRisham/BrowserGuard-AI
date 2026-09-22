from app.services.safety_engine import evaluate


def test_allowlist_precedence_except_strict() -> None:
    assert evaluate("https://good.example", "unsafe_test", 1, 0, "HIGH", [], ["good.example"]).decision == "ALLOW"
    assert evaluate("https://good.example", "unsafe_test", 1, 0, "STRICT", [], ["good.example"]).decision != "ALLOW"
