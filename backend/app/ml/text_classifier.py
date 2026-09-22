"""Model loader with deterministic safe fallback when no trained artifact exists."""
from pathlib import Path
import re
import joblib
import numpy as np
from app.core.config import get_settings


class TextClassifier:
    def __init__(self) -> None:
        self.model = None
        path = Path(get_settings().model_path)
        if path.exists():
            self.model = joblib.load(path)

    @staticmethod
    def clean(text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"https?://\S+", " URL ", text.lower())).strip()

    def predict(self, text: str) -> tuple[str, float, float]:
        if not text.strip():
            return "SAFE", 0.0, 1.0
        if self.model is None:
            # Fail open so a missing model cannot silently overblock. Health/model-info expose this state.
            return "SAFE", 0.0, 0.0
        probs = self.model.predict_proba([self.clean(text)])[0]
        labels = list(self.model.classes_)
        index = int(np.argmax(probs))
        label = str(labels[index])
        risk = float(probs[labels.index("UNSAFE")] + probs[labels.index("SENSITIVE")] * 0.55)
        return label, risk, float(probs[index])
