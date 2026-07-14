import streamlit as st
import time

# --- P4RS3LT0NGV3 Logic Mockup ---
def get_tokenade_sequence(text, carrier="⚓"):
    """
    Creates the sequence of tokens modulated by the carrier.
    """
    for char in text:
        # Carrier mode: [Carrier] [Token] [Carrier]
        # This keeps the layout anchored.
        yield f"{carrier} {char} {carrier}\n"
        time.sleep(0.08) # Speed matching the canonical implementation

# --- UI Layer ---
st.set_page_config(page_title="Tokenade Engine", layout="centered")
st.title("🐍 Tokenade / P4RS3LT0NGV3")

payload_input = st.text_input("Payload Sequence", "TOKENADE_STREAM_DATA")
mode = st.toggle("Carrier Mode (Active)", value=True)

if st.button("Initialize Stream"):
    # Clear previous output
    output_container = st.empty()
    
    # We use a custom generator to yield the modulated stream
    def stream_gen():
        for char in payload_input:
            if mode:
                yield f"⚓ {char} ⚓"
            else:
                yield char
            time.sleep(0.05)

    # Use Streamlit's native streaming to prevent UI jitter
    st.write_stream(stream_gen)
