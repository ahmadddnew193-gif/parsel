import streamlit as st
import base64
import random
import re
from collections import Counter

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Parseltongue", page_icon="🐍")

# Define transformation functions
def alternating_case(text):
    return ''.join(char.upper() if i % 2 == 0 else char.lower() 
                  for i, char in enumerate(text))

def camel_case(text):
    words = text.split()
    return ''.join([words[0].lower()] + [word.capitalize() for word in words[1:]])

def capitalize_words(text):
    return ' '.join(word.capitalize() for word in text.split())

def kebab_case(text):
    return '-'.join(word.lower() for word in text.split())

def lowercase_all(text):
    return text.lower()

def random_case(text):
    return ''.join(char.upper() if random.choice([True, False]) else char.lower() 
                  for char in text)

def sentence_case(text):
    return '. '.join(sentence.capitalize() for sentence in text.split('. '))

def snake_case(text):
    return '_'.join(word.lower() for word in text.split())

def title_case(text):
    return text.title()

def uppercase_all(text):
    return text.upper()

def toggle_case(text):
    return ''.join(char.upper() if char.islower() else char.lower() 
                  for char in text)

# Cipher implementations
def caesar_cipher(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def vigenere_cipher(text, key="SECRET"):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def atbash_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr(ord('Z') - (ord(char) - base))
        else:
            result += char
    return result

# Base encoders
def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def encode_base32(text):
    return base64.b32encode(text.encode()).decode()

def encode_hex(text):
    return text.encode().hex()

# Steganography
def invisible_text(text):
    return '\u200B'.join(text)

def zero_width_encode(text):
    return '\u200B'.join(text)

# Format transformations
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_numbers(text):
    return re.sub(r'\d', '', text)

def reverse_text(text):
    return text[::-1]

def shuffle_characters(text):
    chars = list(text)
    random.shuffle(chars)
    return ''.join(chars)

def remove_spaces(text):
    return text.replace(' ', '')

def mirror_text(text):
    return text[::-1]

def leetspeak(text):
    replacements = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
    return ''.join(replacements.get(c.lower(), c) for c in text)

# Randomizer
def randomize_text(text):
    transforms = [
        ("upper", lambda x: x.upper()),
        ("lower", lambda x: x.lower()),
        ("reverse", lambda x: x[::-1]),
        ("shuffle", lambda x: ''.join(random.sample(x, len(x)))),
        ("leetspeak", leetspeak),
        ("mirror", mirror_text)
    ]
    
    result = []
    for word in text.split():
        transform = random.choice(transforms)
        result.append(transform[1](word))
        
    return ' '.join(result)

# Main app
def main():
    st.title("🐍 Parseltongue: Complete Text Transformation Tool")
    
    # Sidebar with categories
    st.sidebar.header("Categories")
    category = st.sidebar.radio(
        "Select category:",
        ["Case Transformations", "Ciphers", "Encoding", "Formatting", "Visual", "Randomizer"]
    )
    
    # Text input
    text = st.text_area("Enter your text:", height=200)
    
    # Category-specific options
    if category == "Case Transformations":
        transform_type = st.selectbox(
            "Select transformation:",
            ["Alternating Case", "camelCase", "Capitalize Words", "kebab-case", 
             "Lowercase All", "Random Case", "Sentence Case", "snake_case", 
             "Title Case", "Uppercase All", "Toggle Case"]
        )
        
        if st.button("Transform"):
            if transform_type == "Alternating Case":
                result = alternating_case(text)
            elif transform_type == "camelCase":
                result = camel_case(text)
            elif transform_type == "Capitalize Words":
                result = capitalize_words(text)
            elif transform_type == "kebab-case":
                result = kebab_case(text)
            elif transform_type == "Lowercase All":
                result = lowercase_all(text)
            elif transform_type == "Random Case":
                result = random_case(text)
            elif transform_type == "Sentence Case":
                result = sentence_case(text)
            elif transform_type == "snake_case":
                result = snake_case(text)
            elif transform_type == "Title Case":
                result = title_case(text)
            elif transform_type == "Uppercase All":
                result = uppercase_all(text)
            elif transform_type == "Toggle Case":
                result = toggle_case(text)
                
            st.code(result)
            st.session_state.history.append(f"Case: {result}")
    
    elif category == "Ciphers":
        cipher_type = st.selectbox(
            "Select cipher:",
            ["Caesar Cipher", "Vigenère Cipher", "Atbash Cipher"]
        )
        
        if cipher_type == "Caesar Cipher":
            shift = st.slider("Shift value:", min_value=1, max_value=25, value=3)
            if st.button("Encrypt"):
                result = caesar_cipher(text, shift)
                st.code(result)
                st.session_state.history.append(f"Caesar({shift}): {result}")
        
        elif cipher_type == "Vigenère Cipher":
            key = st.text_input("Key:", "SECRET")
            if st.button("Encrypt"):
                result = vigenere_cipher(text, key)
                st.code(result)
                st.session_state.history.append(f"Vigenère({key}): {result}")
        
        elif cipher_type == "Atbash Cipher":
            if st.button("Encrypt"):
                result = atbash_cipher(text)
                st.code(result)
                st.session_state.history.append(f"Atbash: {result}")
    
    elif category == "Encoding":
        encoding_type = st.selectbox(
            "Select encoding:",
            ["Base64", "Base32", "Hexadecimal", "Invisible Text", "Zero-Width"]
        )
        
        if st.button("Encode"):
            if encoding_type == "Base64":
                result = encode_base64(text)
            elif encoding_type == "Base32":
                result = encode_base32(text)
            elif encoding_type == "Hexadecimal":
                result = encode_hex(text)
            elif encoding_type == "Invisible Text":
                result = invisible_text(text)
            elif encoding_type == "Zero-Width":
                result = zero_width_encode(text)
                
            st.code(result)
            st.session_state.history.append(f"{encoding_type}: {result}")
    
    elif category == "Formatting":
        format_type = st.selectbox(
            "Select format:",
            ["Remove Punctuation", "Remove Numbers", "Reverse Text", 
             "Shuffle Characters", "Remove Spaces", "Mirror Text"]
        )
        
        if st.button("Format"):
            if format_type == "Remove Punctuation":
                result = remove_punctuation(text)
            elif format_type == "Remove Numbers":
                result = remove_numbers(text)
            elif format_type == "Reverse Text":
                result = reverse_text(text)
            elif format_type == "Shuffle Characters":
                result = shuffle_characters(text)
            elif format_type == "Remove Spaces":
                result = remove_spaces(text)
            elif format_type == "Mirror Text":
                result = mirror_text(text)
                
            st.code(result)
            st.session_state.history.append(f"Format: {result}")
    
    elif category == "Visual":
        visual_type = st.selectbox(
            "Select visual effect:",
            ["Leetspeak", "Mirror Text"]
        )
        
        if st.button("Apply Effect"):
            if visual_type == "Leetspeak":
                result = leetspeak(text)
            elif visual_type == "Mirror Text":
                result = mirror_text(text)
                
            st.code(result)
            st.session_state.history.append(f"Visual: {result}")
    
    elif category == "Randomizer":
        if st.button("Randomize Text"):
            result = randomize_text(text)
            st.code(result)
            st.session_state.history.append(f"Randomized: {result}")
    
    # History
    if st.session_state.history:
        st.sidebar.subheader("Transformation History")
        for item in st.session_state.history[-5:]:  # Show last 5 items
            st.sidebar.write(item)

if __name__ == "__main__":
    main()
