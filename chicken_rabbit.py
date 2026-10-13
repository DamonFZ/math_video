"""
《鸡兔同笼：假设法》竖屏暗黑风 · 抖音大字报版

视觉目标：字体极大、核心图形撑满横向 ~85%，暗黑网格背景。

重要坐标约定（实测 -r 1080,1920 下 camera.frame=14.222 x 25.284）：
  - Y 范围 [-12.64, 12.64]
  - 注意：to_edge() 内部使用 config.frame_height=8.0，会导致定位错乱，
    因此本视频全部采用绝对 Y 坐标布局。
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig

YELLOW = "#FFEB3B"
CYAN = "#00E5FF"
RED = "#FF1744"
WHITE = "#FFFFFF"
GRAY = "#E0E0E0"

# 实际帧半高（camera.frame_height / 2）
FRAME_HALF_H = 12.64


class ChickenRabbit(MathExplainScene):
    def construct(self):
        safe_w = AppConfig.SAFE_WIDTH  # 12.0 ≈ 帧宽的 85%

        # ============================================================
        # 1. 顶部：大字报标题（两行分离 + 撑满横向）
        # ============================================================
        title_main = Text(
            "鸡兔同笼 (假设法)",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            weight=BOLD,
            color=YELLOW,
        )
        title_detail = Text(
            "共 20 只，56 只脚。鸡兔各多少？",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=WHITE,
        )
        title_group = VGroup(title_main, title_detail).arrange(DOWN, buff=0.4)
        if title_group.width > safe_w:
            title_group.scale_to_fit_width(safe_w)
        # 绝对坐标置顶（顶部留白 ~1.0）
        title_top_y = FRAME_HALF_H - 1.0
        title_group.shift(UP * (title_top_y - title_group.get_top()[1]))

        with self.voiceover(text="经典的鸡兔同笼问题，教你用假设法一秒看破！"):
            self.play(Write(title_group), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # ============================================================
        # 2. 中部：20 只动物网格（撑满横向 + 加粗线条）
        # ============================================================
        animals = VGroup()
        for _ in range(20):
            head = Circle(radius=0.4, color=YELLOW, fill_opacity=0.35, stroke_width=8)
            foot_l = Line(
                head.get_bottom() + LEFT * 0.12,
                head.get_bottom() + DOWN * 0.15 + LEFT * 0.12,
                color=YELLOW, stroke_width=8,
            )
            foot_r = Line(
                head.get_bottom() + RIGHT * 0.12,
                head.get_bottom() + DOWN * 0.15 + RIGHT * 0.12,
                color=YELLOW, stroke_width=8,
            )
            animals.add(VGroup(head, foot_l, foot_r))

        # 紧凑排布（短腿 + 小 buff），让网格宽高比 > 1，利于撑满横向
        animals.arrange_in_grid(rows=4, cols=5, buff=0.3)

        # 撑满横向安全宽度
        animals.scale_to_fit_width(safe_w)

        # 高度保护：网格底部不得侵入公式区
        grid_top_y = title_group.get_bottom()[1] - 1.0
        formulas_start_y = -3.0
        max_grid_height = grid_top_y - (formulas_start_y - 0.5)
        if animals.height > max_grid_height:
            animals.scale_to_fit_height(max_grid_height)

        # 垂直放置：顶部对齐 grid_top_y
        animals.shift(UP * (grid_top_y - animals.get_top()[1]))

        with self.voiceover(text="首先，我们画 20 个圆圈代表这 20 只动物。假设它们全都是鸡！"):
            self.play(*[Create(a[0]) for a in animals],
                      run_time=AppConfig.FAST_SHAPE_RUNTIME)

        with self.voiceover(text="既然全是鸡，每只鸡有 2 只脚，那么此时一共有 20 乘 2 等于 40 只脚。"):
            self.play(
                *[Create(a[1]) for a in animals],
                *[Create(a[2]) for a in animals],
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        # ============================================================
        # 3. 底部深渊：大字号公式瀑布流（font_size=60）
        # ============================================================
        fs = 60

        def make_eq(math_tex, unit, color):
            g = VGroup(
                MathTex(math_tex, font_size=fs, color=color),
                Text(unit, font=AppConfig.DEFAULT_FONT, font_size=fs - 12, color=color),
            ).arrange(RIGHT, buff=0.2)
            if g.width > safe_w:
                g.scale_to_fit_width(safe_w)
            return g

        eq1 = make_eq(r"20 \times 2 = 40", "（只）", GRAY)
        eq1.move_to(DOWN * abs(formulas_start_y))

        with self.voiceover(text="20 乘 2 等于 40 只脚。"):
            self.play(Write(eq1), run_time=AppConfig.FAST_TEXT_RUNTIME)

        eq2 = make_eq(r"56 - 40 = 16", "（只）", RED)
        eq2.next_to(eq1, DOWN, buff=0.7)

        with self.voiceover(text="但是题目说有 56 只脚，还差了 16 只脚，这 16 只脚去哪了呢？"):
            self.play(Write(eq2), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # ============================================================
        # 4. 核心高潮：鸡变兔
        # ============================================================
        eq3 = make_eq(r"4 - 2 = 2", "（只/兔）", CYAN)
        eq3.next_to(eq2, DOWN, buff=0.7)

        with self.voiceover(text="因为我们把兔子也当成了鸡！每只兔子比鸡多出 2 只脚。"):
            self.play(Write(eq3), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # 给前 8 只补 2 条腿并变色
        rabbit_legs = VGroup()
        for i in range(8):
            head = animals[i][0]
            bottom = head.get_bottom()
            r = head.radius
            el = Line(bottom + LEFT * (r * 0.5), bottom + DOWN * (r * 0.4) + LEFT * (r * 0.5),
                      color=CYAN, stroke_width=8)
            er = Line(bottom + RIGHT * (r * 0.5), bottom + DOWN * (r * 0.4) + RIGHT * (r * 0.5),
                      color=CYAN, stroke_width=8)
            rabbit_legs.add(VGroup(el, er))

        eq4 = make_eq(r"16 \div 2 = 8", "（只兔）", CYAN)
        eq4.next_to(eq3, DOWN, buff=0.7)

        with self.voiceover(text="所以，我们需要把差的 16 只脚，两只两只地补给这些鸡，让它们变回兔子！"):
            self.play(
                *[animals[i].animate.set_color(CYAN) for i in range(8)],
                *[Create(rabbit_legs[i]) for i in range(8)],
                Write(eq4),
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        # ============================================================
        # 5. 总结收尾
        # ============================================================
        final_rabbit = VGroup(
            Text("兔：", font=AppConfig.DEFAULT_FONT, font_size=fs, color=CYAN),
            MathTex("8", font_size=fs, color=CYAN),
            Text("只", font=AppConfig.DEFAULT_FONT, font_size=fs, color=CYAN),
        ).arrange(RIGHT, buff=0.2)
        final_chicken = VGroup(
            Text("鸡：", font=AppConfig.DEFAULT_FONT, font_size=fs, color=YELLOW),
            MathTex("20 - 8 = 12", font_size=fs, color=YELLOW),
            Text("只", font=AppConfig.DEFAULT_FONT, font_size=fs, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        final_group = VGroup(final_rabbit, final_chicken).arrange(DOWN, buff=0.5)
        final_group.next_to(eq4, DOWN, buff=0.7)
        if final_group.width > safe_w:
            final_group.scale_to_fit_width(safe_w)

        with self.voiceover(text="补完发现，一共有 8 只兔子！那鸡的数量就是 20 减 8 等于 12 只。假设法，你学会了吗？"):
            self.play(Write(final_group), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.wait(2)
