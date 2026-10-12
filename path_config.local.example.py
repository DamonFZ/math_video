"""
本机专属路径配置模板（会被 git 跟踪，作为示例）

使用方法：
1. 复制本文件为 path_config.local.py
2. 将 MANIM_ENV_ROOT 改为你本机 manim-env 虚拟环境的实际路径
3. path_config.local.py 已在 .gitignore 中忽略，不会同步到其他电脑
"""

from pathlib import Path

# 本机 manim-env 虚拟环境根目录（按实际情况修改）
MANIM_ENV_ROOT = Path.home() / "manim_projects" / "manim-env"
