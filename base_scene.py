import os
import json
import uuid
import base64
import hashlib

import requests
from manim import *
from manim import config as manim_config
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.base import SpeechService

from config import AppConfig


class VolcengineTTSService(SpeechService):
    """火山引擎 TTS 服务（新版 API Key + V3 seed-tts-2.0 大模型流式接口）。"""

    def __init__(self, voice=AppConfig.TTS_VOICE, speed=AppConfig.TTS_SPEED, **kwargs):
        self.voice = voice
        self.speed = speed
        super().__init__(**kwargs)

    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None, **kwargs
    ) -> dict:
        actual_cache_dir = cache_dir if cache_dir is not None else self.cache_dir

        filename = (
            hashlib.md5((text + self.voice + str(self.speed)).encode()).hexdigest()
            + ".mp3"
        )
        audio_path = path if path else os.path.join(actual_cache_dir, filename)

        if not os.path.exists(audio_path):
            url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"

            # V3 新版控制台鉴权：X-Api-Key + X-Api-Resource-Id
            headers = {
                "X-Api-Key": AppConfig.VOLC_API_KEY,
                "X-Api-Resource-Id": AppConfig.TTS_RESOURCE_ID,
                "X-Api-Request-Id": str(uuid.uuid4()),
                "Content-Type": "application/json",
            }

            # V3 请求体结构
            # speech_rate: [-50, 100]，0=1x，100=2x → (speed-1)*100
            speech_rate = int(round((self.speed - 1.0) * 100))
            payload = {
                "user": {"uid": "manim_video_creator"},
                "namespace": "BidirectionalTTS",
                "req_params": {
                    "text": text,
                    "speaker": self.voice,
                    "audio_params": {
                        "format": "mp3",
                        "speech_rate": speech_rate,
                    },
                },
            }

            print(f"正在通过火山引擎 V3 生成语音: {text[:10]}...")
            response = requests.post(
                url, json=payload, headers=headers, stream=True, timeout=60
            )

            if response.status_code != 200:
                raise Exception(
                    f"HTTP 请求失败, 状态码: {response.status_code}, "
                    f"详情: {response.text}"
                )

            # V3 为 chunked 流式返回，逐行解析 JSON 并拼接 base64 音频
            audio_data = b""
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                chunk = json.loads(line)
                code = chunk.get("code")
                if code not in (0, None, 20000000):
                    raise Exception(
                        f"火山引擎 TTS 报错, code: {code}, "
                        f"message: {chunk.get('message')}"
                    )
                if chunk.get("data"):
                    audio_data += base64.b64decode(chunk["data"])

            if not audio_data:
                raise Exception("火山引擎 TTS 未返回音频数据")

            os.makedirs(actual_cache_dir, exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(audio_data)

        return {"original_audio": filename}


class MathExplainScene(VoiceoverScene):
    """所有数学讲解视频的基类。"""

    def setup(self):
        # 强制竖屏配置
        manim_config.pixel_width = 1080
        manim_config.pixel_height = 1920
        manim_config.frame_height = 14.22
        manim_config.frame_width = 8.0

        super().setup()
        self.set_speech_service(
            VolcengineTTSService(
                voice=AppConfig.TTS_VOICE, speed=AppConfig.TTS_SPEED
            )
        )

        # 强制相机帧为 8.0 x 14.22（manim_config 只改配置不改相机，需直接设 camera）
        self.camera.frame_width = 8.0
        self.camera.frame_height = 14.22

        # 白底草稿纸背景
        self.camera.background_color = "#FFFFFF"

        # 清新浅灰网格线
        bg_grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-20, 20, 1],
            background_line_style={
                "stroke_color": "#E8E8E8",  # 浅灰色，像真实的作业本
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
            faded_line_ratio=0,
        )
        bg_grid.axes.set_opacity(0)  # 隐藏坐标轴主线
        self.add(bg_grid)
