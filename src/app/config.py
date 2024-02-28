from typing import Sequence
from pydantic_settings import BaseSettings


class SentrySettings(BaseSettings):
    dsn: str = "https://5943d18cd1acb97606771f4a1a9b53df@us.sentry.io/4506698870554624"
    enable_tracing: bool = True
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0
    transaction_style: str = "url"


class CORS(BaseSettings):
    allow_origins: Sequence[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: Sequence[str] = ["*"]
    allow_headers: Sequence[str] = ["*"]


class Settings(BaseSettings):
    firebase_certificate: str = "/home/dogan/parentwiser/src/key.json"
    sentry: SentrySettings = SentrySettings()
    cors: CORS = CORS()
    enable_cors: bool = True
