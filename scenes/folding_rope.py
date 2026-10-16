"""
《对折剪绳子》竖屏白底草稿本 · SOP 三段式瀑布流版

降维打击动画：将对折3次后的绳子展开，用8条红色虚线模拟"剪8刀"。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class FoldingRope(MathExplainScene):
    def construct(self):
        safe_w = AppConfig.SAFE_WIDTH
        safe_bottom = AppConfig.SAFE_Y_BOTTOM

        C_TEXT = AppConfig.COLOR_TEXT
        C_HL = AppConfig.COLOR_HIGHLIGHT
        C_BLUE = AppConfig.COLOR_LINE_1
        C_GREEN = AppConfig.COLOR_LINE_2

        # ════════════════════════════════════════
        # 1. 顶部：题目展示 (Y > 4，声画分离)
        # ════════════════════════════════════════
        title1 = Text(
            "对折3次剪一刀",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            color=C_HL,
            weight="BOLD",
        )
        title2 = Text(
            "会变成几段？",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        title_group = VGroup(title1, title2).arrange(DOWN, buff=0.35)
        title_group.scale_to_fit_width(safe_w)
        title_group.to_edge(UP, buff=1.2)

        # 声画分离：Hook 仅配音，画面直接出标题
        with self.voiceover("小时候怎么没想到，这种折绳子问题其实有一秒看破的绝招！"):
            self.play(Write(title_group), run_time=1.5)
        self.wait(0.3)

        # ════════════════════════════════════════
        # 2. 中部：核心逻辑与图形区 (0 < Y < 4)
        # ════════════════════════════════════════
        # 第一步：计算层数
        fold_text = Text(
            "对折 3 次 = ",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        fold_math = MathTex(r"2^3 = 8", font_size=AppConfig.NORMAL_FONT_SIZE, color=C_HL)
        layer_text = Text(
            " 层",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        layer_eq = VGroup(fold_text, fold_math, layer_text).arrange(RIGHT, buff=0.15)
        if layer_eq.width > safe_w:
            layer_eq.scale_to_fit_width(safe_w)
        layer_eq.next_to(title_group, DOWN, buff=0.8)

        with self.voiceover("绳子对折 1 次是 2 层，对折 3 次就是 2 的 3 次方，也就是 8 层。"):
            self.play(Write(layer_eq), run_time=1.2)
        self.wait(0.3)

        # 第二步：降维打击图形 —— 展开的绳子 + 8 刀
        rope = Line(LEFT * 3, RIGHT * 3, color=C_BLUE, stroke_width=12)
        cuts = VGroup()
        n_cuts = 8
        for i in range(1, n_cuts + 1):
            x = -3 + (6 * i / (n_cuts + 1))
            cut = DashedLine(
                UP * 0.5 + RIGHT * x,
                DOWN * 0.5 + RIGHT * x,
                color=C_HL,
                stroke_width=4,
                dash_length=0.15,
            )
            cuts.add(cut)

        graphic_group = VGroup(rope, cuts)
        graphic_group.scale_to_fit_width(safe_w * 0.9)
        graphic_group.next_to(layer_eq, DOWN, buff=0.8)

        with self.voiceover("既然有 8 层，这一剪刀下去，就相当于把展开的绳子剪了 8 刀！"):
            self.play(Create(rope), run_time=0.8)
            self.play(
                LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.12, run_time=1.6)
            )
        self.wait(0.3)

        # ════════════════════════════════════════
        # 3. 底部：结论区 (Y < 0，瀑布流)
        # ════════════════════════════════════════
        cut_text = Text(
            "剪 8 刀",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        arrow = MathTex(r"\Rightarrow", font_size=AppConfig.NORMAL_FONT_SIZE, color=C_HL)
        seg_text = Text(
            "8 + 1 = 9 段",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_BLUE,
            weight="BOLD",
        )
        conclusion = VGroup(cut_text, arrow, seg_text).arrange(RIGHT, buff=0.3)
        if conclusion.width > safe_w:
            conclusion.scale_to_fit_width(safe_w)
        conclusion.next_to(graphic_group, DOWN, buff=0.8)

        with self.voiceover("我们都知道，一根绳子剪 1 刀是 2 段，剪 8 刀，自然就是 9 段！"):
            self.play(Write(conclusion), run_time=1.2)
        self.wait(0.3)

        final_answer = Text(
            "= 9 段",
            font=AppConfig.DEFAULT_FONT,
            font_size=72,
            color=C_GREEN,
            weight="BOLD",
        )
        if final_answer.width > safe_w:
            final_answer.scale_to_fit_width(safe_w)
        final_answer.next_to(conclusion, DOWN, buff=0.6)

        # 底部安全区兜底
        if final_answer.get_bottom()[1] < safe_bottom:
            final_answer.shift(UP * (safe_bottom - final_answer.get_bottom()[1]))

        with self.voiceover("是不是一秒钟就想通了？关注我，每天学点数学思维。"):
            self.play(Write(final_answer), run_time=1.0)
            self.play(Circumscribe(final_answer, color=C_GREEN, run_time=1.0))
        self.wait(2.0)
