import streamlit as st
import random

# UI Configuration
st.set_page_config(page_title="Tokenade Engine", layout="centered")
st.title("🐍 Tokenade Engine")

# Parameters
carrier = st.text_input("Carrier Emoji", "🐍")
payload_text = st.text_input("Custom Payload", "Insert text here...")
intensity = st.slider("Noise/Obfuscation Density", 100, 10000, 1000)

def generate_dense_payload(carrier_emoji, payload, size):
    # Unicode ranges for invisible noise/glitch effects
    noise_ranges = [
        range(0xFE00, 0xFE0F),  # Variation Selectors
        range(0x200B, 0x200D),  # ZWSP, ZWNJ, ZWJ
        range(0xE0000, 0xE007F) # Tag Blocks
    ]
    
    # We interleave the custom payload with the carrier and noise
    # The original logic fragments the payload with noise characters
    result = carrier_emoji
    
    # Split the custom payload into parts and inject noise between them
    payload_parts = list(payload)
    for part in payload_parts:
        result += part
        # Inject random noise after each character of your payload
        for _ in range(size // len(payload) if len(payload) > 0 else size):
            chosen_range = random.choice(noise_ranges)
            result += chr(random.choice(chosen_range))
            
    return result

if st.button("Generate Payload"):
    if not payload_text:
        st.warning("Please enter a payload.")
    else:
        output = generate_dense_payload(carrier, payload_text, intensity)
        
        # Display output
        st.code(output, language='text')
        
        # Meta-info
        st.write(f"Total Character Count: {len(output)}")
        st.success("Payload successfully obfuscated.")
