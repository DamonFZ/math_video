"""
《鸡兔同笼：假设法》竖屏白底草稿本 · 抖音安全区版

视觉目标：白底浅灰网格草稿本风格，所有元素收缩在抖音 UI 安全区内。
  - SAFE_WIDTH = 5.8  (防右侧点赞栏遮挡)
  - SAFE_Y_BOTTOM = -5.0  (防底部文案栏遮挡)
  - frame = 8.0 x 14.22，Y 范围 [-7.11, 7.11]
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class ChickenRabbit(MathExplainScene):
    def construct(self):
        # ── 运行时帧高（由基类 setup 强制为 14.22）──
        frame_h = self.camera.frame_height
        half_h = frame_h / 2.0
        safe_w = AppConfig.SAFE_WIDTH
        safe_bottom = AppConfig.SAFE_Y_BOTTOM

        C_TITLE = AppConfig.COLOR_TITLE
        C_TEXT = AppConfig.COLOR_TEXT
        C_HL = AppConfig.COLOR_HIGHLIGHT
        C_BLUE = AppConfig.COLOR_LINE_1
        C_GREEN = AppConfig.COLOR_LINE_2

        # ════════════════════════════════════════
        # 1. 标题区（顶部）
        # ════════════════════════════════════════
        title_main = Text(
            "鸡兔同笼 (假设法)",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            weight="BOLD",
            color=C_HL,
        )
        title_sub = Text(
            "有若干只鸡兔同在一个笼子里，共 20 个头，56 只脚。问鸡和兔各有几只？",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        title_group = VGroup(title_main, title_sub).arrange(DOWN, buff=0.3)
        if title_group.width > safe_w:
            title_group.scale_to_fit_width(safe_w)
        title_top_y = half_h - 0.5
        title_group.shift(UP * (title_top_y - title_group.get_top()[1]))

        with self.voiceover("同学们，今天我们学习经典的鸡兔同笼问题。"):
            self.play(Write(title_group), run_time=1.5)
        self.wait(0.3)

        # ════════════════════════════════════════
        # 2. 图形区（中部，撑满安全宽度）
        # ════════════════════════════════════════
        def make_chicken(scale=1.0):
            body = Circle(radius=0.4 * scale, color=C_BLUE, stroke_width=6)
            legs = VGroup(
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_BLUE,
                    stroke_width=6,
                ),
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_BLUE,
                    stroke_width=6,
                ),
            )
            legs[0].shift(LEFT * 0.15 * scale)
            legs[1].shift(RIGHT * 0.15 * scale)
            return VGroup(body, legs)

        def make_rabbit(scale=1.0):
            body = Circle(radius=0.4 * scale, color=C_GREEN, stroke_width=6)
            legs = VGroup(
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_GREEN,
                    stroke_width=6,
                ),
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_GREEN,
                    stroke_width=6,
                ),
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_GREEN,
                    stroke_width=6,
                ),
                Line(
                    body.get_bottom() + DOWN * 0.05,
                    body.get_bottom() + DOWN * (0.15 * scale),
                    color=C_GREEN,
                    stroke_width=6,
                ),
            )
            x_positions = [-0.25, -0.1, 0.1, 0.25]
            for i, leg in enumerate(legs):
                leg.shift(RIGHT * x_positions[i] * scale)
            return VGroup(body, legs)

        animals = VGroup()
        for i in range(20):
            animals.add(make_chicken())
        animals.arrange_in_grid(rows=4, cols=5, buff=0.3)

        # 标题底部 → 网格顶部
        title_bottom = title_group.get_bottom()[1]
        grid_top_y = title_bottom - 0.8

        # 网格撑满安全宽度
        if animals.width > safe_w:
            animals.scale_to_fit_width(safe_w)

        animals.move_to(
            np.array([0, grid_top_y - animals.height / 2, 0])
        )

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
        # 3. 公式推导区（底部，严格不低于 SAFE_Y_BOTTOM）
        # ════════════════════════════════════════
        grid_bottom = animals.get_bottom()[1]

        eq1 = MathTex(r"20 \times 2 = 40", color=C_TEXT)
        eq1_desc = Text(
            "（只脚）", font=AppConfig.DEFAULT_FONT, font_size=36, color=C_TEXT
        )
        line1 = VGroup(eq1, eq1_desc).arrange(RIGHT, buff=0.15)

        eq2 = MathTex(r"56 - 40 = 16", color=C_TEXT)
        eq2_desc = Text(
            "（只脚）", font=AppConfig.DEFAULT_FONT, font_size=36, color=C_TEXT
        )
        line2 = VGroup(eq2, eq2_desc).arrange(RIGHT, buff=0.15)

        eq3 = MathTex(r"4 - 2 = 2", color=C_TEXT)
        eq3_desc = Text(
            "（只脚）", font=AppConfig.DEFAULT_FONT, font_size=36, color=C_TEXT
        )
        line3 = VGroup(eq3, eq3_desc).arrange(RIGHT, buff=0.15)

        eq4 = MathTex(r"16 \div 2 = 8", color=C_HL)
        eq4_desc = Text(
            "（只兔）", font=AppConfig.DEFAULT_FONT, font_size=36, color=C_HL
        )
        line4 = VGroup(eq4, eq4_desc).arrange(RIGHT, buff=0.15)

        ans_rabbit = Text(
            "兔 = 8 只",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_GREEN,
            weight="BOLD",
        )
        ans_chicken = Text(
            "鸡 = 20 - 8 = 12 只",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_BLUE,
            weight="BOLD",
        )
        final_group = VGroup(ans_rabbit, ans_chicken).arrange(DOWN, buff=0.3)

        formulas = VGroup(line1, line2, line3, line4, final_group).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )

        # 横向安全：不超过 SAFE_WIDTH
        if formulas.width > safe_w:
            formulas.scale_to_fit_width(safe_w)

        # 纵向安全：底部不得低于 SAFE_Y_BOTTOM
        avail_h = grid_bottom - safe_bottom - 0.6
        if formulas.height > avail_h:
            formulas.scale_to_fit_height(avail_h)

        formulas.next_to(animals, DOWN, buff=0.5)
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

        # 将前 8 只鸡"变成"兔（变色 + 添 2 只脚）
        with self.voiceover("所以少的 16 只脚，就是 8 只兔子。"):
            transforms = []
            for i in range(8):
                old = animals[i]
                new_rabbit = make_rabbit()
                new_rabbit.move_to(old.get_center())
                new_rabbit.set(width=old.width)
                transforms.append(
                    ReplacementTransform(old, new_rabbit)
                )
                animals[i] = new_rabbit
            self.play(
                *transforms,
                Write(line4),
                run_time=2.0,
            )
        self.wait(0.3)

        with self.voiceover("答案是兔子 8 只，鸡 12 只。"):
            self.play(Write(final_group), run_time=1.2)
        self.wait(2.0)
