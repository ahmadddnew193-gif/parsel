import streamlit as st
import random

def get_noise():
    # Full set of non-rendering control characters
    return ["\u2062", "\u2063", "\u200D", "\u200B", "\u200E", "\u2060", "\u202A", "\u202B", "\uFEFF"]

def generate_pro_tokenade(text, carrier, density=5):
    noise_pool = get_noise()
    encoded = carrier
    
    # Generate the main payload with high-density noise injection
    for char in text:
        # Inject multiple noise characters to increase entropy
        padding = "".join(random.choices(noise_pool, k=density))
        encoded += padding + chr(0xE0000 + ord(char)) + padding
        
    # Add random "Entropy Blocks" at the end to simulate the 700+ char length
    for _ in range(50):
        encoded += random.choice(noise_pool)
        
    return encoded

# --- UI Integration ---
st.subheader("Advanced Payload Generator")
density = st.slider("Density Multiplier (Length)", 1, 15, 5)

if st.button("Generate Dense Tokenade"):
    result = generate_pro_tokenade(payload_input, final_carrier, density)
    st.code(result, language=None)
    st.write(f"Final Payload Size: {len(result)} characters")
