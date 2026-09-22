from backend.app.ml.text_classifier import TextClassifier


def predict(text: str) -> tuple[str, float, float]:
    return TextClassifier().predict(text)
