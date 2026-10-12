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

## 4. 铁律：边界防溢出机制 (Boundary Safety)
- **动态宽容度检查**：Manim 画布的默认宽度大约为 14.2 个单位。任何排列在右侧（Right Zone）的文本组或长公式，必须进行右侧边界保护。
- **强制缩放策略**：对于单行超过 10 个中文字符，或包含极长等式（如连加、长多项式）的元素，必须主动采取以下两种措施之一：
  1. **大幅降级字号**：将其 `font_size` 设置为常规字号的 70% 甚至更小。
  2. **宽度强制拦截**：在加入画面前，检查其宽度，或强制使用 `.scale_to_fit_width()`，限制其最大宽度不超过画布宽度的一半（约 6.0）。
- **留白原则**：整个右侧的 VGroup 打包后，最后必须验证能否安全放置在画面内，必要时可整体向左平移 `shift(LEFT * 1.0)` 留出安全右边距。
