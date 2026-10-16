# Manim 数学视频自动化生产 SOP (AI 必读)

## 1. 铁律：中文文本渲染
- 绝对禁止使用 `MathTex`、`Tex` 或 `get_text()` 渲染中文字符！
- 只要包含中文，必须使用 `Text("中文", font=AppConfig.DEFAULT_FONT)`。
- 纯数学公式 (无中文) 才能使用 `MathTex`。

## 2. 铁律：竖屏 Y 轴瀑布流排版 (Vertical Waterfall Layout)
- **压低起点**：顶部标题统一定位为 `.to_edge(UP, buff=2.5)`，强制下移整个排版的起点，避免画面重心贴顶。
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
- **触发时机**：每次你修改了非 `.gitignore` 排除的文件（例如新建了业务 `.py` 文件、重构了基类、或者修复了某个排版 Bug），**并且在终端成功执行渲染、确认视频出片无误后**，必须主动进行 Git 提交。
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
