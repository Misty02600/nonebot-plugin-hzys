from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_alconna")

from .command import otto_cmd
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="otto 活字印刷",
    description="调用兼容后端生成 otto 活字印刷语音",
    usage="/ottohzys 大家好啊",
    type="application",
    homepage="https://github.com/Misty02600/nonebot-plugin-hzys",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={"author": "Misty02600 <Misty02600@gmail.com>"},
)

__all__ = ("__plugin_meta__", "otto_cmd")
