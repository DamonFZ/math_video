"""
项目全局路径配置

集中管理项目根目录、Manim 虚拟环境等关键路径，
避免在各场景脚本中硬编码绝对路径，便于跨环境迁移。

注意：Manim 虚拟环境的本机路径（MANIM_ENV_ROOT）因两台电脑安装位置不同，
统一放在本目录下的 ``path_config.local.py`` 中（已 gitignore，不同步）。
本文件只定义共享逻辑与默认值；若本地文件存在则覆盖默认值。
"""

import importlib.util
from pathlib import Path

# === 项目根目录 ===
# 本文件所在目录即为项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent

# === 场景代码目录 ===
# 存放每一道题的 Manim 场景脚本（此目录已在 .gitignore 中忽略，不参与多机同步）
SCENES_DIR = PROJECT_ROOT / "scenes"

# === Manim 虚拟环境路径 ===
# 默认值：若本机没有 path_config.local.py 则使用此路径
MANIM_ENV_ROOT = Path.home() / "manim_projects" / "manim-env"

# 优先读取本机专属配置（两台电脑各自维护，已 gitignore）
_local_cfg = PROJECT_ROOT / "path_config.local.py"
if _local_cfg.exists():
    _spec = importlib.util.spec_from_file_location("path_config_local", _local_cfg)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)  # type: ignore[union-attr]
    if hasattr(_mod, "MANIM_ENV_ROOT"):
        MANIM_ENV_ROOT = Path(_mod.MANIM_ENV_ROOT)

# manim 可执行文件路径（用于命令行渲染）
MANIM_BIN = MANIM_ENV_ROOT / "bin" / "manim"

# manim-env 的 Python 解释器路径
PYTHON_BIN = MANIM_ENV_ROOT / "bin" / "python"

# === 媒体输出目录 ===
MEDIA_DIR = PROJECT_ROOT / "media"
VIDEOS_DIR = MEDIA_DIR / "videos"
TEX_DIR = MEDIA_DIR / "Tex"
TEXTS_DIR = MEDIA_DIR / "texts"

# === 语音缓存目录 ===
VOICEOVER_CACHE_DIR = MEDIA_DIR / "voiceovers"


if __name__ == "__main__":
    # 自检：打印所有路径并检查关键路径是否存在
    print("=== 项目路径自检 ===")
    print(f"项目根目录:   {PROJECT_ROOT}  {'[存在]' if PROJECT_ROOT.exists() else '[缺失]'}")
    print(f"场景目录:     {SCENES_DIR}  {'[存在]' if SCENES_DIR.exists() else '[缺失]'}")
    print(f"Manim 环境:   {MANIM_ENV_ROOT}  {'[存在]' if MANIM_ENV_ROOT.exists() else '[缺失]'}")
    print(f"Manim 可执行: {MANIM_BIN}  {'[存在]' if MANIM_BIN.exists() else '[缺失]'}")
    print(f"Python 解释器: {PYTHON_BIN}  {'[存在]' if PYTHON_BIN.exists() else '[缺失]'}")
    print(f"媒体目录:     {MEDIA_DIR}  {'[存在]' if MEDIA_DIR.exists() else '[缺失]'}")
