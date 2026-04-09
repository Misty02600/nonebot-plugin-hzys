import pytest
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebug import App
from tests.units.fake import fake_group_message_event_v11


@pytest.mark.asyncio
async def test_command_requires_backend_url(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    from nonebot_plugin_otto_hzys import command
    from nonebot_plugin_otto_hzys.config import Config

    monkeypatch.setattr(
        command,
        "get_plugin_config",
        lambda _: Config(otto_hzys_backend_url=""),
    )

    async with app.test_matcher(command.otto_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = fake_group_message_event_v11(
            message=Message("/ottohzys 大家好啊"),
            raw_message="/ottohzys 大家好啊",
        )

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "未配置 OTTO_HZYS_BACKEND_URL", bot=bot)


@pytest.mark.asyncio
async def test_command_sends_voice(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    from nonebot_plugin_alconna.uniseg.fallback import FallbackMessage

    from nonebot_plugin_otto_hzys import command
    from nonebot_plugin_otto_hzys.backend import OttoSynthesisOptions
    from nonebot_plugin_otto_hzys.config import Config

    audio_bytes = b"RIFF....WAVE"

    class FakeClient:
        async def synthesize(
            self, text: str, *, options: OttoSynthesisOptions
        ) -> bytes:
            assert text == "大家好啊"
            assert options.is_ysdd is True
            assert options.use_non_ddb_pinyin is True
            assert options.is_sliced is False
            return audio_bytes

    monkeypatch.setattr(
        command,
        "get_plugin_config",
        lambda _: Config(otto_hzys_backend_url="https://example.com"),
    )
    monkeypatch.setattr(command, "build_backend_client", lambda _: FakeClient())

    async with app.test_matcher(command.otto_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = fake_group_message_event_v11(
            message=Message("/ottohzys 大家好啊"),
            raw_message="/ottohzys 大家好啊",
        )

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            FallbackMessage("[voice]"),
            bot=bot,
        )
