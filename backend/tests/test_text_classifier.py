from app.ml.text_classifier import TextClassifier


def test_empty_text_is_safe() -> None:
    assert TextClassifier().predict("")[0] == "SAFE"
