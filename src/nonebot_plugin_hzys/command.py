from __future__ import annotations

from arclet.alconna import Alconna, AllParam, Args
from nonebot import get_plugin_config
from nonebot_plugin_alconna import UniMessage, Voice, on_alconna

from .backend import (
    OttoBackendConfigError,
    OttoBackendError,
    build_backend_client,
    default_synthesis_options,
)
from .config import Config

otto_cmd = on_alconna(
    Alconna("ottohzys", Args["text", AllParam]),
    aliases={"活字印刷"},
    use_cmd_start=True,
    block=True,
)


@otto_cmd.handle()
async def handle_otto(text: UniMessage) -> None:
    plain_text = text.extract_plain_text().strip()
    if not plain_text:
        await otto_cmd.finish("请输入要转换的文本")

    config = get_plugin_config(Config)

    try:
        client = build_backend_client(config)
        audio = await client.synthesize(
            plain_text,
            options=default_synthesis_options(config),
        )
    except OttoBackendConfigError as exc:
        await otto_cmd.finish(str(exc))
    except OttoBackendError as exc:
        await otto_cmd.finish(f"活字印刷生成失败：{exc}")

    await otto_cmd.finish(UniMessage(Voice(raw=audio, name="otto.wav")))
