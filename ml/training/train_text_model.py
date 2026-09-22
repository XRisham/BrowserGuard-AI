"""Train a local demo classifier; fixture data is synthetic and non-production."""
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from ml.preprocessing.prepare import load_rows


def train() -> Path:
    texts, labels = load_rows()
    pipeline = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)), ("classifier", LogisticRegression(max_iter=1_000, class_weight="balanced", random_state=42))])
    pipeline.fit(texts, labels)
    target = Path(__file__).resolve().parents[2] / "backend" / "models" / "text_classifier.joblib"
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, target)
    return target


if __name__ == "__main__":
    print(train())
