# Manim 数学视频自动化生产项目

基于 [Manim](https://www.manim.community/) 的数学讲解动画视频自动生成项目，配套 `manim-voiceover` 语音合成能力，已将 TTS 引擎从 edge-tts 迁移至**火山引擎（字节跳动）TTS V3 大模型接口**。

---

## 目录结构

```
math/
├── README.md            # 本文档
├── MANIM_SOP.md         # Manim 动画制作铁律（AI/人工必读）
├── base_scene.py        # 场景基类 MathExplainScene + 火山引擎 TTS 服务
├── config.py            # 全局配置：TTS 密钥、音色、动画参数、排版锚点
├── path_config.py       # 全局路径配置：项目根目录、虚拟环境、媒体输出
├── scenes/              # 各题目的场景脚本（已纳入版本控制，每道题一个文件）
│   ├── count_squares.py
│   ├── geometry_math.py
│   ├── odd_numbers.py
│   ├── perimeter_math.py
│   ├── queue_math.py
│   └── track_math.py
└── media/               # 渲染输出（视频/音频/语音缓存，已 gitignore）
```

---

## 环境要求

### 系统依赖（macOS）

```bash
brew install py3cairo ffmpeg pango pkg-config scipy
```

- **Python** ≥ 3.10（当前环境 Python 3.14.7）
- **ffmpeg** ≥ 4.x（当前 9.0.1）—— Manim 渲染视频必需
- **Pango / Cairo** —— ManimPango 渲染中文字体必需

### Python 依赖

| 包名 | 版本 | 说明 |
|------|------|------|
| `manim` | 0.21.0 | 3Blue1Brown 数学动画引擎 |
| `manim-voiceover` | 0.4.0 | 语音合成与音画对齐插件 |
| `ManimPango` | 0.6.1 | 中文/Unicode 文本渲染（Manim 依赖） |
| `numpy` | 2.5.3 | 数值计算（Manim 依赖） |
| `requests` | 2.34.2 | 调用火山引擎 TTS HTTP 接口 |
| `edge-tts` | 7.2.8 | （历史遗留，已弃用）微软 TTS，仅旧脚本保留 |
| `gTTS` | 2.5.4 | （兜底）Google TTS，edge-tts 失败时备用 |

### 一键安装

```bash
# 1. 创建并激活虚拟环境（示例路径）
python3 -m venv ~/manim_projects/manim-env
source ~/manim_projects/manim-env/bin/activate

# 2. 安装核心依赖
pip install manim==0.21.0 manim-voiceover==0.4.0 requests==2.34.2

# 3. （可选）兜底 TTS
pip install gTTS==2.5.4
```

> 建议使用独立虚拟环境 `~/manim_projects/manim-env`，与全局 Python 隔离。

---

## 配置说明

所有配置集中在 [`config.py`](./config.py)，通过 `AppConfig` 类统一管理。

### 1. 火山引擎 TTS 配置（必填）

项目已从 edge-tts 全面迁移至**火山引擎 TTS V3 `seed-tts-2.0` 大模型接口**，使用新版控制台「API Key 快速接入」机制。

```python
class AppConfig:
    # 火山引擎 API Key（语音技术控制台 → 大模型语音合成 → API Key）
    VOLC_API_KEY = "908b1d66-4f7b-4c20-a08d-92b05d8d4753"

    # TTS 应用 AppID
    VOLC_TTS_APPID = "7560255466"

    # 音色：V3 seed-tts-2.0 兼容音色
    TTS_VOICE = "zh_female_yingyujiaoxue_uranus_bigtts"  # 女声老师
    TTS_RESOURCE_ID = "seed-tts-2.0"
    TTS_SPEED = 1.15  # 1.0 = 正常语速
```

**⚠️ 关键说明**：
- 旧版 `VOLC_APPID` + `VOLC_ACCESS_TOKEN` 鉴权方式已废弃，必须使用新版 **API Key**。
- 旧版 V1 音色（如 `BV700_V2_streaming`）与 V3 接口不兼容，需替换为 `seed-tts-2.0` 兼容音色。
- 请求使用双 Header：`X-Api-Key` + `X-Api-Resource-Id`，请求体不含 `app` 节点。

### 2. 动画与画风配置

```python
    # 动画节奏（写入/绘制时长，秒）
    FAST_TEXT_RUNTIME = 0.5
    FAST_SHAPE_RUNTIME = 0.8

    # 字体与字号
    DEFAULT_FONT = "sans-serif"
    TITLE_FONT_SIZE = 36
    NORMAL_FONT_SIZE = 26

    # 配色
    COLOR_TITLE = "#333333"
    COLOR_TEXT  = "#333333"
    COLOR_LINE_1 = BLUE_D
    COLOR_LINE_2 = GREEN_D
    COLOR_HIGHLIGHT = "#E65100"
```

### 3. 三分法排版锚点

遵循 **顶部题干 / 左侧画图 / 右侧推导** 的三区布局，所有坐标锚点集中定义：

```python
    SAFE_Y_TOP = 2.0                      # 题干安全区下边界（图形不得高于此线）
    ZONE_GRAPH_CENTER = np.array([-3.5, -1.0, 0])  # 左侧画图区中心
    ZONE_MATH_START  = np.array([1.0, 1.5, 0])     # 右侧推导区起点
    MAX_GRAPH_SIZE = 5.0                   # 图形缩放极限
```

### 4. 路径配置

[`path_config.py`](./path_config.py) 集中管理共享路径逻辑，避免硬编码。

> **本机专属路径**：由于两台电脑的 manim-env 安装位置不同，`MANIM_ENV_ROOT` 不写死在 `path_config.py` 中，而是放在 **`path_config.local.py`**（已 gitignore，不同步）。`path_config.py` 会优先读取该文件，不存在则使用默认值 `~/manim_projects/manim-env`。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PROJECT_ROOT` | 本文件所在目录 | 项目根目录 |
| `SCENES_DIR` | `./scenes` | 场景脚本目录（已 gitignore） |
| `MANIM_ENV_ROOT` | `~/manim_projects/manim-env` | Manim 虚拟环境（可被 `path_config.local.py` 覆盖） |
| `MANIM_BIN` | `.../bin/manim` | Manim 可执行文件 |
| `PYTHON_BIN` | `.../bin/python` | 虚拟环境 Python |
| `MEDIA_DIR` | `./media` | 渲染输出根目录 |
| `VOICEOVER_CACHE_DIR` | `./media/voiceovers` | TTS 音频缓存 |

**在新机器上配置**：

```bash
cp path_config.local.example.py path_config.local.py
# 然后编辑 path_config.local.py，把 MANIM_ENV_ROOT 改成你本机的实际路径
```

---

## 使用方法

### 1. 编写场景

每个场景继承 `MathExplainScene`（已内置火山引擎 TTS 与作业本方格背景）：

```python
from manim import *
from base_scene import MathExplainScene
from config import AppConfig

class MyScene(MathExplainScene):
    def construct(self):
        # 题干放顶部
        title = Text("题目：...", font=AppConfig.DEFAULT_FONT)
        # 图形放左侧 ZONE_GRAPH_CENTER
        # 推导放右侧 ZONE_MATH_START
        ...
```

### 2. 渲染视频

```bash
# 使用项目配置的虚拟环境渲染（高质量预览）
~/manim_projects/manim-env/bin/manim -p -qh scenes/count_squares.py CountSquares

# 或激活环境后直接
source ~/manim_projects/manim-env/bin/activate
manim -p -qh scenes/count_squares.py CountSquares
```

常用参数：
- `-p`：渲染完成后自动预览
- `-qh`：高质量（1080p60）；`-ql` 低质量快速预览，`-qm` 中质量
- `-s`：只渲染最后一帧（快速调试布局）

### 3. 路径自检

```bash
python path_config.py
```

会打印所有路径并标注是否存在，便于跨环境迁移时排查。

---

## 核心文件说明

### `base_scene.py`

- **`VolcengineTTSService`**：继承 `manim_voiceover` 的 `SpeechService`，调用火山引擎 V3 `unidirectional` 流式接口，逐 chunk 解析 base64 音频并拼接，带 MD5 缓存。
- **`MathExplainScene`**：继承 `VoiceoverScene`，在 `setup()` 中自动绑定 TTS 服务，并绘制白色作业本方格背景 + 红色页边线。

### `config.py`

`AppConfig` 单例类，所有动画的字体、颜色、节奏、TTS 参数、排版锚点的唯一来源。**禁止在场景脚本中硬编码字体/颜色/坐标**。

### `MANIM_SOP.md`

动画制作四大铁律，违反会导致渲染失败或布局错乱：

1. **中文文本**：必须用 `Text("中文", font=AppConfig.DEFAULT_FONT)`，禁止 `MathTex`/`Tex` 渲染中文。
2. **三分法排版**：题干左上、图形左下、推导右下，最高点不得超过 `SAFE_Y_TOP`。
3. **相对坐标绑定**：高亮框、辅助线必须通过 `.get_center()`/`.get_corner()` 绑定主图，禁止硬编码绝对坐标。
4. **边界防溢出**：右侧长文本/长公式必须 `scale_to_fit_width(6.0)` 或降级字号，整体右移至少 `LEFT * 1.0` 留安全边距。

---

## 常见问题

### Q: 火山引擎 TTS 报错 `appid requested grant not found`？
A：使用了旧版 AppID + Access Token 鉴权。请改用新版控制台的 **API Key**，并在 `config.py` 中填写 `VOLC_API_KEY`。

### Q: 渲染报错 `No such file or directory: 'ffmpeg'`？
A：未安装 ffmpeg。`brew install ffmpeg`。

### Q: 中文字体显示为方块/乱码？
A：确保系统已安装对应字体（如 `PingFang SC`、`Heiti SC`），并在 `AppConfig.DEFAULT_FONT` 中指定可用字体名。ManimPango 会自动查找系统字体。

### Q: 语音不播放 / 视频无声音？
A：检查 `VOLC_API_KEY` 是否有效，火山引擎账户是否已开通 `seed-tts-2.0` 资源并绑定对应音色。可删除 `media/voiceovers/` 缓存后重试。
