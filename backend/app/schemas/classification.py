from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator

Label = Literal["SAFE", "SENSITIVE", "UNSAFE"]
Decision = Literal["ALLOW", "WARN", "BLOCK"]


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)
    threshold: float = Field(default=0.65, ge=0, le=1)

    @field_validator("text")
    @classmethod
    def normalize(cls, value: str) -> str:
        return " ".join(value.split())


class ImageRequest(BaseModel):
    image_base64: str = Field(min_length=8, max_length=7_000_000)


class PageRequest(BaseModel):
    url: HttpUrl
    title: str = Field(default="", max_length=300)
    text: str = Field(default="", max_length=10_000)
    images: list[str] = Field(default_factory=list, max_length=8)
    sensitivity: Literal["LOW", "MEDIUM", "HIGH", "STRICT"] = "HIGH"
    blocklist: list[str] = Field(default_factory=list, max_length=250)
    allowlist: list[str] = Field(default_factory=list, max_length=250)


class ClassificationResponse(BaseModel):
    classification: Label
    risk_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    categories: list[str] = Field(default_factory=list)
    processing_time_ms: int


class PageResponse(BaseModel):
    decision: Decision
    risk_score: float
    confidence: float
    signals: dict[str, float]
