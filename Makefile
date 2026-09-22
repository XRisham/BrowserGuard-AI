.PHONY: train test backend extension
train:
	python -m ml.training.train_text_model
test:
	cd backend && pytest
backend:
	cd backend && uvicorn app.main:app --reload
extension:
	cd extension && npm run dev
