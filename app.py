import streamlit as st

# Unicode mapping for invisible characters
UNICODE_MAP = {
    "ZWJ": "\u200D",   # Zero Width Joiner
    "ZWNJ": "\u200C",  # Zero Width Non-Joiner
    "ZWSP": "\u200B",  # Zero Width Space
    "None": ""
}

def generate_payload(depth, breadth, repeats, separator_key, use_noise):
    sep = UNICODE_MAP.get(separator_key, "")
    
    # Building the payload
    # Original logic: {depth} nesting * breadth * repeats
    base_unit = "{" * depth + "TOKEN" * breadth + "}" * depth
    
    noise = "\u200B" if use_noise else ""
    
    # Construct the final string
    full_payload = (base_unit + noise + sep).join([""] * repeats)
    return full_payload

# Streamlit UI
st.title("Tokenade Python Implementation")

# Sliders to match the original UI
depth = st.slider("Depth", 1, 10, 3)
breadth = st.slider("Breadth", 1, 10, 4)
repeats = st.slider("Repeats", 1, 100, 6)

# Selectors
use_noise = st.checkbox("Invisible noise")
separator = st.radio("Separator", ["ZWJ", "ZWNJ", "ZWSP", "None"], horizontal=True)

if st.button("Generate Tokenade"):
    payload = generate_payload(depth, breadth, repeats, separator, use_noise)
    st.text_area("Generated Payload", payload, height=200)
    st.info(f"Length: {len(payload)} characters")
