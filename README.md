<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://github.com/Misty02600/nonebot-plugin-template/releases/download/assets/NoneBotPlugin.png" width="310" alt="logo"></a>

## ✨ nonebot-plugin-hzys ✨
[![LICENSE](https://img.shields.io/github/license/Misty02600/nonebot-plugin-hzys.svg)](./LICENSE)
[![python](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org)
[![Adapters](https://img.shields.io/badge/Adapters-OneBot%20v11-blue)](#supported-adapters)
<br/>

[![uv](https://img.shields.io/badge/package%20manager-uv-black?logo=uv)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?logo=ruff)](https://github.com/astral-sh/ruff)

</div>

## 📖 介绍

由于饼干的 [`nonebot-plugin-ottohzys`](https://github.com/lgc-NB2Dev/nonebot-plugin-ottohzys) 已归档，写了这个插件来跟踪最新上游数据。服务端来自 [`kaixinol/otto-hzys-api-backend`](https://github.com/kaixinol/otto-hzys-api-backend)，上游数据源来自 [`hua-zhi-wan/otto-hzys`](https://github.com/hua-zhi-wan/otto-hzys)。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-hzys --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-hzys --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-hzys --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-hzys
安装仓库 main 分支

    uv add git+https://github.com/Misty02600/nonebot-plugin-hzys@main
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-hzys
安装仓库 main 分支

    pdm add git+https://github.com/Misty02600/nonebot-plugin-hzys@main
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-hzys
安装仓库 main 分支

    poetry add git+https://github.com/Misty02600/nonebot-plugin-hzys@main
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_hzys"]

</details>

<details>
<summary>使用 nbr 安装(使用 uv 管理依赖可用)</summary>

[nbr](https://github.com/fllesser/nbr) 是一个基于 uv 的 nb-cli，可以方便地管理 nonebot2

    nbr plugin install nonebot-plugin-hzys
使用 **pypi** 源安装

    nbr plugin install nonebot-plugin-hzys -i "https://pypi.org/simple"
使用**清华源**安装

    nbr plugin install nonebot-plugin-hzys -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>


## ⚙️ 配置

在 NoneBot 项目的 `.env` 中配置：

| 配置项 | 必填 | 默认值 | 说明 |
| :-- | :--: | :--: | :-- |
| `OTTO_HZYS_BACKEND_URL` | 否 | `https://otto-hzys-api-backend.vercel.app` | 后端地址，例如 `http://127.0.0.1:3000` |
| `OTTO_HZYS_API_KEY` | 否 | 无 | 后端 Token |

示例：

```env
OTTO_HZYS_BACKEND_URL=http://127.0.0.1:3000
```

## 🎉 使用
### 指令表
| 指令 | 说明 |
| :-- | :-- |
| `ottohzys/活字印刷 <文本>` | 生成活字印刷语音 |
