"""In-memory, non-persistent lightweight image risk signal.

This is intentionally conservative: it measures image decode validity and visual
complexity, not human attributes. Replace with a consented, evaluated model for
production deployment.
"""
import base64
from io import BytesIO
import numpy as np
from PIL import Image


class ImageClassifier:
    def predict(self, encoded: str) -> tuple[str, float, float]:
        try:
            raw = base64.b64decode(encoded.split(",")[-1], validate=True)
            image = Image.open(BytesIO(raw)).convert("RGB")
            image.thumbnail((224, 224))
            pixels = np.asarray(image, dtype=np.float32)
            # A calibrated model may replace this adapter. Never infer explicit content from pixels here.
            variance = float(np.var(pixels) / (255**2))
            return "SAFE", min(0.2, variance), 0.25
        except Exception as exc:
            raise ValueError("Image must be valid base64-encoded image data") from exc
