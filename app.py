import streamlit as st
import time

def to_unicode_tags(text):
    """
    Converts normal text into Invisible Unicode Tag characters.
    The Tag range starts at U+E0000.
    """
    res = "✨" # Their carrier
    for char in text:
        # Each character becomes a hidden tag character
        res += chr(0xE0000 + ord(char))
    return res

st.title("P4RS3LT0NGV3 Clone")

payload = st.text_input("Payload:", "TOKENADE")
mode = st.radio("Mode:", ["Carrier Mode (Invisible)", "Visible"])

if st.button("Generate"):
    if mode == "Carrier Mode (Invisible)":
        # This will produce the exact string structure as their repo
        output = to_unicode_tags(payload)
        st.code(output, language=None)
        st.write("Copy the code block above—it is now in the exact format they use.")
    else:
        # Your visible version
        st.write(f"⚓ {' ⚓ '.join(list(payload))} ⚓")
