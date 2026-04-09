from pydantic import BaseModel, ConfigDict, Field


class Config(BaseModel):
    model_config = ConfigDict(extra="ignore")

    otto_hzys_backend_url: str = Field(
        default="https://otto-hzys-api-backend.vercel.app",
        description="兼容 otto-hzys API 的后端地址",
    )
    otto_hzys_api_key: str | None = Field(
        default=None,
        description="兼容后端的 Bearer Token",
    )
