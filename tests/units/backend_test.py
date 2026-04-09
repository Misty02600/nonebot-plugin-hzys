import httpx
import pytest


def _options():
    from nonebot_plugin_otto_hzys.backend import OttoSynthesisOptions

    return OttoSynthesisOptions(
        is_ysdd=True,
        use_non_ddb_pinyin=True,
        is_sliced=False,
    )


@pytest.mark.asyncio
async def test_backend_client_synthesize_success() -> None:
    from nonebot_plugin_otto_hzys.backend import OttoBackendClient

    audio_bytes = b"RIFF....WAVE"

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/text-to-wav"
        assert request.headers["Authorization"] == "Bearer secret"
        assert request.headers["Content-Type"] == "application/json"
        assert request.read() == (
            b'{"text":"\xe5\xa4\xa7\xe5\xae\xb6\xe5\xa5\xbd\xe5\x95\x8a",'
            b'"isYsdd":true,"useNonDdbPinyin":true,"isSliced":false}'
        )
        return httpx.Response(
            200, content=audio_bytes, headers={"Content-Type": "audio/wav"}
        )

    transport = httpx.MockTransport(handler)
    client = OttoBackendClient(
        base_url="https://example.com",
        api_key="secret",
        transport=transport,
    )

    result = await client.synthesize("大家好啊", options=_options())

    assert result == audio_bytes


@pytest.mark.asyncio
async def test_backend_client_synthesize_http_error() -> None:
    from nonebot_plugin_otto_hzys.backend import (
        OttoBackendClient,
        OttoBackendRequestError,
    )

    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "static resources unavailable"})

    transport = httpx.MockTransport(handler)
    client = OttoBackendClient(base_url="https://example.com", transport=transport)

    with pytest.raises(OttoBackendRequestError, match="503"):
        await client.synthesize("测试", options=_options())
