import time
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
import replicate

# =========================================================
# INTERNAL UTILITIES
# =========================================================

def _check_replicate_key():
    if not os.getenv("REPLICATE_API_TOKEN"):
        raise EnvironmentError("REPLICATE_API_TOKEN not found in environment")


def _extract_url(output):
    if isinstance(output, list) and len(output) > 0:
        item = output[0]
        return item.url if hasattr(item, "url") else item
    if hasattr(output, "url"):
        return output.url
    return output

# =========================================================
# ANIME CHARACTER GENERATION
# =========================================================

ANIME_GENERATION_MODEL = "aisha-ai-official/wai-nsfw-illustrious-v12:0fc0fa9885b284901a6f9c0b4d67701fd7647d157b88371427d63f8089ce140e"

def anime_generation(prompt: str):

    _check_replicate_key()

    if not prompt:
        raise ValueError("Prompt is Required")
    
    output = replicate.run(
        ANIME_GENERATION_MODEL,
        input={
            "vae": "default",
            "seed": -1,
            "model": "WAI-NSFW-Illustrious-SDXL-v12",
            "steps": 30,
            "width": 832,
            "height": 1232,
            "prompt": prompt,
            "cfg_scale": 7,
            "clip_skip": 2,
            "pag_scale": 0,
            "scheduler": "Euler a",
            "batch_size": 1,
            "negative_prompt": "blurry, low quality, extra limbs, extra fingers, distorted face, bad anatomy, watermark, text, logo, cropped, duplicate body parts",
            "guidance_rescale": 1,
            "prepend_preprompt": True
        }
    )

    # Handle FileOutput correctly
    if isinstance(output, list):
        first = output[0]
        return first.url if hasattr(first, "url") else first

    # Single FileOutput
    if hasattr(output, "url"):
        return output.url

    return output

ANIME_EDIT_MODEL = "lucataco/omnigen2:5b9ea1d0821a60be9c861ebfc3513d121ecd8cab1932d3aa8d703e517988502e"

def edit_anime(image_url: str, prompt: str):

    _check_replicate_key()

    output = replicate.run(
        ANIME_EDIT_MODEL,
        input = {
            "cfg_range_end": 1,
            "cfg_range_start": 0,
            "height": 1024,
            "image": image_url,
            "image_guidance_scale": 2,
            "max_input_image_side_length": 2048,
            "max_pixels": 1048576,
            "negative_prompt": "(((deformed))), blurry, over saturation, bad anatomy, disfigured, poorly drawn face, mutation, mutated, (extra_limb), (ugly), (poorly drawn hands), fused fingers, messy drawing, broken legs censor, censored, censor_bar",
            "num_inference_steps": 50,
            "prompt": prompt,
            "scheduler": "euler",
            "seed": -1,
            "text_guidance_scale": 5,
            "width": 832
            }
    )

    # Handle FileOutput correctly
    if isinstance(output, list):
        first = output[0]
        return first.url if hasattr(first, "url") else first

    # Single FileOutput
    if hasattr(output, "url"):
        return output.url

    return output

ANIME_VIDEO_MODEL = "minimax/video-01-live"

def anime_video(image_url: str, prompt: str):

    _check_replicate_key()

    output = replicate.run(
        ANIME_VIDEO_MODEL,
        input = {
            "prompt": prompt,
            "prompt_optimizer": True,
            "first_frame_image": image_url
        }
    )

    # Normalize output → URL
    if isinstance(output, list) and len(output) > 0:
         item = output[0]
         video_url = item.url if hasattr(item, "url") else item
    elif hasattr(output, "url"):
         video_url = output.url
    else:
         raise RuntimeError(f"Unexpected output: {output}")

    return video_url
