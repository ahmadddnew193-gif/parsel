import streamlit as st
import random

# --- Logic Engine ---
def generate_tokenade(text, carrier="✨", spacing="ZWJ"):
    # Map separators to Unicode characters
    separators = {"ZWJ": "\u200D", "ZWNJ": "\u200C", "ZWSP": "\u200B", "None": ""}
    sep = separators.get(spacing, "")
    
    # Transform to Unicode Tags (U+E0000 block)
    payload = "".join([chr(0xE0000 + ord(c)) for c in text])
    return f"{carrier}{sep}{payload.replace('', sep)}"

# --- UI Interface ---
st.set_page_config(page_title="Tokenade Generator", layout="wide")
st.title("💥 Tokenade Generator")
st.write("Craft dense token payloads with emojis and zero-width characters")

# --- Presets (The "Feather" to "SuperDepth" logic) ---
presets = {"🪶 Feather": 1, "🍃 Light": 2, "🨨 Middle": 4, "🗿 Heavy": 8, "⚓ SuperDepth": 16}
selected_preset = st.select_slider("Presets", options=list(presets.keys()))

col1, col2 = st.columns(2)
with col1:
    nesting = st.number_input("Nesting levels", 1, 10, presets[selected_preset])
    breadth = st.slider("Breadth", 1, 10, 3)
with col2:
    repeats = st.slider("Repeats", 1, 5, 1)
    separator = st.selectbox("Separator", ["ZWJ", "ZWNJ", "ZWSP", "None"])

st.divider()

# --- Carrier Selection ---
carrier_opt = st.text_input("Custom carrier", placeholder="Overrides quick picks")
quick_picks = "🐍🐉🐲🔥💥🗿⚓⭐✨🚀💀🨨🍃🪶🔮🐢🐊🦎"
selected_emoji = st.selectbox("Quick picks", list(quick_picks))
final_carrier = carrier_opt if carrier_opt else selected_emoji

# --- Payload Generation ---
payload_input = st.text_input("Base text", "TOKENADE")

if st.button("Generate Tokenade"):
    result = generate_tokenade(payload_input, final_carrier, separator)
    st.code(result, language=None)
    st.success(f"Estimated length: {len(result)} chars")
