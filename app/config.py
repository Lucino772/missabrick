import secrets

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CeleryConfig(BaseModel):
    broker_url: str
    result_backend: str


class ProxyConfig(BaseModel):
    x_for: int = Field(default=1)
    x_proto: int = Field(default=1)
    x_host: int = Field(default=0)
    x_port: int = Field(default=0)
    x_prefix: int = Field(default=0)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="missabrick_", env_nested_delimiter="__", case_sensitive=False
    )

    # Flask
    SECRET_KEY: str = Field(init=False, default_factory=secrets.token_hex)
    SECURITY_PASSWORD_SALT: str = Field(init=False, default_factory=secrets.token_hex)
    SERVER_NAME: str | None = Field(init=False, default=None)
    APPLICATION_ROOT: str = Field(init=False, default="/")

    # Database
    SQLALCHEMY_DATABASE_URI: str = Field(init=False)

    # Demo Account
    ENABLE_DEMO_ACCOUNT: bool = Field(init=False, default=False)
    DEMO_ACCOUNT_NAME: str | None = Field(init=False)
    DEMO_ACCOUNT_EMAIL: str | None = Field(init=False)
    DEMO_ACCOUNT_PASSWORD: str | None = Field(init=False)

    # SendGrid
    SENDGRID_API_KEY: str = Field(init=False)

    # Celery
    CELERY: CeleryConfig = Field(init=False)

    # Proxy
    PROXY: ProxyConfig | None = Field(init=False, default=None)
