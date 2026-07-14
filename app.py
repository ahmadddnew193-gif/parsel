import streamlit as st
import random

# UI Configuration
st.set_page_config(page_title="Tokenade Engine", layout="centered")
st.title("🐍 Tokenade Engine")

# Parameters
carrier = st.text_input("Carrier Emoji", "🐍")
intensity = st.slider("Payload Density", 100, 5000, 1000)

# The logic that mimics the "glitch" functionality
def generate_dense_payload(carrier_emoji, size):
    # These are the unicode ranges used for "invisible" noise and variation
    # Variation Selectors: U+FE00-U+FE0F
    # Invisible Formatting: U+200B-U+200D
    # Tag Blocks (used in dense payloads): U+E0000-U+E007F
    noise_ranges = [
        range(0xFE00, 0xFE0F), 
        range(0x200B, 0x200D),
        range(0xE0000, 0xE007F)
    ]
    
    payload = carrier_emoji
    
    for _ in range(size):
        # Pick a random range, then a random character from that range
        chosen_range = random.choice(noise_ranges)
        char = chr(random.choice(chosen_range))
        payload += char
        
    return payload

if st.button("Generate Payload"):
    output = generate_dense_payload(carrier, intensity)
    
    # Display the output in a code block so it doesn't break the UI
    st.code(output, language='text')
    
    # Display meta-info
    st.write(f"Payload Character Count: {len(output)}")
    st.success("Payload generated. You can now copy this for testing.")
