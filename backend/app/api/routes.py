from time import perf_counter
from fastapi import APIRouter, HTTPException, Request
from app.schemas.classification import TextRequest, ImageRequest, PageRequest, ClassificationResponse, PageResponse
from app.ml.text_classifier import TextClassifier
from app.ml.image_classifier import ImageClassifier
from app.services.safety_engine import evaluate

router = APIRouter(prefix="/api/v1")
text_model = TextClassifier()
image_model = ImageClassifier()


@router.post("/classify/text", response_model=ClassificationResponse)
def classify_text(payload: TextRequest, request: Request) -> ClassificationResponse:
    started = perf_counter()
    label, risk, confidence = text_model.predict(payload.text)
    return ClassificationResponse(classification=label, risk_score=round(risk, 4), confidence=round(confidence, 4), categories=[] if label == "SAFE" else [label.lower()], processing_time_ms=int((perf_counter()-started)*1000))


@router.post("/classify/image", response_model=ClassificationResponse)
def classify_image(payload: ImageRequest) -> ClassificationResponse:
    started = perf_counter()
    try:
        label, risk, confidence = image_model.predict(payload.image_base64)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ClassificationResponse(classification=label, risk_score=round(risk, 4), confidence=round(confidence, 4), processing_time_ms=int((perf_counter()-started)*1000))


@router.post("/classify/page", response_model=PageResponse)
def classify_page(payload: PageRequest) -> PageResponse:
    _, text_score, confidence = text_model.predict(payload.text)
    image_scores: list[float] = []
    for raw in payload.images:
        try:
            _, score, _ = image_model.predict(raw)
            image_scores.append(score)
        except ValueError:
            continue
    result = evaluate(str(payload.url), payload.text, text_score, max(image_scores, default=0.0), payload.sensitivity, payload.blocklist, payload.allowlist)
    return PageResponse(decision=result.decision, risk_score=result.score, confidence=round(confidence, 4), signals=result.signals)


@router.get("/model/info")
def model_info() -> dict[str, object]:
    return {"text_model_loaded": text_model.model is not None, "text_algorithm": "TF-IDF + Logistic Regression", "image_adapter": "in-memory lightweight signal", "fixture_data": "synthetic demo only"}
