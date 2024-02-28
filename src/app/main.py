from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.api.v1.posts.routes import router as posts_routes

from app.config import Settings

settings = Settings()

sentry_sdk.init(
    dsn=settings.sentry.dsn,
    enable_tracing=settings.sentry.enable_tracing,
    traces_sample_rate=settings.sentry.traces_sample_rate,
    profiles_sample_rate=settings.sentry.profiles_sample_rate,
    integrations=[
        FastApiIntegration(transaction_style=settings.sentry.transaction_style),
        StarletteIntegration(transaction_style=settings.sentry.transaction_style),
    ],
)

app = FastAPI()
app.include_router(posts_routes, prefix="/posts", tags=["posts"])

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    errs = []
    for i in errors:
        errs.append({"field": i["loc"][-1], "msg": i["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=errs,
    )
