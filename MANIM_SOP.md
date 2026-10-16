# Manim 数学视频自动化生产 SOP (AI 必读)

## 1. 铁律：中文文本渲染
- 绝对禁止使用 `MathTex`、`Tex` 或 `get_text()` 渲染中文字符！
- 只要包含中文，必须使用 `Text("中文", font=AppConfig.DEFAULT_FONT)`。
- 纯数学公式 (无中文) 才能使用 `MathTex`。

## 2. 铁律：三分法防重叠排版 (Anti-Overlap Layout)
- **顶部题干 (Question)**：统一定位在左上角 `.to_corner(UL)`，使用 `VGroup(...).arrange(DOWN, aligned_edge=LEFT)`。
- **左侧画图区 (Diagram)**：图形整体的主体中心必须放置在 `AppConfig.ZONE_GRAPH_CENTER`。严禁使用纯 `ORIGIN` 或随意 `shift` 导致撞上文字。
- **右侧推导区 (Equations)**：公式和总结文字统一放在右侧，起始位置对齐 `AppConfig.ZONE_MATH_START`。后续推导公式请使用 `.next_to(prev_eq, DOWN, aligned_edge=LEFT)` 垂直向下排列。
- **高度红线**：图形和右侧公式的最高点，绝对不能超过 Y 坐标 `AppConfig.SAFE_Y_TOP`。

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
