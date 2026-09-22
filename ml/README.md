# ML pipeline

`datasets/synthetic_demo.csv` is a deliberately small, non-explicit demo fixture. `python -m ml.training.train_text_model` creates a serialized TF-IDF/Logistic Regression model. `python -m ml.evaluation.evaluate` prints diagnostics only; no metrics are represented as production results. Replace the fixture with consented, licensed, balanced, reviewed data; use stratified train/validation/test splits, retain a held-out test set, and record accuracy, precision, recall, F1, confusion matrix and ROC-AUC where binary scoring applies.
