#!/usr/bin/env python3
"""
用法：
    # 仅裁切（原有功能）
    python scripts/crop-cover.py <图片路径>

    # 先去除背景，再裁切
    python scripts/crop-cover.py --remove-bg <图片路径>

API Key 自动从项目根目录 .env 文件读取（REMOVE_BG_API_KEY=xxx）。

将图片居中裁切并缩放至 1200×630（1.9:1），直接覆盖原文件。
去背后输出为 PNG（保留透明通道），路径后缀自动改为 .png。
"""

import os
import sys
import argparse
import io
from pathlib import Path
import requests
from PIL import Image

TARGET_W, TARGET_H = 1200, 630
RATIO = TARGET_W / TARGET_H
REMOVE_BG_URL = "https://api.remove.bg/v1.0/removebg"

# 项目根目录 = scripts/ 的上一级
_ROOT = Path(__file__).parent.parent


def load_env() -> None:
    """从项目根目录的 .env 文件加载环境变量（简单 KEY=VALUE 格式）。"""
    env_file = _ROOT / ".env"
    if not env_file.exists():
        return
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


load_env()


def remove_background(path: str, api_key: str) -> Image.Image:
    """调用 remove.bg API 去除背景，返回 PIL Image（RGBA）。"""
    print(f"  → 正在调用 remove.bg 去除背景...")
    with open(path, "rb") as f:
        response = requests.post(
            REMOVE_BG_URL,
            files={"image_file": f},
            data={"size": "auto"},
            headers={"X-Api-Key": api_key},
        )
    if response.status_code != requests.codes.ok:
        print(f"✗ remove.bg 错误 {response.status_code}: {response.text}")
        sys.exit(1)
    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
    print(f"  → 背景去除成功")
    return img


def crop_image(img: Image.Image) -> Image.Image:
    """居中裁切并缩放至 TARGET_W × TARGET_H。"""
    w, h = img.size
    cur_ratio = w / h

    if cur_ratio > RATIO:
        new_w = int(h * RATIO)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / RATIO)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    return img.resize((TARGET_W, TARGET_H), Image.LANCZOS)


def process(path: str, do_remove_bg: bool, api_key: str | None) -> None:
    if do_remove_bg:
        if not api_key:
            print("✗ 使用 --remove-bg 时需要提供 API Key（--api-key 或环境变量 REMOVE_BG_API_KEY）")
            sys.exit(1)
        img = remove_background(path, api_key)
        # 去背后输出为 PNG
        out_path = os.path.splitext(path)[0] + ".png"
    else:
        img = Image.open(path)
        out_path = path

    img = crop_image(img)

    save_kwargs = {"optimize": True}
    if out_path.lower().endswith(".png"):
        save_kwargs["format"] = "PNG"
    img.save(out_path, **save_kwargs)

    print(f"✓ {TARGET_W}×{TARGET_H}  →  {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="封面图处理：去背 + 裁切")
    parser.add_argument("images", nargs="+", metavar="图片路径")
    parser.add_argument(
        "--remove-bg",
        action="store_true",
        help="调用 remove.bg API 去除背景（需要 API Key）",
    )
    args = parser.parse_args()
    api_key = os.environ.get("REMOVE_BG_API_KEY")

    for path in args.images:
        print(f"处理: {path}")
        process(path, args.remove_bg, api_key)


if __name__ == "__main__":
    main()
