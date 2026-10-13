"""
《代数极值与最短路径》演示视频
竖屏暗黑霓虹风 · 9:16

题目：已知 a + b = 6，求 sqrt(a^2+9) + sqrt(b^2+25) 的最小值。
几何降维：转化为两条斜边之和，利用两点之间直线最短求解。
"""

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class ShortestPathProblem(MathExplainScene):
    def construct(self):
        # ============ 全局几何缩放（竖屏收窄，线段 6 缩放为 4.8） ============
        s = 0.8
        L = 6 * s        # 底边 a+b 总长
        H1 = 3 * s       # 青色垂线高
        H2 = 5 * s       # 黄色垂线高
        H_big = 8 * s    # 大三角形高 (3+5)

        # 坐标锚点（以画面中心 y=0 为几何底边）
        A = np.array([-L / 2, 0, 0])          # 底边左端点
        C = np.array([L / 2, 0, 0])           # 底边右端点
        J = np.array([0, 0, 0])               # a 与 b 的接点（中点演示）
        P = A + UP * H1                       # 青色垂线顶端（上）
        Q = C + DOWN * H2                     # 黄色垂线底端（下）

        # ============================================================
        # 第一幕：引出题目（居中偏上）
        # ============================================================
        title = Text(
            "已知：a + b = 6",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            color=AppConfig.COLOR_TITLE,
        )
        title.to_edge(UP, buff=1.2)

        formula = MathTex(
            r"\sqrt{a^2+9} + \sqrt{b^2+25}",
            font_size=48,
            color=AppConfig.COLOR_TEXT,
        )
        formula.next_to(title, DOWN, buff=0.6)

        # 防越界校验
        if formula.width > AppConfig.MAX_RIGHT_WIDTH:
            formula.scale_to_fit_width(AppConfig.MAX_RIGHT_WIDTH)

        with self.voiceover("已知 a 加 b 等于 6，求这个复杂根式之和的最小值。"):
            self.play(Write(title), run_time=AppConfig.FAST_TEXT_RUNTIME)
            self.play(Write(formula), run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # ============================================================
        # 第二幕：丝滑形变（9→3², 25→5²）
        # ============================================================
        formula_sq = MathTex(
            r"\sqrt{a^2+3^2} + \sqrt{b^2+5^2}",
            font_size=48,
            color=AppConfig.COLOR_TEXT,
        )
        formula_sq.move_to(formula)

        with self.voiceover("注意看，9和25是两个完全平方数，果断改写！"):
            self.play(TransformMatchingTex(formula, formula_sq), run_time=1.2)

        # 形变完成后，将公式移到屏幕最上方，腾出中央舞台
        formula_sq.target = formula_sq.generate_target()
        formula_sq.target.to_edge(UP, buff=0.3).scale(0.8)
        self.play(MoveToTarget(formula_sq), run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # ============================================================
        # 第三幕：几何降维打击（画面正中央）
        # ============================================================
        # 底边 a (青色) + b (黄色)
        seg_a = Line(A, J, color=AppConfig.COLOR_LINE_1, stroke_width=6)
        seg_b = Line(J, C, color=AppConfig.COLOR_LINE_2, stroke_width=6)
        base_group = VGroup(seg_a, seg_b)

        label_a = Text("a", font=AppConfig.DEFAULT_FONT, font_size=28,
                       color=AppConfig.COLOR_LINE_1).next_to(seg_a, UP, buff=0.15)
        label_b = Text("b", font=AppConfig.DEFAULT_FONT, font_size=28,
                       color=AppConfig.COLOR_LINE_2).next_to(seg_b, UP, buff=0.15)
        label_6 = Text("6", font=AppConfig.DEFAULT_FONT, font_size=30,
                       color=AppConfig.COLOR_TITLE).next_to(base_group, DOWN, buff=0.2)

        with self.voiceover("这其实是求两条斜边之和！我们画一条线段代表a，再画一条代表b，合在一起长度就是6。"):
            self.play(Create(seg_a), Create(seg_b), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.play(Write(label_a), Write(label_b), Write(label_6),
                      run_time=AppConfig.FAST_TEXT_RUNTIME)

        # 两条垂线（青色 3 向上，黄色 5 向下）
        vert_cyan = Line(A, P, color=AppConfig.COLOR_LINE_1, stroke_width=6)
        vert_yellow = Line(C, Q, color=AppConfig.COLOR_LINE_2, stroke_width=6)

        label_3 = Text("3", font=AppConfig.DEFAULT_FONT, font_size=28,
                       color=AppConfig.COLOR_LINE_1).next_to(vert_cyan, LEFT, buff=0.15)
        label_5 = Text("5", font=AppConfig.DEFAULT_FONT, font_size=28,
                       color=AppConfig.COLOR_LINE_2).next_to(vert_yellow, RIGHT, buff=0.15)

        # 两条红色斜边（折线）
        hyp1 = Line(P, J, color=AppConfig.COLOR_HIGHLIGHT, stroke_width=5)
        hyp2 = Line(J, Q, color=AppConfig.COLOR_HIGHLIGHT, stroke_width=5)
        broken_path = VGroup(hyp1, hyp2)

        with self.voiceover("接着画两条垂线段，代表3和5，连接起来构造出两个直角三角形。"):
            self.play(Create(vert_cyan), Create(vert_yellow),
                      run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.play(Write(label_3), Write(label_5),
                      run_time=AppConfig.FAST_TEXT_RUNTIME)
            self.play(Create(hyp1), Create(hyp2),
                      run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # ============================================================
        # 第四幕：空间重组与破题（核心高潮）
        # ============================================================
        # 大直角三角形包围盒：底边 6，高 8
        # 顶点 P(左上)、R(右上)、Q(右下)
        R = np.array([C[0], P[1], 0])   # 右上角
        big_top = DashedLine(P, R, color=AppConfig.COLOR_TEXT,
                             stroke_width=3, dash_length=0.15)
        big_right = DashedLine(R, Q, color=AppConfig.COLOR_TEXT,
                               stroke_width=3, dash_length=0.15)

        with self.voiceover("题目要求两条斜边之和何时最小。我们把图形补齐，构建一个大直角三角形。"):
            self.play(Create(big_top), Create(big_right),
                      run_time=AppConfig.FAST_SHAPE_RUNTIME)

        # 大斜边（连接 P 与 Q 的直线，最短路径）
        big_hyp = Line(P, Q, color=AppConfig.COLOR_HIGHLIGHT, stroke_width=8)

        with self.voiceover("根据两点之间直线最短，当这两条斜边变成一条直线时，它正好是这个大三角形的斜边！"):
            self.play(
                Transform(broken_path, big_hyp),
                run_time=1.5,
            )

        # ============================================================
        # 第五幕：终极解答（底部）
        # ============================================================
        answer = MathTex(
            r"\sqrt{6^2+8^2} = 10",
            font_size=52,
            color=AppConfig.COLOR_HIGHLIGHT,
        )
        answer.to_edge(DOWN, buff=1.5)

        # 防越界校验
        if answer.width > AppConfig.MAX_RIGHT_WIDTH:
            answer.scale_to_fit_width(AppConfig.MAX_RIGHT_WIDTH)

        with self.voiceover("底边是6，高是8，根据勾股定理，最短距离就是10。拓展数学思维，你学会了吗？"):
            self.play(Write(answer), run_time=AppConfig.FAST_SHAPE_RUNTIME)
            self.wait(2)
