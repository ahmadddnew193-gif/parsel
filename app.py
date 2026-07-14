import streamlit as st
import random

# --- Page Config ---
st.set_page_config(page_title="Tokenade Generator", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { width: 100%; border-radius: 4px; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# --- Logic Engine ---
def get_noise():
    return ["\u2062", "\u2063", "\u200D", "\u200B", "\u200E", "\u2060", "\u202A", "\u202B", "\uFEFF"]

def generate_pro_tokenade(text, carrier, density=5):
    noise_pool = get_noise()
    encoded = carrier
    for char in text:
        padding = "".join(random.choices(noise_pool, k=density))
        encoded += padding + chr(0xE0000 + ord(char)) + padding
    for _ in range(50):
        encoded += random.choice(noise_pool)
    return encoded

# --- Sidebar Layout ---
with st.sidebar:
    st.header("💥 Tokenade")
    st.caption("Advanced Payload Generator")
    
    preset = st.radio("Presets", ["🪶 Feather", "🍃 Light", "🪨 Middle", "🗿 Heavy", "⚓ SuperDepth"])
    
    # Preset Intensity Mapping
    intensity = {"🪶 Feather": 1, "🍃 Light": 3, "🪨 Middle": 5, "🗿 Heavy": 8, "⚓ SuperDepth": 15}
    
    st.divider()
    
    st.subheader("Fine-tuning")
    density = st.slider("Density Multiplier", 1, 15, intensity[preset])
    separator = st.selectbox("Separator", ["ZWJ", "ZWNJ", "ZWSP", "None"])
    
    st.divider()
    st.info("Ensure the target environment handles Unicode Tag characters.")

# --- Main Layout ---
header_col, disclaimer_col = st.columns([3, 1])
with header_col:
    st.title("Tokenade Generator")
with disclaimer_col:
    with st.expander("⚠️ Disclaimer"):
        st.write("For testing only. Do not deploy to production or unauthorized systems.")

# --- Input Area ---
payload_input = st.text_input("Base text:", "TOKENADE")
carrier_input = st.text_input("Carrier emoji:", "🐍")

# --- Transformation Logic (Defined as functions) ---
transformations = {
    "Uppercase": lambda t: t.upper(),
    "Lowercase": lambda t: t.lower(),
    "None": lambda t: t
}

selected_op = st.selectbox("Text Transformation", list(transformations.keys()))

# --- Action ---
if st.button("Generate Tokenade"):
    processed_text = transformations[selected_op](payload_input)
    result = generate_pro_tokenade(processed_text, carrier_input, density)
    
    st.code(result, language=None)
    st.success(f"Payload generated. Length: {len(result)} chars")
    
    if st.button("Copy to clipboard"):
        st.write("Use Ctrl+C to copy the code block above.")
