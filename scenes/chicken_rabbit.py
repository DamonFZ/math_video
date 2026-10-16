"""
《鸡兔同笼：假设法》竖屏白底草稿本 · 大字报瀑布流版

视觉目标：白底浅灰网格，内容撑满 UI 安全框，自上而下大间距分布。
  - SAFE_WIDTH = 6.5   (红色安全框，左右各留 0.75)
  - SAFE_Y_BOTTOM = -5.0
  - frame = 8.0 x 14.22，Y 范围 [-7.11, 7.11]
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class ChickenRabbit(MathExplainScene):
    def construct(self):
        safe_w = AppConfig.SAFE_WIDTH
        safe_bottom = AppConfig.SAFE_Y_BOTTOM

        C_HL = AppConfig.COLOR_HIGHLIGHT
        C_TEXT = AppConfig.COLOR_TEXT
        C_BLUE = AppConfig.COLOR_LINE_1
        C_GREEN = AppConfig.COLOR_LINE_2

        # ════════════════════════════════════════
        # 1. 顶部题目区（to_edge 置顶，横向顶满红框）
        # ════════════════════════════════════════
        title_main = Text(
            "鸡兔同笼 (假设法)",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            weight="BOLD",
            color=C_HL,
        )
        title_sub = Text(
            "共 20 个头，56 只脚，鸡兔各几只？",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        title_group = VGroup(title_main, title_sub).arrange(DOWN, buff=0.35)
        title_group.scale_to_fit_width(safe_w)
        title_group.to_edge(UP, buff=1.0)

        with self.voiceover("同学们，今天我们学习经典的鸡兔同笼问题。"):
            self.play(Write(title_group), run_time=1.5)
        self.wait(0.3)

        # ════════════════════════════════════════
        # 2. 中部画图区（加大间距，撑满红框 85%）
        # ════════════════════════════════════════
        def make_chicken():
            body = Circle(radius=0.4, color=C_BLUE, stroke_width=6)
            l1 = Line(
                body.get_bottom() + DOWN * 0.05,
                body.get_bottom() + DOWN * 0.15,
                color=C_BLUE, stroke_width=6,
            ).shift(LEFT * 0.15)
            l2 = Line(
                body.get_bottom() + DOWN * 0.05,
                body.get_bottom() + DOWN * 0.15,
                color=C_BLUE, stroke_width=6,
            ).shift(RIGHT * 0.15)
            return VGroup(body, l1, l2)

        def make_rabbit():
            body = Circle(radius=0.4, color=C_GREEN, stroke_width=6)
            xs = [-0.25, -0.1, 0.1, 0.25]
            legs = VGroup(*[
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * 0.15,
                    color=C_GREEN, stroke_width=6,
                ).shift(RIGHT * x)
                for x in xs
            ])
            return VGroup(body, legs)

        animals = VGroup(*[make_chicken() for _ in range(20)])
        animals.arrange_in_grid(rows=4, cols=5, buff=0.5)
        # 撑满安全框的 85%
        animals.scale_to_fit_width(safe_w * 0.85)
        animals.next_to(title_group, DOWN, buff=1.2)

        with self.voiceover("我们先假设笼子里全是鸡，每只鸡有 2 只脚。"):
            self.play(
                LaggedStart(
                    *[FadeIn(a, shift=DOWN * 0.3) for a in animals],
                    lag_ratio=0.05,
                    run_time=1.8,
                )
            )
        self.wait(0.3)

        # ════════════════════════════════════════
        # 3. 底部公式区（大字号瀑布流，严格不低于 SAFE_Y_BOTTOM）
        # ════════════════════════════════════════
        def make_line(math_tex, desc, color):
            eq = MathTex(math_tex, color=color, font_size=56)
            d = Text(desc, font=AppConfig.DEFAULT_FONT, font_size=40, color=color)
            return VGroup(eq, d).arrange(RIGHT, buff=0.2)

        line1 = make_line(r"20 \times 2 = 40", "（只脚）", C_TEXT)
        line2 = make_line(r"56 - 40 = 16", "（只脚）", C_TEXT)
        line3 = make_line(r"4 - 2 = 2", "（只脚）", C_TEXT)
        line4 = make_line(r"16 \div 2 = 8", "（只兔）", C_HL)

        ans_rabbit = Text(
            "兔 = 8 只",
            font=AppConfig.DEFAULT_FONT, font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_GREEN, weight="BOLD",
        )
        ans_chicken = Text(
            "鸡 = 20 - 8 = 12 只",
            font=AppConfig.DEFAULT_FONT, font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_BLUE, weight="BOLD",
        )
        final_group = VGroup(ans_rabbit, ans_chicken).arrange(DOWN, buff=0.3)

        formulas = VGroup(line1, line2, line3, line4, final_group).arrange(
            DOWN, buff=0.8, aligned_edge=LEFT
        )

        # 横向安全
        if formulas.width > safe_w:
            formulas.scale_to_fit_width(safe_w)

        # 纵向安全：撑满网格底部 → 安全底线之间的空间
        grid_bottom = animals.get_bottom()[1]
        avail_h = grid_bottom - safe_bottom - 0.5
        if formulas.height > avail_h:
            formulas.scale_to_fit_height(avail_h)

        formulas.next_to(animals, DOWN, buff=0.6)
        # 最终兜底：若底部仍低于安全线，整体上移
        if formulas.get_bottom()[1] < safe_bottom:
            formulas.shift(UP * (safe_bottom - formulas.get_bottom()[1]))

        # ════════════════════════════════════════
        # 4. 动画演绎（鸡→兔变色 + 添脚）
        # ════════════════════════════════════════
        with self.voiceover("全是鸡的话，20 只鸡一共 40 只脚。"):
            self.play(Write(line1), run_time=1.0)
        self.wait(0.2)

        with self.voiceover("但实际有 56 只脚，少了 16 只脚。"):
            self.play(Write(line2), run_time=1.0)
        self.wait(0.2)

        with self.voiceover("每只兔比鸡多 2 只脚。"):
            self.play(Write(line3), run_time=1.0)
        self.wait(0.2)

        with self.voiceover("所以少的 16 只脚，就是 8 只兔子。"):
            transforms = []
            for i in range(8):
                old = animals[i]
                new_rabbit = make_rabbit()
                new_rabbit.move_to(old.get_center())
                new_rabbit.set(width=old.width)
                transforms.append(ReplacementTransform(old, new_rabbit))
                animals[i] = new_rabbit
            self.play(*transforms, Write(line4), run_time=2.0)
        self.wait(0.3)

        with self.voiceover("答案是兔子 8 只，鸡 12 只。"):
            self.play(Write(final_group), run_time=1.2)
        self.wait(2.0)
