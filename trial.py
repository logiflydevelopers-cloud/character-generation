import streamlit as st
import os
import fal_client
from dotenv import load_dotenv
import tempfile

load_dotenv()

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
# STREAMLIT UI
# ===================================================

st.set_page_config(page_title="Character Editor", layout="centered")

st.title("🎨 AI Character Editor")

st.write("Upload a character image and modify it using a prompt")

uploaded_file = st.file_uploader("Upload Character Image", type=["png", "jpg", "jpeg", "webp"])

prompt = st.text_area(
    "Edit Prompt",
    placeholder="Example: same character wearing black leather jacket, cyberpunk city background, neon lighting"
)

generate = st.button("Generate Edited Character")


# ===================================================
# PROCESS
# ===================================================

if generate:

    if not uploaded_file:
        st.error("Please upload an image")
        st.stop()

    if not prompt:
        st.error("Please enter a prompt")
        st.stop()

    with st.spinner("Generating edited character..."):

        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded_file.read())
            image_path = tmp.name

        # Upload to fal storage
        uploaded = fal_client.upload_file(image_path)

        try:
            image_url = edit_character([uploaded], prompt)

            st.success("Character Edited Successfully!")

            st.image(image_url, caption="Edited Character", use_container_width=True)

            st.download_button(
                "Download Image",
                data=image_url,
                file_name="edited_character.webp"
            )

        except Exception as e:
            st.error(str(e))