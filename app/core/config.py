import secrets
import warnings
from typing import List, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator, model_validator, EmailStr
from pydantic_settings import BaseSettings

# Development-only fallbacks. Refused when ENVIRONMENT=production.
DEV_SUPERUSER_PASSWORD = "admin123"
DEV_POSTGRES_PASSWORD = "password"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise AI Assistant"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # "development" or "production"
    
    # JWT Auth
    # Must be set via env/.env. In development a random key is generated per
    # process (tokens stop working after a restart); production refuses to start.
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = DEV_POSTGRES_PASSWORD
    POSTGRES_DB: str = "enterprise_ai"
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] = ""

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, any]) -> any:
        if isinstance(v, str) and v:
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Superuser (Seeding)
    FIRST_SUPERUSER: EmailStr = "admin@enterprise.com"
    FIRST_SUPERUSER_PASSWORD: str = DEV_SUPERUSER_PASSWORD

    # Uploads
    MAX_UPLOAD_SIZE_MB: int = 20

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    # LLM (LM Studio / OpenAI)
    LLM_BASE_URL: str = "http://localhost:1234/v1"
    LLM_API_KEY: str = "lm-studio"

    @model_validator(mode="after")
    def check_secrets(self) -> "Settings":
        problems = []
        if not self.SECRET_KEY:
            problems.append("SECRET_KEY is not set")
        elif len(self.SECRET_KEY) < 32:
            problems.append("SECRET_KEY must be at least 32 characters")
        if self.FIRST_SUPERUSER_PASSWORD == DEV_SUPERUSER_PASSWORD:
            problems.append("FIRST_SUPERUSER_PASSWORD is the default development password")
        if self.POSTGRES_PASSWORD == DEV_POSTGRES_PASSWORD and "postgresql" in str(self.SQLALCHEMY_DATABASE_URI):
            problems.append("POSTGRES_PASSWORD is the default development password")

        if self.ENVIRONMENT == "production":
            if problems:
                raise ValueError("Insecure production settings: " + "; ".join(problems))
            return self

        if not self.SECRET_KEY:
            self.SECRET_KEY = secrets.token_urlsafe(48)
        for problem in problems:
            warnings.warn(f"[config] {problem} (allowed in development only)", stacklevel=2)
        return self

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
