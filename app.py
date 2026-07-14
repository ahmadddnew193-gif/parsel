import streamlit as st
import random

# Emojis for the quick pick list
EMOJI_LIST = "🐍🐉🐲🔥💥🗿⚓⭐✨🚀💀🪨🍃🪶🔮🐢🐊🦎"

def generate_tokenade(base, nest_levels, breadth, repeats, separator, use_noise):
    noise_chars = ["\uFE0E", "\uFE0F", "\u200B", "\u200C", "\u200D"]
    
    # Logic to build nested structures
    def build_nest(content, level):
        if level <= 0:
            return content
        nested = [build_nest(content, level - 1) for _ in range(breadth)]
        return separator.join(nested)

    # Core generation
    payload = build_nest(base, nest_levels)
    payload = (payload + separator) * repeats
    
    # Injecting noise
    if use_noise:
        payload = "".join([c + random.choice(noise_chars) for c in payload])
        
    return payload

st.title("💥 Tokenade Generator")
st.warning("DISCLAIMER: Tokenade payloads can degrade model performance. Use for testing only.")

# Sidebar Controls
nest_levels = st.slider("Nesting levels", 1, 5, 2)
breadth = st.slider("Breadth (Items per level)", 1, 10, 3)
repeats = st.slider("Repeats (Block count)", 1, 10, 3)

col1, col2 = st.columns(2)
with col1:
    separator = st.selectbox("Separator", ["ZWJ", "ZWNJ", "ZWSP", "None"])
    sep_map = {"ZWJ": "\u200D", "ZWNJ": "\u200C", "ZWSP": "\u200B", "None": ""}
    final_sep = sep_map[separator]

with col2:
    carrier = st.selectbox("Carrier", list(EMOJI_LIST))
    use_noise = st.checkbox("Invisible noise", True)

if st.button("Generate Tokenade"):
    result = generate_tokenade(carrier, nest_levels, breadth, repeats, final_sep, use_noise)
    st.code(result, language=None)
    st.info(f"Estimated length: {len(result)} chars")
