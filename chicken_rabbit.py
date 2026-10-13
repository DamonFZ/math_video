"""
《鸡兔同笼：假设法》竖屏暗黑风短视频

题目：笼子里有鸡和兔共 20 只，脚共有 56 只。鸡和兔各有多少只？

Y 轴三段式绝对分层（防重叠结界）：
  - 顶部结界 (Y > 4)：仅题目文字
  - 中部舞台 (0 < Y < 4)：仅图形动画
  - 底部深渊 (Y < 0)：所有推导公式，从 Y=0 向下瀑布流排列
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig

YELLOW = "#FFEB3B"
CYAN = "#00E5FF"
RED = "#FF1744"
WHITE = "#FFFFFF"
GRAY = "#E0E0E0"


class ChickenRabbit(MathExplainScene):
    def setup(self):
        super().setup()
        # 仅设置黑底，绝不修改分辨率配置
        self.camera.background_color = "#000000"
        for mob in self.mobjects:
            mob.set_opacity(0.12)

    def construct(self):
        # ============================================================
        # 1. 顶部结界 (Y > 4)：提出问题
        # ============================================================
        question = Text(
            "鸡兔同笼：共 20 只，56 只脚。\n鸡兔各多少？",
            font=AppConfig.DEFAULT_FONT,
            font_size=34,
            color=WHITE,
            line_spacing=1.2,
        )
        question.move_to(UP * 5.5)  # Y=5.5，严格位于顶部结界

        with self.voiceover(text="经典的鸡兔同笼问题，教你用假设法一秒看破！"):
            self.play(Write(question), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # ============================================================
        # 2. 中部舞台 (0 < Y < 4)：全员变鸡
        # ============================================================
        animals = VGroup()
        for _ in range(20):
            head = Circle(radius=0.4, color=YELLOW, fill_opacity=0.35)
            # 两只鸡脚，从头部底部分开向下
            foot_l = Line(
                head.get_bottom() + LEFT * 0.12,
                head.get_bottom() + DOWN * 0.35 + LEFT * 0.12,
                color=YELLOW, stroke_width=4,
            )
            foot_r = Line(
                head.get_bottom() + RIGHT * 0.12,
                head.get_bottom() + DOWN * 0.35 + RIGHT * 0.12,
                color=YELLOW, stroke_width=4,
            )
            animal = VGroup(head, foot_l, foot_r)
            animals.add(animal)

        animals.arrange_in_grid(rows=4, cols=5, buff=0.5)
        # 等比缩放并锁定中部舞台 (0 < Y < 4)
        animals.scale_to_fit_height(3.0)
        if animals.width > 6.5:
            animals.scale_to_fit_width(6.5)
        animals.move_to(UP * 2.0)  # 中心 Y=2.0

        with self.voiceover(text="首先，我们画 20 个圆圈代表这 20 只动物。假设它们全都是鸡！"):
            self.play(
                *[Create(a[0]) for a in animals],
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        with self.voiceover(text="既然全是鸡，每只鸡有 2 只脚，那么此时一共有 20 乘 2 等于 40 只脚。"):
            self.play(
                *[Create(a[1]) for a in animals],
                *[Create(a[2]) for a in animals],
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        # ============================================================
        # 3. 底部深渊 (Y < 0)：计算差额（瀑布流）
        # ============================================================
        eq1 = VGroup(
            MathTex(r"20 \times 2 = 40", font_size=38, color=GRAY),
            Text("（只）", font=AppConfig.DEFAULT_FONT, font_size=28, color=GRAY),
        ).arrange(RIGHT, buff=0.15)
        eq1.move_to(DOWN * 1.0)  # 瀑布流起点 Y=-1

        with self.voiceover(text="20 乘 2 等于 40 只脚。"):
            self.play(Write(eq1), run_time=AppConfig.FAST_TEXT_RUNTIME)

        eq2 = VGroup(
            MathTex(r"56 - 40 = 16", font_size=38, color=RED),
            Text("（只）", font=AppConfig.DEFAULT_FONT, font_size=28, color=RED),
        ).arrange(RIGHT, buff=0.15)
        eq2.next_to(eq1, DOWN, buff=0.55)

        with self.voiceover(text="但是题目说有 56 只脚，还差了 16 只脚，这 16 只脚去哪了呢？"):
            self.play(Write(eq2), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # ============================================================
        # 4. 核心高潮：鸡变兔
        # ============================================================
        eq3 = VGroup(
            MathTex(r"4 - 2 = 2", font_size=38, color=CYAN),
            Text("（只/兔）", font=AppConfig.DEFAULT_FONT, font_size=28, color=CYAN),
        ).arrange(RIGHT, buff=0.15)
        eq3.next_to(eq2, DOWN, buff=0.55)

        with self.voiceover(text="因为我们把兔子也当成了鸡！每只兔子比鸡多出 2 只脚。"):
            self.play(Write(eq3), run_time=AppConfig.FAST_TEXT_RUNTIME)

        # 给前 8 只动物补上 2 条额外腿并变色为青色（兔子）
        rabbit_legs = VGroup()
        for i in range(8):
            animal = animals[i]
            head = animal[0]
            bottom = head.get_bottom()
            r = head.radius
            extra_l = Line(
                bottom + LEFT * (r * 0.5),
                bottom + DOWN * (r * 0.9) + LEFT * (r * 0.5),
                color=CYAN, stroke_width=4,
            )
            extra_r = Line(
                bottom + RIGHT * (r * 0.5),
                bottom + DOWN * (r * 0.9) + RIGHT * (r * 0.5),
                color=CYAN, stroke_width=4,
            )
            rabbit_legs.add(VGroup(extra_l, extra_r))

        eq4 = VGroup(
            MathTex(r"16 \div 2 = 8", font_size=38, color=CYAN),
            Text("（只兔）", font=AppConfig.DEFAULT_FONT, font_size=28, color=CYAN),
        ).arrange(RIGHT, buff=0.15)
        eq4.next_to(eq3, DOWN, buff=0.55)

        with self.voiceover(text="所以，我们需要把差的 16 只脚，两只两只地补给这些鸡，让它们变回兔子！"):
            # 前 8 只变色 + 长出额外腿
            self.play(
                *[animals[i].animate.set_color(CYAN) for i in range(8)],
                *[Create(rabbit_legs[i]) for i in range(8)],
                Write(eq4),
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        # ============================================================
        # 5. 总结收尾（屏幕最下方）
        # ============================================================
        final_rabbit = VGroup(
            Text("兔：", font=AppConfig.DEFAULT_FONT, font_size=30, color=CYAN),
            MathTex("8", font_size=40, color=CYAN),
            Text("只", font=AppConfig.DEFAULT_FONT, font_size=30, color=CYAN),
        ).arrange(RIGHT, buff=0.15)
        final_chicken = VGroup(
            Text("鸡：", font=AppConfig.DEFAULT_FONT, font_size=30, color=YELLOW),
            MathTex("20 - 8 = 12", font_size=40, color=YELLOW),
            Text("只", font=AppConfig.DEFAULT_FONT, font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.15)
        final_group = VGroup(final_rabbit, final_chicken).arrange(DOWN, buff=0.4)
        final_group.next_to(eq4, DOWN, buff=0.7)

        # 防越界：底部公式组宽度限制
        if final_group.width > 6.0:
            final_group.scale_to_fit_width(6.0)

        with self.voiceover(text="补完发现，一共有 8 只兔子！那鸡的数量就是 20 减 8 等于 12 只。假设法，你学会了吗？"):
            self.play(Write(final_group), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.wait(2)
