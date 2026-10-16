"""
《年龄差不变：小明与妈妈》竖屏白底草稿本 · 偏左非对称安全区版

核心动画：两条线段（小明/妈妈），同时向右延伸"+10"橙色段，
用大括号标注"相差依然是 30 岁"，直观证明年龄差不变。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from base_scene import MathExplainScene
from config import AppConfig


class AgeDifference(MathExplainScene):
    def construct(self):
        safe_w = AppConfig.SAFE_WIDTH
        safe_cx = AppConfig.SAFE_CENTER_X
        safe_bottom = AppConfig.SAFE_Y_BOTTOM

        C_TEXT = AppConfig.COLOR_TEXT
        C_HL = AppConfig.COLOR_HIGHLIGHT
        C_BLUE = AppConfig.COLOR_LINE_1
        C_GREEN = AppConfig.COLOR_LINE_2

        # ════════════════════════════════════════
        # 1. 顶部：题目展示 (声画分离，起点压低 buff=2.5)
        # ════════════════════════════════════════
        t1 = Text(
            "年龄问题 (易错题)",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.TITLE_FONT_SIZE,
            color=C_HL,
            weight="BOLD",
        )
        t2 = Text(
            "小明6岁，妈36岁。10年后妈妈大几岁？",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_TEXT,
        )
        title_group = VGroup(t1, t2).arrange(DOWN, buff=0.35)
        title_group.scale_to_fit_width(safe_w)
        title_group.to_edge(UP, buff=2.5)
        title_group.set_x(safe_cx)

        # IP 专属 Hook：仅配音，不渲染文字（SOP 铁律 7）
        with self.voiceover("小时候怎么没想到，这种年龄差问题其实有秒杀的绝招！"):
            self.play(Write(title_group), run_time=1.5)
        self.wait(0.3)

        # ════════════════════════════════════════
        # 2. 中部：核心动画区 (0 < Y < 4)
        # ════════════════════════════════════════
        # 线段基准：左端点统一在 x=0，向右延伸（整体打包后再定位）
        xm_len = 1.5   # 小明线段
        mom_len = 6.0  # 妈妈线段
        add_len = 2.5  # 10年后延伸段

        xiao_bar = Line(ORIGIN, xm_len * RIGHT, color=C_BLUE, stroke_width=14)
        xiao_label = Text("小明: 6岁", font=AppConfig.DEFAULT_FONT,
                          font_size=30, color=C_BLUE).next_to(xiao_bar, UP, buff=0.2)

        mom_bar = Line(ORIGIN, mom_len * RIGHT, color=C_GREEN, stroke_width=14)
        mom_label = Text("妈妈: 36岁", font=AppConfig.DEFAULT_FONT,
                         font_size=30, color=C_GREEN).next_to(mom_bar, UP, buff=0.2)

        xiao_group = VGroup(xiao_bar, xiao_label)
        mom_group = VGroup(mom_bar, mom_label)
        # 两根线段的垂直间距拉开（舒展瀑布流）
        bars = VGroup(xiao_group, mom_group).arrange(DOWN, buff=1.3)

        # 延伸段（预构建，初始隐藏）
        xiao_add = Line(xiao_bar.get_end(), xiao_bar.get_end() + add_len * RIGHT,
                        color=C_HL, stroke_width=14)
        mom_add = Line(mom_bar.get_end(), mom_bar.get_end() + add_len * RIGHT,
                       color=C_HL, stroke_width=14)
        xiao_add_label = Text("+10", font=AppConfig.DEFAULT_FONT, font_size=26, color=C_HL
                              ).move_to(xiao_add.get_center()).shift(UP * 0.35)
        mom_add_label = Text("+10", font=AppConfig.DEFAULT_FONT, font_size=26, color=C_HL
                             ).move_to(mom_add.get_center()).shift(UP * 0.35)

        # 初始大括号：今年的长度差
        diff_brace = Brace(Line(xiao_bar.get_end(), mom_bar.get_end()), RIGHT, color=C_HL)
        diff_label = Text("相差 30 岁", font=AppConfig.DEFAULT_FONT,
                          font_size=30, color=C_HL).next_to(diff_brace, RIGHT, buff=0.15)

        # 延伸后大括号：10年后的长度差
        new_diff_brace = Brace(Line(xiao_add.get_end(), mom_add.get_end()), RIGHT, color=C_HL)
        new_diff_label = Text("相差依然是 30 岁！", font=AppConfig.DEFAULT_FONT,
                              font_size=30, color=C_HL, weight="BOLD"
                              ).next_to(new_diff_brace, RIGHT, buff=0.15)

        # 完整图形统一打包 → 缩放 → 偏左对齐 → 定位
        full_graphic = VGroup(
            bars, diff_brace, diff_label,
            xiao_add, mom_add, xiao_add_label, mom_add_label,
            new_diff_brace, new_diff_label,
        )
        full_graphic.scale_to_fit_width(safe_w * 0.9)
        full_graphic.set_x(safe_cx)
        full_graphic.next_to(title_group, DOWN, buff=1.5)

        # 先隐藏后出现的元素
        for mob in [xiao_add, mom_add, xiao_add_label, mom_add_label,
                    new_diff_brace, new_diff_label]:
            mob.set_opacity(0)

        with self.voiceover("今年，妈妈比小明大 36 减 6 等于 30 岁。"):
            self.play(Create(xiao_bar), Create(mom_bar), run_time=0.8)
            self.play(Write(xiao_label), Write(mom_label), run_time=0.6)
            self.play(GrowFromCenter(diff_brace), Write(diff_label), run_time=0.8)
        self.wait(0.3)

        with self.voiceover("时间对每个人都是公平的！10年后，小明长了10岁，妈妈也长了10岁。"):
            self.play(
                Create(xiao_add), Create(mom_add),
                Write(xiao_add_label), Write(mom_add_label),
                run_time=1.2,
            )
        self.wait(0.3)

        with self.voiceover("你看，两人都加了同样的岁数，所以相差依然是 30 岁！"):
            self.play(FadeOut(diff_brace), FadeOut(diff_label), run_time=0.4)
            self.play(GrowFromCenter(new_diff_brace), run_time=0.6)
            self.play(Write(new_diff_label), new_diff_label.animate.scale(1.15), run_time=0.6)
        self.wait(0.4)

        # ════════════════════════════════════════
        # 3. 底部：结论推导 (Y < 0，瀑布流)
        # ════════════════════════════════════════
        def make_eq(prefix, math_str, suffix):
            p = Text(prefix, font=AppConfig.DEFAULT_FONT, font_size=40, color=C_TEXT)
            m = MathTex(math_str, font_size=44, color=C_TEXT)
            s = Text(suffix, font=AppConfig.DEFAULT_FONT, font_size=40, color=C_TEXT)
            return VGroup(p, m, s).arrange(RIGHT, buff=0.15)

        eq1 = make_eq("今年：", r"36 - 6 = 30", "(岁)")
        eq2 = make_eq("10年后：", r"46 - 16 = 30", "(岁)")
        # 行间距按新 SOP 加大到 1.0
        equations = VGroup(eq1, eq2).arrange(DOWN, buff=1.0)
        if equations.width > safe_w:
            equations.scale_to_fit_width(safe_w)

        conclusion = Text(
            "结论：年龄差永远不变！",
            font=AppConfig.DEFAULT_FONT,
            font_size=AppConfig.NORMAL_FONT_SIZE,
            color=C_HL, weight="BOLD",
        )
        final_answer = Text(
            "= 30 岁",
            font=AppConfig.DEFAULT_FONT,
            font_size=68, color=C_GREEN, weight="BOLD",
        )
        result_group = VGroup(conclusion, final_answer).arrange(DOWN, buff=0.3)
        if result_group.width > safe_w:
            result_group.scale_to_fit_width(safe_w)

        # 底部整体瀑布流栈：算式区 + 结论区打包，统一做纵向预算
        # 可用高度 = 图形底 - 1.5 间距 - 底部警戒线
        bottom_stack = VGroup(equations, result_group).arrange(DOWN, buff=0.8)
        avail_h = full_graphic.get_bottom()[1] - 1.5 - safe_bottom
        if bottom_stack.height > avail_h:
            bottom_stack.scale_to_fit_height(avail_h)
        bottom_stack.next_to(full_graphic, DOWN, buff=1.5)
        bottom_stack.set_x(safe_cx)

        # 底部安全区兜底：整栈上移，确保不低于警戒线
        if bottom_stack.get_bottom()[1] < safe_bottom:
            bottom_stack.shift(UP * (safe_bottom - bottom_stack.get_bottom()[1]))

        with self.voiceover("算式验证一下，也是30岁。所以，无论过多少年，年龄差永远不变！"):
            self.play(Write(equations), run_time=1.2)
        self.wait(0.3)

        with self.voiceover("记住这个秘诀，年龄问题一秒出答案！关注我，每天学点数学思维。"):
            self.play(Write(conclusion), run_time=0.8)
            self.play(Write(final_answer), Circumscribe(final_answer, color=C_GREEN), run_time=1.0)
        self.wait(2.0)
