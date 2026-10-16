# Manim 数学视频自动化生产 SOP (AI 必读)

## 1. 铁律：中文文本渲染
- 绝对禁止使用 `MathTex`、`Tex` 或 `get_text()` 渲染中文字符！
- 只要包含中文，必须使用 `Text("中文", font=AppConfig.DEFAULT_FONT)`。
- 纯数学公式 (无中文) 才能使用 `MathTex`。

## 2. 铁律：竖屏 Y 轴瀑布流排版 (Vertical Waterfall Layout)
- **顶部标题区 (长题隐身、标题独大法则)**：
  - **文字应用题（题干超过 10 个字）**：**严禁在画面上渲染题干文字！** 题目条件全部交由 `voiceover` 配音读出。画面顶部**只允许保留一行核心主标题**（如 `"年龄巧算（变倍问题）"`），使用 `AppConfig.TITLE_FONT_SIZE` 加粗高亮，置于 `.to_edge(UP, buff=3.0)` 并对齐 `SAFE_CENTER_X`，直接调用 `.scale_to_fit_width(AppConfig.SAFE_WIDTH * 0.95)` 让主标题独自撑满安全区宽度！
  - **纯算式题（如 `1998² - 1997²`）**：顶部同样只放一行大主标题，原算式直接放到中部核心推导区展示。
- **压低起点**：顶部标题统一定位为 `.to_edge(UP, buff=3.0)`，强制下移整个排版的起点，避免画面重心贴顶。
- **舒展间距**：利用 `next_to(..., DOWN)` 排布中部图形和底部公式时，必须加大垂直间距（`buff=1.5` 或更大），让内容像瀑布一样舒展地流向屏幕中下部，严禁元素挤在一起。
- **相对坐标绑定**：中部图形与底部推导必须通过 `.next_to(上一区域, DOWN, buff=1.5)` 链式锚定，确保整体重心分布在屏幕中下部。

## 3. 铁律：相对坐标绑定
- 辅助线、高亮扫描框、移动动效等，坐标必须通过核心图形的 `.get_center()`、`.get_corner()` 或 `VGroup` 绑定。绝不能硬编码写死坐标，确保主图缩放移动时，附属物不发生错位。

## 4. 铁律：基于边界检测的防溢出机制 (Responsive Boundary Safety)
- **动态宽度校验**：在将任何大型 `VGroup`（如左侧的复杂几何图、右侧的长篇推导公式或总结文字）最终加入画面 (`play` 或 `add`) 之前，必须主动检查其物理宽度 `.width`。
- **右侧公式区压缩拦截**：
  ```python
  if right_math_group.width > AppConfig.MAX_RIGHT_WIDTH:
      right_math_group.scale_to_fit_width(AppConfig.MAX_RIGHT_WIDTH)
  ```
- **左侧图形区压缩拦截**：
  ```python
  if diagram_group.width > AppConfig.MAX_LEFT_WIDTH:
      diagram_group.scale_to_fit_width(AppConfig.MAX_LEFT_WIDTH)
  ```
- **相对坐标的重置要求**：请注意，如果在应用 `.scale_to_fit_width()` 之后改变了元素的尺寸，必须重新调用 `.next_to()` 或 `.move_to()` 刷新其锚点，以防缩放导致中心点偏移！

## 5. 铁律：自动化版本控制 (Git Workflow)
- **目录约定**：每一道题的场景类文件，统一存放在项目根目录下的 `scenes/` 文件夹中（如 `scenes/age_difference.py`）。`scenes/` 目录已被 `.gitignore` 忽略（多机同步时避免场景文件与视频互相干扰），**仅核心项目文件（`config.py`、`base_scene.py`、`MANIM_SOP.md`、`README.md` 等）参与版本控制**。场景文件顶部必须加入 `sys.path` 引导，以确保能从子目录正确导入根目录的 `base_scene` 与 `config`：
  ```python
  import sys
  from pathlib import Path
  sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
  from base_scene import MathExplainScene
  from config import AppConfig
  ```
- **触发时机**：每次你修改了核心项目文件（如 `config.py`、`base_scene.py`、`MANIM_SOP.md` 等，不含被 `.gitignore` 忽略的 `scenes/` 与 `media/`），**并且在终端成功执行渲染、确认视频出片无误后**，必须主动进行 Git 提交。
- **标准执行动作**：
  1. 执行 `git status` 检查变动。
  2. 执行 `git add .` 添加所有合法文件的修改。
  3. 执行 `git commit -m "<type>: <简明扼要描述本次修改或新增的题目>"` （type 请使用规范的 feat, fix, chore, docs 等）。
- **底线原则**：严禁在代码运行报错、画面崩溃时进行 commit。确保历史记录中的每一次 commit 都是一个能跑通出片的“可用版本”。

## 6. 铁律：非对称 UI 安全区 (Asymmetric Safe Zone)
- **偏左视觉中轴**：为了躲避右侧的点赞/评论按钮，**严禁将画面内容绝对居中！** 所有的头部标题、中部图形、底部公式，如果需要居中放置，必须且只能相对于 `x = AppConfig.SAFE_CENTER_X` 进行中心对齐。例如：`group.move_to(RIGHT * AppConfig.SAFE_CENTER_X)` 或者在排列后 `group.shift(LEFT * 0.5)`。
- **右侧防遮挡**：在加入画面前，必须强制调用 `.scale_to_fit_width(AppConfig.SAFE_WIDTH)`，进一步确保宽度安全。
- **底部防遮挡**：排版在最底部的总结或公式，其 `.get_bottom()[1]` 绝对不能小于 `AppConfig.SAFE_Y_BOTTOM`（即 -3.5）。确保为抖音底部文案留出巨大留白。

## 7. 铁律：专属配音 Hook (Voiceover Standard)
- **标准句式**：所有视频的 voiceover 开场第一句话，必须且只能使用以下两种句式之一：
  - `"小时候怎么没想到，[结合题目的后续文案]"`
  - `"你是不是忘记了，[结合题目的后续文案]"`
- **视觉约束**：该 Hook 仅限语音播放，**绝对不可作为 `Text` 渲染在画面上**（保持声画分离，画面直接出现标题）。

## 8. 铁律：图形视觉饱满度 (Visual Weight & Fullness)
竖屏环境下的图形必须能抗衡巨大的文字，严禁使用 Manim 默认的细线！
- **线段必须是"条"**：在绘制任何用于表示数量的独立线段（如年龄线段、绳子、路程）时，必须强制设置 `stroke_width=AppConfig.LINE_STROKE_WIDTH`（即 25）。
- **图形必须加粗/填充**：在绘制圆圈、多边形等闭合几何体时，必须设置 `stroke_width=AppConfig.SHAPE_STROKE_WIDTH`（即 10），并尽可能附带 `fill_opacity=AppConfig.SHAPE_FILL_OPACITY` 使其具有体积感。
- **双向限幅法则（极度重要）**：所有图形 `VGroup` 组装完毕后，在放大时必须根据其"宽高比"选择不同的缩放方法：
  - **横向图形（宽 > 高）**：使用 `.scale_to_fit_width(AppConfig.SAFE_WIDTH * 0.85)` 撑满宽度。
  - **纵向图形（高 >= 宽）**：**绝对禁止使用宽缩放！** 必须强制使用 `.scale_to_fit_height(AppConfig.SAFE_HEIGHT_GRAPHIC)`，确保图形高度不会捅破上方的标题或挤走下方的公式。

## 9. 铁律：动态空间管理 (阅后即焚 / FadeOut 法则)
- **严禁全屏堆砌**：当一道题目包含多个独立的几何状态（如情况A、情况B）或冗长的推导步骤时，绝对不允许把所有内容同时挤在画面上！
- **分镜展示与淡出**：必须采用"阅后即焚"逻辑。例如展示完"情况A"的图形与公式后，在进入"情况B"前，必须调用 `self.play(FadeOut(情况A所在的VGroup))` 释放中部和底部的空间，然后再在原位居中绘制"情况B"。
- **聚焦核心**：任何时刻，画面中部只允许存在**当前正在讲解**的那一个饱满的、巨大的图形。
