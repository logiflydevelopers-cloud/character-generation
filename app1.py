import streamlit as st
import requests
import zipfile
import io

from services.fal_client import charcter_generation, edit_character

st.set_page_config(page_title="AI Character Studio", layout="wide")

st.title("AI Character Generator")

# ==============================
# CHARACTER SETTINGS
# ==============================

st.subheader("Character Settings")

col1, col2 = st.columns(2)

with col1:

    style = st.selectbox(
        "Style",
        ["Realistic", "Anime"]
    )

    ethnicity = st.selectbox(
        "Ethnicity",
        ["Caucasian", "Asian", "Black / Afro", "Latina", "Arab", "American", "French", "Spanish", "Italian", "Turkish"]
    )

    age = st.slider("Age", 18, 35, 20)

    hair_style = st.selectbox(
        "Hair Style",
        ["Buzz Cut", "Long", "Slicked Back", "Short", "Bun", "Dreadlocks", "Curly", "Bald"]
    )

    hair_color = st.selectbox(
        "Hair Color",
        ["Brown", "Blonde", "Black", "Ginger", "Gray", "White", "Pink", "Silver"]
    )

with col2:

    eye_color = st.selectbox(
        "Eye Color",
        ["Brown", "Blue", "Green"]
    )

    body_type = st.selectbox(
        "Body Type",
        ["Slim", "Muscular", "Wide", "Lean"]
    )

# ==============================
# CLOTHING
# ==============================

st.subheader("Choose Clothing")

clothing_options = [
"Suit And Shirt","Jeans And T-Shirt","Chinos And Shirt","Bermuda And Polo",
"Pants And Sweater","Tracksuit","Blazer And T-Shirt","Leather Vest And Jeans",
"Hoodie And Cargo","Denim And Khakis","Cardigan And Shirt",
"Peacoat And Turtleneck","Vest And Long Sleeve","Shorts And Henley",
"Trench And Collared Shirt","Jacket And Chinos","Polo And Linen Pants",
"Shirt And Corduroy Pants","Henley And Shorts","Linen Shirt And Pants",
"Rugby Shirt And Joggers","Sweater And Jeans","Tee And Leather Pants",
"Turtleneck And Trousers","Vest And Sweatpants","Suit And Tie","Tuxedo",
"Basketball","Soccer","Tennis","Swim Shorts","Boxer Shorts",
"Martial Arts Black Belt","F1 Driver","Military","Firefighter","Police",
"Scientist","Cowboy","Builder","Biker","Pilot","Waiter","Barista","Chef",
"Business","Ninja","Knight","Ski","Superhero","Steampunk","Astronaut",
"Hip-Hop","Gothic","Pirate","Scottish","Prince","Monk","Prisoner",
"Tribal","Santa","Rugby","Golfer","Surfer","Lumberjack","Samurai"
]

clothing = st.multiselect(
    "Select Clothing Style",
    clothing_options
)

# ==============================
# PERSONALITY
# ==============================

st.subheader("Personality")

personality = st.multiselect(
    "Select Personality Traits",
    [
        "Protector", "Sage", "Hero", "Jester", "Toy Boy",
        "Dominant", "Submissive", "Lover", "Beast",
        "Confident", "Rebel", "Scholar"
    ]
)

# ==============================
# HOBBIES
# ==============================

Hobbies = st.selectbox(
    "Hobbies",
    [
        "Fitness", "Weightlifting", "Travelling", "Hiking", "Gaming", "Parties",
        "Series", "Anime", "Cosplay", "Self-Development", "Writing",
        "Camping", "Sailing", "Photography", "Volunteering", "Cars", "Art"
    ]
)

# ==============================
# RELATIONSHIP
# ==============================

Relationship = st.selectbox(
    "Relationship",
    [
        "Stranger", "Schoolmate", "Work Colleague", "Mentor",
        "Boyfriend", "Sex Friend", "Husband", "Lover",
        "Friend", "Best Friend", "Step Brother", "Step Father"
    ]
)

# ==============================
# OCCUPATION
# ==============================

occupation = st.selectbox(
    "Occupation",
    [
        "Massage Therapist","Dentist","Nutrionist","Personal Trainer","Pharmacist",
        "Barber","Gynecologist","Doctor","Librarian","Execcutive Assistant",
        "Interior designer","Fashion Designer","Architect","Chef","Product Designer",
        "Yoga Instructor","Flight Attendant","Martial Arts Instructor","Commercial Pilot",
        "Taxi Driver","Firefighter","Professor","Dancer","Detective","Soldier/Military Personnel",
        "Singer/Musician","Photographer","Artist","Scientst","Writer","Lawyer",
        "Construction Worker","Plumber","Mechanic","Truck Driver",
        "Software developer","Journalist"
    ]
)

# ==============================
# EDIT PROMPTS
# ==============================

st.subheader("Edit Prompts")

edit_prompt_1 = st.text_area("Edit Prompt 1")
edit_prompt_2 = st.text_area("Edit Prompt 2")

# ==============================
# PROMPT CREATION
# ==============================

personality_text = ", ".join(personality)
clothing_text = ", ".join(clothing)

generated_prompt = f"""
{style} handsome {ethnicity} man,
age {age},
{hair_color} {hair_style} hair,
{eye_color} eyes,
{body_type} body type,
wearing: {clothing_text},
personality: {personality_text},
hobbies: {Hobbies},
relationship: {Relationship},
occupation: {occupation},

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

    with st.spinner("Generating Base Image..."):
        image_url = charcter_generation(character_prompt)

    with st.spinner("Generating Edit Image 1..."):
        edited_url_1 = edit_character([image_url], edit_prompt_1)

    with st.spinner("Generating Edit Image 2..."):
        edited_url_2 = edit_character([edited_url_1], edit_prompt_2)

    # ==============================
    # DISPLAY RESULTS
    # ==============================

    st.divider()
    st.subheader("Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image_url, caption="Original Image")

    with col2:
        st.image(edited_url_1, caption="Edited Image 1")

    with col3:
        st.image(edited_url_2, caption="Edited Image 2")

    # ==============================
    # FETCH FILES
    # ==============================

    image_bytes = requests.get(image_url).content
    edit1_bytes = requests.get(edited_url_1).content
    edit2_bytes = requests.get(edited_url_2).content

    # ==============================
    # ZIP DOWNLOAD
    # ==============================

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("original.webp", image_bytes)
        zf.writestr("edit_1.webp", edit1_bytes)
        zf.writestr("edit_2.webp", edit2_bytes)

    st.download_button(
        "Download All Results (ZIP)",
        zip_buffer.getvalue(),
        "character_package.zip",
        "application/zip"
    )