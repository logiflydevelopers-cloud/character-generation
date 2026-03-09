import os
import fal_client
from dotenv import load_dotenv

load_dotenv()

# ===================================================
# Character Generation
# ===================================================

GENERATION_MODEL = "fal-ai/qwen-image-2512"

def charcter_generation(prompt: str):

    if not os.getenv("FAL_KEY"):
        raise EnvironmentError("FAL_KEY not found in environment")
    
    arguments = {
        "prompt": prompt,
        "image_size": {
            "width": 832,
            "height": 1232
        },
        "num_inference_steps": 28,
        "guidance_scale": 4,
        "num_images": 1,
        "enable_safety_checker": False,
        "output_format": "webp",
        "acceleration": "regular"
    }

    try:
        result = fal_client.subscribe(
            GENERATION_MODEL,
            arguments=arguments
        )

        image = result.get("images")
        if not image:
            raise RuntimeError(f"No image returned from fal.ai: {result}")

        return image[0]["url"]

    except Exception as e:
        raise RuntimeError(f"qwen-image-2512 failed: {e}")
    

# ===================================================
# Character Edit
# ===================================================

EDIT_MODEL = "fal-ai/qwen-image-2/pro/edit"

def edit_character(image_url: list[str], prompt: str):

    if not os.getenv("FAL_KEY"):
        raise EnvironmentError("FAL_KEY not found in environment")
    
    arguments = {
        "prompt": prompt,
        "negative_prompt": "low resolution, error, worst quality, low quality, deformed",
        "enable_prompt_expansion": True,
        "enable_safety_checker": False,
        "num_images": 1,
        "output_format": "webp",
        "image_urls": image_url,
        "image_size": {
            "width": 832,
            "height": 1232
        }
        }
    
    try:
        result = fal_client.subscribe(
            EDIT_MODEL,
            arguments=arguments
        )

        image = result.get("images")
        if not image:
            raise RuntimeError(f"No image returned from fal.ai: {result}")

        return image[0]["url"]

    except Exception as e:
        raise RuntimeError(f"qwen-image-Edit failed: {e}")
    
# ===================================================
# Character Video Generation
# ===================================================

VIDEO_MODEL = "fal-ai/wan/v2.2-a14b/image-to-video/lora"

def generate_video(image_url: str, prompt: str):
    
    if not os.getenv("FAL_KEY"):
        raise EnvironmentError("FAL_KEY not found in environment")
    
    arguments = {
        "prompt": prompt,
        "negative_prompt": "bright colors, overexposed, static, blurred details, subtitles, style, artwork, painting, picture, still, overall gray, worst quality, low quality, JPEG compression residue, ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn faces, deformed, disfigured, malformed limbs, fused fingers, still picture, cluttered background, three legs, many people in the background, walking backwards",
        "image_url": image_url,
        "num_frames": 81,
        "frames_per_second": 16,
        "resolution": "720p",
        "num_inference_steps": 30,
        "guide_scale": 5,
        "shift": 5,
        "enable_safety_checker": False,
        "enable_prompt_expansion": False,
        "acceleration": "regular",
        "aspect_ratio": "auto"
        }
    
    try:
        result = fal_client.subscribe(
            VIDEO_MODEL,
            arguments=arguments
        )

        video = result.get("video")
        if not video:
            raise RuntimeError(f"No image returned from fal.ai: {result}")

        return video["url"]

    except Exception as e:
        raise RuntimeError(f"wan-v2.2 failed: {e}")
    
