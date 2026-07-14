import streamlit as st
import base64
import random
import re
from collections import Counter
import string
import emoji

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Parseltongue", page_icon="🐍")

# Define all transformations
ALL_TRANSFORMS = {
    # Case transformations
    "Alternating Case": lambda t: ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(t)),
    "camelCase": lambda t: ''.join([t.split()[0].lower()] + [w.capitalize() for w in t.split()[1:]]),
    "Capitalize Words": lambda t: ' '.join(w.capitalize() for w in t.split()),
    "kebab-case": lambda t: '-'.join(w.lower() for w in t.split()),
    "Lowercase All": lambda t: t.lower(),
    "Random Case": lambda t: ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in t),
    "Sentence Case": lambda t: '. '.join(s.capitalize() for s in t.split('. ')),
    "snake_case": lambda t: '_'.join(w.lower() for w in t.split()),
    "Title Case": lambda t: t.title(),
    "Uppercase All": lambda t: t.upper(),
    "Toggle Case": lambda t: ''.join(c.upper() if c.islower() else c.lower() for c in t),
    
    # Ciphers
    "A1Z26": lambda t: '-'.join(str(ord(c)-ord('A')+1) if c.isalpha() else c for c in t.upper()),
    "Atbash Cipher": lambda t: ''.join(chr(ord('Z')-(ord(c)-ord('A'))) if c.isalpha() else c for c in t.upper()),
    "Caesar Cipher": lambda t, shift=3: ''.join(chr((ord(c)-ord('A')+shift)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
    "Vigenère Cipher": lambda t, key="SECRET": ''.join(chr((ord(c)-ord('A')+ord(k)-ord('A'))%26+ord('A')) if c.isalpha() else c for c,k in zip(t.upper(), (key*len(t))[:len(t)])),
    "Baconian Cipher": lambda t: ' '.join(bin(ord(c)-ord('A')).replace('0b','') if c.isalpha() else c for c in t.upper()),
    "Playfair Cipher": lambda t, key="SECRET": playfair_encrypt(t, key),
    "Rail Fence": lambda t, n=3: ''.join(''.join(t[i::n]) for i in range(n)),
    "Affine Cipher": lambda t, a=3, b=5: ''.join(chr((a*(ord(c)-ord('A'))+b)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
    "XOR Cipher": lambda t, key="KEY": ''.join(chr(ord(c)^ord(k)) for c,k in zip(t, (key*len(t))[:len(t)])),
    
    # Encoding
    "Base64": lambda t: base64.b64encode(t.encode()).decode(),
    "Base32": lambda t: base64.b32encode(t.encode()).decode(),
    "Hexadecimal": lambda t: t.encode().hex(),
    
    # Formatting
    "Remove Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
    "Remove Numbers": lambda t: re.sub(r'\d', '', t),
    "Reverse Text": lambda t: t[::-1],
    "Shuffle Characters": lambda t: ''.join(random.sample(t, len(t))),
    "Remove Spaces": lambda t: t.replace(' ', ''),
    "Mirror Text": lambda t: t[::-1],
    
    # Visual effects
    "Leetspeak": lambda t: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in t),
    "Mirror Text": lambda t: t[::-1],
    
    # Randomizer
    "Randomizer": lambda t: ' '.join(random.choice([
        lambda w: w.upper(),
        lambda w: w.lower(),
        lambda w: w[::-1],
        lambda w: ''.join(random.sample(w, len(w))),
        lambda w: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in w),
        lambda w: w[::-1]
    ])(w) for w in t.split()),
}

# Tokenade generator
def generate_tokenade(depth, breadth, repeats, variation_selectors, invisible_noise, separator, carrier):
    # Emoji carriers
    quick_picks = ['🐍', '🐉', '🐲', '🔥', '💥', '🗿', '⚓', '⭐', '✨', '🚀', '💀', '🪨', '🍃', '🪶', '🔮', '🐢', '🐊', '🦎']
    
    # Generate base payload
    payload = []
    for _ in range(repeats):
        # Create nested structure
        layer = carrier
        for _ in range(depth):
            children = []
            for _ in range(breadth):
                child = random.choice(quick_picks)
                if variation_selectors:
                    child += "\uFE0F"  # Variation selector
                if invisible_noise:
                    child += random.choice(["\u200B", "\u200C", "\u200D", "\uFEFF"])
                children.append(child)
            
            layer = separator.join(children)
        
        payload.append(layer)
    
    return separator.join(payload)

# Text payload generator
def generate_text_payload(base_text, repeat_count, combining_marks, zero_width_spacing):
    payload = []
    for _ in range(repeat_count):
        text = base_text
        
        # Add combining marks
        if combining_marks:
            text += "".join("\u0300-\u036F" for _ in range(len(text)))
        
        # Add zero-width spacing
        if zero_width_spacing:
            text = "\u200B".join(text)
        
        payload.append(text)
    
    return "\n".join(payload)

# Cipher helper functions
def playfair_encrypt(plaintext, key):
    # Simplified Playfair implementation
    alphabet = string.ascii_uppercase.replace('J', '')
    key_table = ''.join(dict.fromkeys(key.upper() + alphabet))
    
    # Create pairs
    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper())
    if len(plaintext) % 2 == 1:
        plaintext += 'X'
    
    pairs = [(plaintext[i:i+2]) for i in range(0, len(plaintext), 2)]
    
    # Encryption
    result = []
    for pair in pairs:
        if pair[0] == pair[1]:
            pair = pair[0] + 'X'
        
        pos1 = key_table.index(pair[0])
        pos2 = key_table.index(pair[1])
        row1, col1 = divmod(pos1, 5)
        row2, col2 = divmod(pos2, 5)
        
        if row1 == row2:
            result.append(key_table[row1*5 + (col1+1)%5])
            result.append(key_table[row2*5 + (col2+1)%5])
        elif col1 == col2:
            result.append(key_table[((row1+1)%5)*5 + col1])
            result.append(key_table[((row2+1)%5)*5 + col2])
        else:
            result.append(key_table[row1*5 + col2])
            result.append(key_table[row2*5 + col1])
    
    return ''.join(result)

# Main app
def main():
    st.title("🐍 Parseltongue: Complete Text Transformation Tool")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Transformer", "Tokenade Generator"])
    
    with tab1:
        # Sidebar
        st.sidebar.header("Categories")
        category = st.sidebar.radio(
            "Select category:",
            ["All", "Case", "Cipher", "Encoding", "Formatting", "Visual", "Randomizer"]
        )
        
        # Text input
        text = st.text_area("Enter your text:", height=200)
        
        # Filter transforms by category
        if category == "All":
            transforms = ALL_TRANSFORMS
        elif category == "Case":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Alternating Case", "camelCase", "Capitalize Words", "kebab-case",
                "Lowercase All", "Random Case", "Sentence Case", "snake_case",
                "Title Case", "Uppercase All", "Toggle Case"
            ]}
        elif category == "Cipher":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "A1Z26", "Atbash Cipher", "Caesar Cipher", "Vigenère Cipher",
                "Baconian Cipher", "Playfair Cipher", "Rail Fence", "Affine Cipher",
                "XOR Cipher"
            ]}
        elif category == "Encoding":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Base64", "Base32", "Hexadecimal"
            ]}
        elif category == "Formatting":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Remove Punctuation", "Remove Numbers", "Reverse Text",
                "Shuffle Characters", "Remove Spaces", "Mirror Text"
            ]}
        elif category == "Visual":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Leetspeak", "Mirror Text"
            ]}
        elif category == "Randomizer":
            transforms = {"Randomizer": ALL_TRANSFORMS["Randomizer"]}
        
        # Select transformation
        transform_name = st.selectbox("Select transformation:", sorted(transforms.keys()))
        
        # Special parameters
        params = {}
        if "Caesar Cipher" in transform_name:
            params["shift"] = st.slider("Shift value:", min_value=1, max_value=25, value=3)
        elif "Vigenère Cipher" in transform_name:
            params["key"] = st.text_input("Key:", "SECRET")
        elif "Playfair Cipher" in transform_name:
            params["key"] = st.text_input("Key:", "SECRET")
        elif "Rail Fence" in transform_name:
            params["n"] = st.slider("Rails:", min_value=2, max_value=10, value=3)
        elif "Affine Cipher" in transform_name:
            params["a"] = st.slider("a:", min_value=1, max_value=25, value=3)
            params["b"] = st.slider("b:", min_value=0, max_value=25, value=5)
        elif "XOR Cipher" in transform_name:
            params["key"] = st.text_input("Key:", "KEY")
        
        # Apply transformation
        if st.button("Transform"):
            try:
                if transform_name == "Randomizer":
                    result = transforms[transform_name](text)
                elif "Caesar Cipher" in transform_name:
                    result = transforms[transform_name](text, params["shift"])
                elif "Vigenère Cipher" in transform_name:
                    result = transforms[transform_name](text, params["key"])
                elif "Playfair Cipher" in transform_name:
                    result = transforms[transform_name](text, params["key"])
                elif "Rail Fence" in transform_name:
                    result = transforms[transform_name](text, params["n"])
                elif "Affine Cipher" in transform_name:
                    result = transforms[transform_name](text, params["a"], params["b"])
                elif "XOR Cipher" in transform_name:
                    result = transforms[transform_name](text, params["key"])
                else:
                    result = transforms[transform_name](text)
                
                st.code(result)
                st.session_state.history.append(f"{transform_name}: {result}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # History
        if st.session_state.history:
            st.sidebar.subheader("Transformation History")
            for item in st.session_state.history[-5:]:  # Show last 5 items
                st.sidebar.write(item)
    
    with tab2:
        st.markdown("💥 Tokenade Generator")
        st.markdown("Craft dense token payloads with emojis and zero-width characters")
        st.markdown("DISCLAIMER: Tokenade payloads can severely degrade model performance and crash UIs. Use for testing only. Do not deploy to production or target systems without explicit permission.")
        
        # Tokenade settings
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🪶 Feather")
            st.markdown("🍃 Light")
            st.markdown("🪨 Middle")
            st.markdown("🗿 Heavy")
            st.markdown("⚓ Super")
            
            depth = st.slider("Depth", min_value=1, max_value=10, value=3)
            breadth = st.slider("Breadth", min_value=1, max_value=20, value=4)
            repeats = st.slider("Repeats", min_value=1, max_value=100, value=5)
            variation_selectors = st.checkbox("Variation selectors")
            invisible_noise = st.checkbox("Invisible noise")
            
            separator_options = ["ZWJ", "ZWNJ", "ZWSP", "None"]
            separator = st.radio("Separator", separator_options, index=0)
            separator = {
                "ZWJ": "\u200D",
                "ZWNJ": "\u200C",
                "ZWSP": "\u200B",
                "None": ""
            }[separator]
        
        with col2:
            st.markdown("Estimated length: 2,882 chars")
            
            # Quick picks
            quick_picks = ['🐍', '🐉', '🐲', '🔥', '💥', '🗿', '⚓', '⭐', '✨', '🚀', '💀', '🪨', '🍃', '🪶', '🔮', '🐢', '🐊', '🦎']
            carrier = st.selectbox("Single emoji carrier", quick_picks)
            
            # Custom carrier
            custom_carrier = st.text_input("Custom carrier", value="", placeholder="Overrides quick picks")
            if custom_carrier:
                carrier = custom_carrier
            
            # Generate button
            if st.button("Generate Tokenade"):
                result = generate_tokenade(depth, breadth, repeats, variation_selectors, invisible_noise, separator, carrier)
                st.code(result)
                st.session_state.history.append(f"Tokenade: {len(result)} chars")
        
        # Text Payload Generator
        st.markdown("---")
        st.markdown("Text Payload Generator")
        base_text = st.text_input("Base text", value="hello", placeholder="Enter base snippet (e.g., hello)")
        repeat_count = st.slider("Repeat count", min_value=1, max_value=1000, value=100)
        combining_marks = st.checkbox("Combining marks")
        zero_width_spacing = st.checkbox("Zero-width spacing")
        
        if st.button("Generate Text Payload"):
            result = generate_text_payload(base_text, repeat_count, combining_marks, zero_width_spacing)
            st.code(result)
            st.session_state.history.append(f"Text Payload: {len(result)} chars")

if __name__ == "__main__":
    main()
