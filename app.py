import streamlit as st
import base64
import random
import re
from collections import Counter

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Parseltongue", page_icon="🐍")

# Cipher implementations
def a1z26_cipher(text):
    return '-'.join(str(ord(c)-ord('A')+1) if c.isalpha() else c for c in text.upper())

def atbash_cipher(text):
    return ''.join(chr(ord('Z')-(ord(c)-ord('A'))) if c.isalpha() else c for c in text.upper())

def caesar_cipher(text, shift=3):
    return ''.join(chr((ord(c)-ord('A')+shift)%26+ord('A')) if c.isalpha() else c for c in text.upper())

def vigenere_cipher(text, key="SECRET"):
    return ''.join(chr((ord(c)-ord('A')+ord(k)-ord('A'))%26+ord('A')) if c.isalpha() else c 
                  for c,k in zip(text.upper(), (key*len(text))[:len(text)]))

def baconian_cipher(text):
    binary_map = {'A':'00000', 'B':'00001', 'C':'00010', 'D':'00011', 'E':'00100',
                  'F':'00101', 'G':'00110', 'H':'00111', 'I':'01000', 'J':'01001',
                  'K':'01010', 'L':'01011', 'M':'01100', 'N':'01101', 'O':'01110',
                  'P':'01111', 'Q':'10000', 'R':'10001', 'S':'10010', 'T':'10011',
                  'U':'10100', 'V':'10101', 'W':'10110', 'X':'10111', 'Y':'11000',
                  'Z':'11001'}
    return ' '.join(binary_map[c] if c.isalpha() else c for c in text.upper())

def playfair_cipher(text, key="SECRET"):
    # Simplified Playfair implementation
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key_table = ''.join(dict.fromkeys(key.upper() + alphabet))
    
    pairs = []
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i].upper() != text[i+1].upper():
            pairs.append((text[i], text[i+1]))
            i += 2
        else:
            pairs.append((text[i], 'X'))
            i += 1
    
    result = []
    for p1, p2 in pairs:
        if p1.isalpha() and p2.isalpha():
            idx1 = key_table.index(p1.upper())
            idx2 = key_table.index(p2.upper())
            row1, col1 = idx1 // 5, idx1 % 5
            row2, col2 = idx2 // 5, idx2 % 5
            
            if row1 == row2:
                result.append(key_table[row1*5 + (col1+1)%5])
                result.append(key_table[row2*5 + (col2+1)%5])
            elif col1 == col2:
                result.append(key_table[((row1+1)%5)*5 + col1])
                result.append(key_table[((row2+1)%5)*5 + col2])
            else:
                result.append(key_table[row1*5 + col2])
                result.append(key_table[row2*5 + col1])
        else:
            result.append(p1+p2)
    
    return ''.join(result)

def rail_fence_cipher(text, n_rails=3):
    fence = [[] for _ in range(n_rails)]
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        if rail == 0:
            direction = 1
        elif rail == n_rails - 1:
            direction = -1
        rail += direction
    
    result = []
    for row in fence:
        result.extend(row)
    return ''.join(result)

def affine_cipher(text, a=3, b=5):
    m = 26
    a_inv = pow(a, -1, m)
    return ''.join(chr((a_inv*(ord(c)-ord('A')-b))%m+ord('A')) if c.isalpha() else c 
                  for c in text.upper())

def xor_cipher(text, key="KEY"):
    key = (key * len(text))[:len(text)]
    return ''.join(chr(ord(c) ^ ord(k)) for c,k in zip(text, key))

# Main app
def main():
    st.title("🐍 Parseltongue: Complete Text Transformation Tool")
    
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
        transforms = {
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
            "A1Z26": a1z26_cipher,
            "Atbash Cipher": atbash_cipher,
            "Caesar Cipher": caesar_cipher,
            "Vigenère Cipher": vigenere_cipher,
            "Baconian Cipher": baconian_cipher,
            "Playfair Cipher": playfair_cipher,
            "Rail Fence": rail_fence_cipher,
            "Affine Cipher": affine_cipher,
            "XOR Cipher": xor_cipher,
            
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
    elif category == "Case":
        transforms = {
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
        }
    elif category == "Cipher":
        transforms = {
            "A1Z26": a1z26_cipher,
            "Atbash Cipher": atbash_cipher,
            "Caesar Cipher": caesar_cipher,
            "Vigenère Cipher": vigenere_cipher,
            "Baconian Cipher": baconian_cipher,
            "Playfair Cipher": playfair_cipher,
            "Rail Fence": rail_fence_cipher,
            "Affine Cipher": affine_cipher,
            "XOR Cipher": xor_cipher,
        }
    elif category == "Encoding":
        transforms = {
            "Base64": lambda t: base64.b64encode(t.encode()).decode(),
            "Base32": lambda t: base64.b32encode(t.encode()).decode(),
            "Hexadecimal": lambda t: t.encode().hex(),
        }
    elif category == "Formatting":
        transforms = {
            "Remove Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
            "Remove Numbers": lambda t: re.sub(r'\d', '', t),
            "Reverse Text": lambda t: t[::-1],
            "Shuffle Characters": lambda t: ''.join(random.sample(t, len(t))),
            "Remove Spaces": lambda t: t.replace(' ', ''),
            "Mirror Text": lambda t: t[::-1],
        }
    elif category == "Visual":
        transforms = {
            "Leetspeak": lambda t: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in t),
            "Mirror Text": lambda t: t[::-1],
        }
    elif category == "Randomizer":
        transforms = {"Randomizer": lambda t: ' '.join(random.choice([
            lambda w: w.upper(),
            lambda w: w.lower(),
            lambda w: w[::-1],
            lambda w: ''.join(random.sample(w, len(w))),
            lambda w: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in w),
            lambda w: w[::-1]
        ])(w) for w in t.split())}
    
    # Select transformation
    transform_name = st.selectbox("Select transformation:", sorted(transforms.keys()))
    
    # Special parameters
    params = {}
    if "Caesar Cipher" in transform_name:
        params["shift"] = st.slider("Shift value:", min_value=1, max_value=25, value=3)
    elif "Vigenère Cipher" in transform_name:
        params["key"] = st.text_input("Key:", "SECRET")
    elif "Rail Fence" in transform_name:
        params["n_rails"] = st.slider("Rails:", min_value=2, max_value=10, value=3)
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
            elif "Rail Fence" in transform_name:
                result = transforms[transform_name](text, params["n_rails"])
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

if __name__ == "__main__":
    main()
