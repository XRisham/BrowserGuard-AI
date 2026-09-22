# API

`GET /health` returns service status. `POST /api/v1/classify/text` accepts `{text, threshold?}`. `POST /api/v1/classify/image` accepts `{image_base64}` and decodes it only in memory. `POST /api/v1/classify/page` accepts a URL, bounded text, optional image strings, sensitivity and user lists; it returns `ALLOW`, `WARN`, or `BLOCK` plus signal scores. `GET /api/v1/model/info` reports model availability. Interactive OpenAPI is at `/docs`.
