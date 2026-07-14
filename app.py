import streamlit as st

def generate_tokenade(depth, breadth, repeats, noise_level):
    # Logic to build the payload structure based on user inputs
    payload = "{" * depth
    for _ in range(repeats):
        payload += "TOKEN" * breadth + ("\u200b" * noise_level)
    payload += "}" * depth
    return payload

st.title("💣 Tokenade Payload Builder")

with st.sidebar:
    st.header("Parameters")
    depth = st.slider("Depth", 1, 10, 3)
    breadth = st.slider("Breadth", 1, 10, 5)
    repeats = st.slider("Repeats", 1, 100, 10)
    noise = st.checkbox("Include Unicode/ZWSP Noise")
    
if st.button("Generate Payload"):
    output = generate_tokenade(depth, breadth, repeats, 1 if noise else 0)
    
    # Safety Check
    token_est = len(output) # Simplified metric
    if token_est > 10000:
        st.warning(f"Danger: High token threshold reached ({token_est} chars)")
    
    st.text_area("Payload Output", output, height=200)
