import streamlit as st
import base64
import random
from collections import Counter

st.set_page_config(page_title="Parseltongue", page_icon="🐍")

def apply_transformation(text, transform_type):
    """Apply selected transformation to text."""
    if transform_type == "Upper":
        return text.upper()
    elif transform_type == "Lower":
        return text.lower()
    elif transform_type == "Title":
        return text.title()
    elif transform_type == "CamelCase":
        words = text.split()
        return ''.join([words[0].lower()] + [word.capitalize() for word in words[1:]])
    elif transform_type == "Snake_Case":
        return '_'.join(word.lower() for word in text.split())
    elif transform_type == "Kebab_Case":
        return '-'.join(word.lower() for word in text.split())
    # Add other transformations here
    
    return text

def main():
    st.title("🐍 Parseltongue: Text Transformation Tool")
    
    text = st.text_area("Enter your text:")
    transform_type = st.selectbox(
        "Choose transformation:",
        ["Upper", "Lower", "Title", "CamelCase", "Snake_Case", "Kebab_Case"]
    )
    
    if st.button("Transform"):
        transformed = apply_transformation(text, transform_type)
        st.code(transformed)

if __name__ == "__main__":
    main()
