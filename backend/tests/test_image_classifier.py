import base64
from io import BytesIO
from PIL import Image
from app.ml.image_classifier import ImageClassifier


def test_image_inference() -> None:
    raw = BytesIO()
    Image.new("RGB", (2, 2), "white").save(raw, "PNG")
    assert ImageClassifier().predict(base64.b64encode(raw.getvalue()).decode())[0] == "SAFE"
