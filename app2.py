import streamlit as st
import requests
import zipfile
import io
import os
import replicate

replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

from services.replicate_client import anime_generation, edit_anime, anime_video

st.set_page_config(page_title="AI Character Studio", layout="wide")

st.title("AI Character Generator")

# ==============================
# CHARACTER SETTINGS
# ==============================

st.subheader("Character Settings")

col1, col2 = st.columns(2)

with col1:

    style = st.selectbox("Style", ["Realistic", "Anime"])

    ethnicity = st.selectbox(
        "Ethnicity",
        ["Caucasian", "Asian", "Latina"]
    )

    age = st.slider("Age", 18, 39, 25)

    hair_style = st.selectbox(
        "Hair Style",
        ["Straight", "Bangs", "Curly", "Bun", "Short", "Ponytail"]
    )

    hair_color = st.selectbox(
        "Hair Color",
        ["Brunette", "Blonde", "Black", "Redhead", "Pink", "Purple",
         "Blue", "White", "Green", "Yellow", "Multicolor"]
    )

with col2:

    eye_color = st.selectbox(
        "Eye Color",
        ["Brown", "Blue", "Green", "Red", "Yellow"]
    )

    body_type = st.selectbox(
        "Body Type",
        ["Skinny", "Athletic", "Average", "Curvy"]
    )

    b_size = st.selectbox(
        "Bust Size",
        ["Small", "Medium", "Large", "Extra Large"]
    )

# ==============================
# PERSONALITY
# ==============================

st.subheader("Personality")

personality = st.multiselect(
    "Select Personality Traits",
    [
        "Nympho","Lover","Submissive","Dominant","Temptress",
        "Innocent","Caregiver","Experimenter","Mean",
        "Confident","Shy","Queen","BDSM"
    ]
)

# ==============================
# RELATIONSHIP
# ==============================

relationship = st.selectbox(
    "Relationship",
    [
        "Stranger","Girlfriend","Sex Friend","School Mate",
        "Work Colleague","Wife","Mistress","Friend",
        "Step Sister","Step Mom","Step daughter","Landlord",
        "Sugar Baby","Boss","Teacher","Student","Neighbour",
        "Mother-in-law","Sister-in-law"
    ]
)

# ==============================
# OCCUPATION
# ==============================

occupation = st.selectbox(
    "Occupation",
    [
        "Student","Dancer","Model","Stripper","Maid",
        "Cam Girl","Boss / CEO","Babysitter / Au Pair",
        "Pornstar","Streamer","Bartender","Tech Engineer",
        "Lifeguard","Cashier","Massage Therapist",
        "Teacher","Nurse","Secretary","Yoga Instructor",
        "Cook","Artist","Movie star/ Actress","Doctor","Libraian",
        "Spy","Police Officer","Solider","Lawyer","Hairdresser",
        "Dentist","Musician/Singer","Gynecologist","Writer",
        "Flight Attendent","Professional Athlete","Scientist",
        "Florist","Makeup Artist","Photographer","Social Worker",
        "Pharmacist","Designer","Nutritionalist"
    ]
)

# ==============================
# KINKS
# ==============================

kinks = st.selectbox(
    "Kinks",
    [
        "Daddy Dominance","Bondage","Spanking","Collar and Leash",
        "Punishment","Humiliation","Public Play","Role Play",
        "Anal Play","Oral Play","Cum Play","Creampie",
        "Squirting","Dirty Talk","Breeding","Edging",
        "Obidenece","Control","Inexperienced","Shy Flirting",
        "Playful Teasing","Cuddling","Slow and Sensual","Hair Pulling"
    ]
)

# ==============================
# EDIT PROMPTS
# ==============================

st.subheader("Edit Prompts")

edit_prompt_1 = st.text_area("Edit Prompt 1")
edit_prompt_2 = st.text_area("Edit Prompt 2")

# ==============================
# VIDEO PROMPTS
# ==============================

st.subheader("Video Prompts")

video_prompt_1 = st.text_area("Video Prompt 1")
video_prompt_2 = st.text_area("Video Prompt 2")

# ==============================
# PROMPT CREATION
# ==============================

personality_text = ", ".join(personality)

generated_prompt = f"""
{style} beautiful {ethnicity} woman,
age {age},
{hair_color} {hair_style} hair,
{eye_color} eyes,
{body_type} body type,
bust size {b_size},
personality: {personality_text},
relationship: {relationship},
occupation: {occupation},
kinks: {kinks}
"""

character_prompt = st.text_area(
    "Generated Prompt (Editable)",
    value=generated_prompt,
    height=200
)

# ==============================
# GENERATE
# ==============================

if st.button("Generate Character"):

    try:

        # BASE IMAGE
        with st.spinner("Generating Base Image..."):
            image_url = anime_generation(character_prompt)

        edited_url_1 = None
        edited_url_2 = None

        # EDIT 1
        if edit_prompt_1.strip():
            with st.spinner("Generating Edit Image 1..."):
                edited_url_1 = edit_anime(image_url, edit_prompt_1)

        # EDIT 2
        if edit_prompt_2.strip() and edited_url_1:
            with st.spinner("Generating Edit Image 2..."):
                edited_url_2 = edit_anime(edited_url_1, edit_prompt_2)

        video_url_1 = None
        video_url_2 = None

        # VIDEO 1
        if video_prompt_1.strip():
            with st.spinner("Generating Video 1..."):
                video_url_1 = anime_video(image_url, video_prompt_1)

        # VIDEO 2
        if video_prompt_2.strip() and edited_url_1:
            with st.spinner("Generating Video 2..."):
                video_url_2 = anime_video(edited_url_1, video_prompt_2)

        # ==============================
        # DISPLAY
        # ==============================

        st.divider()
        st.subheader("Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(image_url, caption="Original Image")

        if edited_url_1:
            with col2:
                st.image(edited_url_1, caption="Edited Image 1")

        if edited_url_2:
            with col3:
                st.image(edited_url_2, caption="Edited Image 2")

        st.divider()

        col4, col5 = st.columns(2)

        if video_url_1:
            with col4:
                st.video(video_url_1)

        if video_url_2:
            with col5:
                st.video(video_url_2)

        # ==============================
        # DOWNLOAD ZIP
        # ==============================

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:

            image_bytes = requests.get(image_url).content
            zf.writestr("original.webp", image_bytes)

            if edited_url_1:
                edit1_bytes = requests.get(edited_url_1).content
                zf.writestr("edit_1.webp", edit1_bytes)

            if edited_url_2:
                edit2_bytes = requests.get(edited_url_2).content
                zf.writestr("edit_2.webp", edit2_bytes)

            if video_url_1:
                video1_bytes = requests.get(video_url_1).content
                zf.writestr("video_1.mp4", video1_bytes)

            if video_url_2:
                video2_bytes = requests.get(video_url_2).content
                zf.writestr("video_2.mp4", video2_bytes)

        st.download_button(
            "Download All Results (ZIP)",
            zip_buffer.getvalue(),
            "character_package.zip",
            "application/zip"
        )

    except Exception as e:
        st.error(f"Error: {e}")
        