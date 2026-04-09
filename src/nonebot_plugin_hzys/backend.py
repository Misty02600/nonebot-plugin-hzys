from __future__ import annotations

from dataclasses import dataclass

import httpx

from .config import Config


class OttoBackendError(Exception):
    """Base exception for remote otto backend failures."""


class OttoBackendConfigError(OttoBackendError):
    """Raised when the plugin is missing required backend configuration."""


class OttoBackendRequestError(OttoBackendError):
    """Raised when the backend request fails or returns an invalid response."""


@dataclass(slots=True, frozen=True)
class OttoSynthesisOptions:
    is_ysdd: bool = True
    use_non_ddb_pinyin: bool = True
    is_sliced: bool = False


class OttoBackendClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        timeout: float = 20.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.transport = transport

    async def synthesize(self, text: str, *, options: OttoSynthesisOptions) -> bytes:
        payload = {
            "text": text,
            "isYsdd": options.is_ysdd,
            "useNonDdbPinyin": options.use_non_ddb_pinyin,
            "isSliced": options.is_sliced,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                transport=self.transport,
            ) as client:
                response = await client.post(
                    "/api/text-to-wav", json=payload, headers=headers
                )
        except httpx.HTTPError as exc:
            raise OttoBackendRequestError(f"请求后端失败：{exc}") from exc

        if response.status_code >= 400:
            detail = _extract_error_detail(response)
            raise OttoBackendRequestError(
                f"后端返回错误 {response.status_code}：{detail}"
            )
        if not response.content:
            raise OttoBackendRequestError("后端没有返回音频数据")

        return response.content

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                transport=self.transport,
            ) as client:
                response = await client.get("/health")
        except httpx.HTTPError:
            return False
        return response.status_code < 400


def build_backend_client(config: Config) -> OttoBackendClient:
    if not config.otto_hzys_backend_url.strip():
        raise OttoBackendConfigError("未配置 OTTO_HZYS_BACKEND_URL")

    return OttoBackendClient(
        base_url=config.otto_hzys_backend_url,
        api_key=config.otto_hzys_api_key,
    )


def default_synthesis_options(config: Config) -> OttoSynthesisOptions:
    return OttoSynthesisOptions()


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return response.text.strip() or "未知错误"

    if isinstance(data, dict):
        for key in ("error", "message", "detail"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return response.text.strip() or "未知错误"
