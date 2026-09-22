from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
app = FastAPI(title="BrowserGuard AI API", version="0.1.0", docs_url="/docs")
app.state.limiter = limiter
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    if request.method == "POST" and int(request.headers.get("content-length", "0")) > settings.max_image_size_mb * 1024 * 1024 * 2:
        return JSONResponse(status_code=413, content={"detail": "Request too large"})
    response = await call_next(request)
    response.headers.update({"X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer", "Cache-Control": "no-store"})
    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limited(_: Request, __: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "browserguard-api"}


app.include_router(router)
