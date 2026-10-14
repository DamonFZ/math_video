"""
《平方差公式巧算》竖屏白底草稿本 · SOP 三段式瀑布流验收版

严格遵循 MANIM_SOP.md：
  - 顶部灵魂拷问区 (Y > 4)
  - 中部核心推导区 (0 < Y < 4)
  - 底部丝滑解题区 (Y < 0，瀑布流)
  - 全程 SAFE_WIDTH=6.5 横向保护，SAFE_Y_BOTTOM=-5.0 底部保护
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class DifferenceOfSquares(MathExplainScene):
    def construct(self):
        safe_w = AppConfig.SAFE_WIDTH
        safe_bottom = AppConfig.SAFE_Y_BOTTOM

        C_TITLE = AppConfig.COLOR_TITLE
        C_TEXT = AppConfig.COLOR_TEXT
        C_HL = AppConfig.COLOR_HIGHLIGHT
        C_BLUE = AppConfig.COLOR_LINE_1
        C_GREEN = AppConfig.COLOR_LINE_2

        # ════════════════════════════════════════
        # 1. 顶部：核心标题区 (Y > 4)
        # ════════════════════════════════════════
        title_group = Text(
            "平方差公式巧算",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            color=C_HL,
            weight="BOLD",
        )
        if title_group.width > safe_w:
            title_group.scale_to_fit_width(safe_w)
        title_group.to_edge(UP, buff=1.2)

        # 声画分离：配音保留开场口语，画面只出现标题
        with self.voiceover("你是不是早就忘了初中学的平方差公式？"):
            self.play(Write(title_group), run_time=1.5)
        self.wait(0.3)

        # ════════════════════════════════════════
        # 2. 中部：核心推导区 (0 < Y < 4)
        # ════════════════════════════════════════
        problem = MathTex(
            r"1998^2 - 1997^2 = \ ?",
            font_size=60,
            color=C_TEXT,
        )
        if problem.width > safe_w:
            problem.scale_to_fit_width(safe_w)
        problem.next_to(title_group, DOWN, buff=0.8)

        with self.voiceover("遇到 1998 的平方减去 1997 的平方，千万不要硬算！"):
            self.play(Write(problem), run_time=1.2)
        self.wait(0.3)

        formula = MathTex(
            r"a^2 - b^2 = (a+b)(a-b)",
            font_size=60,
            color=C_HL,
        )
        if formula.width > safe_w:
            formula.scale_to_fit_width(safe_w)
        formula.next_to(problem, DOWN, buff=0.8)

        with self.voiceover("回忆一下公式：a 的平方减 b 的平方，等于 a 加 b，乘以 a 减 b。"):
            self.play(Write(formula), run_time=1.2)
            self.play(Circumscribe(formula, color=C_HL, run_time=1.0))
        self.wait(0.3)

        # ════════════════════════════════════════
        # 3. 底部：丝滑解题区 (Y < 0，瀑布流)
        # ════════════════════════════════════════
        # 代入公式后的形式（原题丝滑变形目标）
        substituted = MathTex(
            r"= (1998 + 1997) \times (1998 - 1997)",
            font_size=56,
            color=C_BLUE,
        )
        if substituted.width > safe_w:
            substituted.scale_to_fit_width(safe_w)
        substituted.next_to(formula, DOWN, buff=1.0)

        with self.voiceover("套用公式，原式就变成了 1998 加 1997，乘以 1998 减 1997。"):
            self.play(ReplacementTransform(problem, substituted), run_time=1.5)
        self.wait(0.3)

        result_step = MathTex(
            r"= 3995 \times 1",
            font_size=56,
            color=C_TEXT,
        )
        if result_step.width > safe_w:
            result_step.scale_to_fit_width(safe_w)
        result_step.next_to(substituted, DOWN, buff=0.8)

        with self.voiceover("后面的差刚好是 1！所以结果就是 3995。"):
            self.play(Write(result_step), run_time=1.0)
        self.wait(0.3)

        final_answer = MathTex(
            r"= 3995",
            font_size=72,
            color=C_GREEN,
        )
        final_answer.set(stroke_width=3)
        if final_answer.width > safe_w:
            final_answer.scale_to_fit_width(safe_w)
        final_answer.next_to(result_step, DOWN, buff=0.8)

        # 底部安全区兜底
        if final_answer.get_bottom()[1] < safe_bottom:
            final_answer.shift(UP * (safe_bottom - final_answer.get_bottom()[1]))

        with self.voiceover("是不是一秒钟就口算出来了？关注我，每天学点巧算技巧。"):
            self.play(Write(final_answer), run_time=1.0)
            self.play(Circumscribe(final_answer, color=C_GREEN, run_time=1.0))
        self.wait(2.0)
