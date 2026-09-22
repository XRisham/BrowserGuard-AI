"""Evaluate only after replacing the tiny fixture with a real held-out dataset."""
from ml.preprocessing.prepare import load_rows
from ml.training.train_text_model import train
import joblib
from sklearn.metrics import classification_report, confusion_matrix


def main() -> None:
    model = joblib.load(train())
    texts, labels = load_rows()
    predicted = model.predict(texts)
    print("Synthetic fixture diagnostic (not a performance claim):")
    print(classification_report(labels, predicted, zero_division=0))
    print(confusion_matrix(labels, predicted))


if __name__ == "__main__":
    main()
