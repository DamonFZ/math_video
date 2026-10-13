"""
《代数极值与将军饮马模型》竖屏暗黑风演示视频

题目：已知 a + b = 6，求 sqrt(a^2+9) + sqrt(b^2+25) 的最小值。
几何模型：转化为两条斜边之和，两点之间直线最短 → 大直角三角形斜边 = 10。

架构铁律：
- 分辨率严禁在代码中修改，一律通过 CLI `-r 1080,1920` 注入；
- 几何由精确坐标点位生成，打包 VGroup 后统一 scale_to_fit_width 等比缩放；
- 缩放后的附属元素（虚线、大斜边、标注）一律从实际点位 (.get_end/.get_center) 取值。
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class ShortestPathProblem(MathExplainScene):
    def setup(self):
        super().setup()
        # 仅设置黑底，绝不修改分辨率配置
        self.camera.background_color = "#000000"
        # 暗化基类自带的作业本网格，使其在黑底上几乎不可见
        for mob in self.mobjects:
            mob.set_opacity(0.12)

    def construct(self):
        # ============================================================
        # 1. 顶部公式区（动态让位）
        # ============================================================
        condition = Text(
            "已知: a + b = 6",
            font=AppConfig.DEFAULT_FONT,
            color="#FFFFFF",
            font_size=36,
        )
        target_eq1 = MathTex(
            r"\sqrt{a^2+9} + \sqrt{b^2+25}",
            font_size=42,
            color="#E0E0E0",
        )
        target_eq2 = MathTex(
            r"\sqrt{a^2+3^2} + \sqrt{b^2+5^2}",
            font_size=42,
            color="#E0E0E0",
        )

        top_group = VGroup(condition, target_eq1).arrange(DOWN, buff=0.5)
        top_group.move_to(UP * 3.0)  # 绝对坐标放置，避免 to_edge 越界

        with self.voiceover(text="已知 a 加 b 等于 6，求这个复杂根式之和的最小值。"):
            self.play(Write(top_group), run_time=AppConfig.FAST_TEXT_RUNTIME)

        with self.voiceover(text="注意看，9和25是完全平方数，我们可以果断把它改写为3的平方和5的平方。"):
            self.play(
                TransformMatchingTex(target_eq1, target_eq2),
                run_time=AppConfig.FAST_SHAPE_RUNTIME,
            )

        # 将公式推到最顶部，为几何腾出中央舞台
        self.play(
            condition.animate.shift(UP * 2.0).scale(0.8),
            target_eq2.animate.shift(UP * 2.5).scale(0.8),
        )

        # ============================================================
        # 2. 中央几何区（严谨坐标点位防拉伸）
        # ============================================================
        # 逻辑锚点：总长 a+b=6，取 a=2, b=4 演示
        P_left = np.array([-3, 0, 0])
        P_mid = np.array([-1, 0, 0])
        P_right = np.array([3, 0, 0])
        P_top = np.array([-3, 3, 0])      # a 的垂线顶点（高 3，向上）
        P_bottom = np.array([3, -5, 0])   # b 的垂线底点（高 5，向下）

        line_a = Line(P_left, P_mid, color="#00E5FF", stroke_width=6)
        line_b = Line(P_mid, P_right, color="#FFEB3B", stroke_width=6)
        line_3 = Line(P_left, P_top, color="#00E5FF", stroke_width=6)
        line_5 = Line(P_right, P_bottom, color="#FFEB3B", stroke_width=6)

        hypo_1 = Line(P_top, P_mid, color="#FF1744", stroke_width=6)
        hypo_2 = Line(P_mid, P_bottom, color="#FF1744", stroke_width=6)

        # 打包所有几何元素，统一等比缩放并居中，防止越界与拉伸
        geo_group = VGroup(line_a, line_b, line_3, line_5, hypo_1, hypo_2)
        geo_group.scale_to_fit_width(6.0).move_to(DOWN * 1.0)

        with self.voiceover(text="这其实是求两条斜边之和。我们画一条长为6的线段，分为a和b。分别向上和向下作长度为3和5的垂线，连接出两条斜边。"):
            self.play(Create(line_a), Create(line_b), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.play(Create(line_3), Create(line_5), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.play(Create(hypo_1), Create(hypo_2), run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # 标注（基于缩放后的实际点位定位，保证对齐完美）
        label_3 = Text("3", font=AppConfig.DEFAULT_FONT, font_size=28, color="#00E5FF")
        label_3.move_to(line_3.get_center() + LEFT * 0.35)
        label_5 = Text("5", font=AppConfig.DEFAULT_FONT, font_size=28, color="#FFEB3B")
        label_5.move_to(line_5.get_center() + RIGHT * 0.35)
        label_a = Text("a", font=AppConfig.DEFAULT_FONT, font_size=28, color="#00E5FF")
        label_a.move_to(line_a.get_center() + UP * 0.3)
        label_b = Text("b", font=AppConfig.DEFAULT_FONT, font_size=28, color="#FFEB3B")
        label_b.move_to(line_b.get_center() + UP * 0.3)
        label_6 = Text("6", font=AppConfig.DEFAULT_FONT, font_size=30, color="#FFFFFF")
        label_6.move_to((line_a.get_start() + line_b.get_end()) / 2 + DOWN * 0.35)

        self.play(
            Write(label_3), Write(label_5),
            Write(label_a), Write(label_b), Write(label_6),
            run_time=AppConfig.FAST_TEXT_RUNTIME,
        )

        # ============================================================
        # 3. 虚线补全大三角形（从实际点位构建，完美对齐）
        # ============================================================
        top_pt = line_3.get_end()       # 青色垂线顶端
        bot_pt = line_5.get_end()       # 黄色垂线底端
        # 大直角顶点：与 top_pt 同高、与 bot_pt 同横坐标
        corner = np.array([bot_pt[0], top_pt[1], 0])

        dash_top = DashedLine(top_pt, corner, color=WHITE,
                              stroke_width=3, dash_length=0.15)
        dash_right = DashedLine(corner, bot_pt, color=WHITE,
                                stroke_width=3, dash_length=0.15)

        with self.voiceover(text="把图形补齐，构建一个大直角三角形。"):
            self.play(Create(dash_top), Create(dash_right),
                      run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # ============================================================
        # 4. 最短路径形变（折线 → 直线）
        # ============================================================
        straight_hypo = Line(top_pt, bot_pt, color="#FF1744", stroke_width=8)

        with self.voiceover(text="根据两点之间直线最短，当这两条折线拉直时，正好是大三角形的斜边！"):
            self.play(
                Transform(VGroup(hypo_1, hypo_2), straight_hypo),
                run_time=1.4,
            )

        # ============================================================
        # 5. 结论区
        # ============================================================
        final_text = MathTex(
            r"\sqrt{6^2+8^2} = 10",
            font_size=48,
            color="#FF1744",
        )
        final_text.to_edge(DOWN, buff=1.0)

        # 防越界校验
        if final_text.width > AppConfig.MAX_RIGHT_WIDTH:
            final_text.scale_to_fit_width(AppConfig.MAX_RIGHT_WIDTH)

        with self.voiceover(text="底边是6，高是8，勾股定理算出最短距离就是10！"):
            self.play(Write(final_text), run_time=AppConfig.FAST_SHAPE_RUNTIME)

        self.wait(2)
