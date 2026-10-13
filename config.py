from manim import *

class AppConfig:
    # === 火山引擎 TTS API 密钥配置 (新版 API Key 接入) ===
    # 请 PM 填入图 1 中获取到的 API Key (例如：908b1d66-...)
    VOLC_API_KEY = "908b1d66-4f7b-4c20-a08d-92b05d8d4753"
    # 语音技术控制台的 TTS 应用 AppID (v1/tts 接口必填)
    VOLC_TTS_APPID = "7560255466"

    # 音色与语速 (V3 seed-tts-2.0 大模型女声)
    TTS_VOICE = "zh_female_yingyujiaoxue_uranus_bigtts" # 火山引擎大模型女声，老师
    # TTS_VOICE = "zh_male_yuanboxiaoshu_uranus_bigtts" # 火山引擎大模型男声，学生
    TTS_RESOURCE_ID = "seed-tts-2.0"
    TTS_SPEED = 1.15  # 1.0 为正常语速，1.15 表示提速 15%

    # === 动画与画风配置 ===
    FAST_TEXT_RUNTIME = 0.5
    FAST_SHAPE_RUNTIME = 0.8
    DEFAULT_FONT = "sans-serif"
    TITLE_FONT_SIZE = 36
    NORMAL_FONT_SIZE = 26

    COLOR_TITLE = "#333333"
    COLOR_TEXT = "#333333"
    COLOR_LINE_1 = BLUE_D
    COLOR_LINE_2 = GREEN_D
    COLOR_HIGHLIGHT = "#E65100"

    # === 全局空间排版锚点 (Zoning & Layout) ===
    # 遵循三分法则：顶部题干区、左下图形区、右下推导区

    # 1. 题干安全区边界 (Y轴坐标)：所有图形和推导公式不得高于此线
    SAFE_Y_TOP = 2.0

    # 2. 核心画图区中心 (左下)：所有几何、网格演示的默认绝对中心点
    ZONE_GRAPH_CENTER = np.array([-3.5, -1.0, 0])

    # 3. 核心计算推导区起始点 (右下)：所有右侧排版等式的默认左上角起点
    ZONE_MATH_START = np.array([1.0, 1.5, 0])

    # 4. 安全边距缩放极限：如果图形长宽超过 5.0，建议默认 scale(0.75)
    MAX_GRAPH_SIZE = 5.0

    # === 响应式物理边界限制 (Bounding Box Limits) ===
    # Manim 标准横屏画布总宽度约为 14.2
    # 左侧图形区最大允许宽度 (防止挤压右侧)
    MAX_LEFT_WIDTH = 6.5

    # 右侧公式区最大允许宽度 (防止溢出屏幕右侧)
    MAX_RIGHT_WIDTH = 6.0
