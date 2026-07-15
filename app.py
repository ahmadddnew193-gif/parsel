import streamlit as st
import base64
import random
import re
import string
import urllib.parse
import requests
from collections import Counter

# --- INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = []
if "copy_history" not in st.session_state:
    st.session_state.copy_history = []
if "openrouter_api_key" not in st.session_state:
    st.session_state.openrouter_api_key = ""
if "generated_cases" not in st.session_state:
    st.session_state.generated_cases = []

st.set_page_config(page_title="Parseltongue V4", page_icon="🐍", layout="wide")

# --- SAFE DICTIONARY-BASED TRANSFORMATION MAPS ---
MAP_BOLD_ITALIC = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
)))

MAP_BOLD = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁🇨🇩🇪options🇫𝐆𝐇𝐈𝐉𝐊🇱🇲🇳🇴🇵𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
)))

MAP_BUBBLE = str.maketrans(dict(zip(
    string.ascii_letters,
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
)))

MAP_CIRCLED = str.maketrans(dict(zip(
    string.ascii_letters,
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
)))

MAP_CURSIVE = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝒀𝓩"
)))

MAP_CYRILLIC_STYLIZED = str.maketrans(dict(zip(
    string.ascii_letters,
    "авсdеfԍнijкlмԍорԛяѕтцѵшхуzАВСDЕFԌНIJКLМԌОРԚЯЅТЦѴШХУZ"
)))

MAP_DOUBLE_STRUCK = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
)))

MAP_FRAKTUR = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝔞𝔟𝔳𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅𝔆𝔇𝔈𝔉𝔊𝔋𝔌𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔𝔕𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔝"
)))

MAP_FULL_WIDTH = str.maketrans(dict(zip(
    string.ascii_letters,
    "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
)))

MAP_ITALIC = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶content𝐷𝐸𝐹content𝐺contentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontent"
)))

MAP_MEDIEVAL = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
)))

MAP_MONOSPACE = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔|𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱🇨🇩🇪🇫🇬🇭🇮𝙹𝙺🇱🇲🇳🇴🇵𝚀🇷🇸🇹🇺🇻🇼𝚇𝚈𝚉"
)))

MAP_SMALL_CAPS = str.maketrans(dict(zip(
    string.ascii_letters,
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡXʏᴢ"
)))

# Robust Subscript Dictionary Mapping
sub_dict = {
    'a': 'ₐ', 'b': 'ᵦ', 'c': '꜀', 'd': 'ᵈ', 'e': 'ₑ', 'f': '𝆑', 'g': 'g', 'h': 'ₕ', 'i': 'ᵢ', 
    'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ', 'p': 'ₚ', 'q': 'q', 'r': 'ᵣ', 
    's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ', 'v': 'ᵥ', 'w': 'w', 'x': 'ₓ', 'y': 'ᵧ', 'z': '𝓏'
}
sub_dict.update({k.upper(): v for k, v in sub_dict.items()})
MAP_SUB_SCRIPT = str.maketrans(sub_dict)

# Robust Superscript Dictionary Mapping
super_dict = {
    'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 
    'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ', 'p': 'ᵖ', 'q': 'ᵠ', 'r': 'ʳ', 
    's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ'
}
super_dict.update({k.upper(): v.upper() for k, v in super_dict.items()})
MAP_SUPER_SCRIPT = str.maketrans(super_dict)

MAP_ELDER_FUTHARK = str.maketrans(dict(zip(
    string.ascii_letters,
    "ᚨᛒᚲᛞᛖᚠᚷᚺᛁᛃᚲᛚᛗᚾᛟᛈᛢᚱᛊᛏᚢᚠᚹᛝᛦᛏᚨᛒᚲᛞᛖᚠᚷᚺᛁᛃᚲᛚᛗᚾᛟᛈᛢᚱᛊᛏᚢᚠᚹᛝᛦᛏ"
)))

MAP_OGHAM = str.maketrans(dict(zip(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "ᚐᚒᚓᚔᚕᚖᚗᚘᚙᚚᚐᚒᚓᚔᚕᚖᚗᚘᚙᚚ "
)))

MAP_ALCHEMICAL = str.maketrans(dict(zip(
    string.ascii_letters,
    "🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭"
)))

MAP_GREEK = str.maketrans(dict(zip(
    string.ascii_letters,
    "αβψδεφγηιξκλμνοπχρστυωωςγζΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠΧΡΣ𝐓ΥΩΩΣΓΖ"
)))

MAP_PIGPEN_CHARS = {
    'a': '⊓', 'b': '⊔', 'c': '⊏', 'd': '⊐', 'e': '□', 'f': '◪', 'g': '◩', 'h': '◨', 'i': '◧',
    'j': '⊓̣', 'k': '⊔̣', 'l': '⊏̣', 'm': '⊐̣', 'n': '□̣', 'o': '◪̣', 'p': '◩̣', 'q': '◨̣', 'r': '◧̣',
    's': '∨', 't': '∧', 'u': '>', 'v': '<', 'w': '∨̣', 'x': '∧̣', 'y': '>̣', 'z': '<̣'
}

MAP_AUREBESH = {
    'a': 'Aurek', 'b': 'Besh', 'c': 'Cresh', 'd': 'Dorn', 'e': 'Esk', 'f': 'Forn', 'g': 'Grek',
    'h': 'Herf', 'i': 'Isk', 'j': 'Jenth', 'k': 'Krill', 'l': 'Leth', 'm': 'Mern', 'n': 'Nern',
    'o': 'Osk', 'p': 'Peth', 'q': 'Qek', 'r': 'Resh', 's': 'Senth', 't': 'Trill', 'u': 'Usk',
    'v': 'Vev', 'w': 'Wesk', 'x': 'Xesh', 'y': 'Yirt', 'z': 'Zerek'
}

# Homoglyph database for confusion mutations
HOMOGLYPHS = {
    'a': ['а', 'ａ', 'ɑ', 'å', 'ǎ'], 'b': ['Ь', 'ｂ', 'ь', 'Б', 'ß'], 'c': ['с', 'ｃ', 'ⅽ', 'ć'],
    'd': ['ⅾ', 'ｄ', 'đ', 'ď'], 'e': ['е', 'ｅ', 'ė', 'ě', 'ē'], 'f': ['ｆ', 'ƒ'], 'g': ['ｇ', 'ğ', 'ġ'],
    'h': ['ｈ', 'һ', 'ћ'], 'i': ['і', 'ｉ', 'í', 'ǐ', 'ï'], 'j': ['ｊ', 'ј'], 'k': ['ｋ', 'κ'],
    'l': ['ｌ', 'ⅼ', 'ł', 'ľ'], 'm': ['ｍ', 'ⅿ'], 'n': ['ｎ', 'ñ', 'ń'], 'o': ['о', 'ｏ', 'ö', 'ő', 'ø'],
    'p': ['р', 'ｐ'], 'q': ['ｑ'], 'r': ['ｒ', 'ŕ', 'ř'], 's': ['ｓ', 'ѕ', 'ś', 'š'],
    't': ['ｔ', 'ť', 'ţ'], 'u': ['ｕ', 'μ', 'ü', 'ū', 'ǔ'], 'v': ['ｖ', 'ⅴ'], 'w': ['ｗ', 'ŵ'],
    'x': ['х', 'ｘ', 'ⅹ'], 'y': ['у', 'ｙ', 'ý', 'ÿ'], 'z': ['ｚ', 'ž', 'ź', 'ż'],
    'A': ['А', 'Ａ'], 'B': ['В', 'Ｂ'], 'C': ['С', 'Ｃ'], 'D': ['Ｄ'], 'E': ['Е', 'Ｅ'], 'F': ['Ｆ'],
    'G': ['Ｇ'], 'H': ['Н', 'Ｈ'], 'I': ['І', 'Ｉ'], 'J': ['Ｊ', 'Ј'], 'K': ['Ｋ'], 'L': ['Ｌ'],
    'M': ['Ｍ', 'М'], 'N': ['Ｎ'], 'O': ['О', 'Ｏ'], 'P': ['Р', 'Ｐ'], 'Q': ['Ｑ'], 'R': ['Ｒ'],
    'S': ['Ｓ', 'Ѕ'], 'T': ['Ｔ'], 'U': ['Ｕ'], 'V': ['Ｖ', 'Ⅴ'], 'W': ['Ｗ'], 'X': ['Х', 'Ｘ'],
    'Y': ['Ү', 'Ｙ'], 'Z': ['Ｚ']
}

# Combine all functions for flat selection
TRANSFORMS = {
    "Case": {
        "Alternating Case": lambda t: ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(t)),
        "camelCase": lambda t: ''.join([t.split()[0].lower()] + [w.capitalize() for w in t.split()[1:]]) if t.split() else t,
        "Capitalize Words": lambda t: ' '.join(w.capitalize() for w in t.split()),
        "kebab-case": lambda t: '-'.join(w.lower() for w in t.split()),
        "Lowercase All": lambda t: t.lower(),
        "Random Case": lambda t: ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in t),
        "Sentence Case": lambda t: '. '.join(s.capitalize() for s in t.split('. ')),
        "snake_case": lambda t: '_'.join(w.lower() for w in t.split()),
        "Title Case": lambda t: t.title(),
        "Uppercase All": lambda t: t.upper(),
        "Toggle Case": lambda t: ''.join(c.upper() if c.islower() else c.lower() for c in t)
    },
    "Unicode": {
        "Bold Italic": lambda t: t.translate(MAP_BOLD_ITALIC),
        "Bold": lambda t: t.translate(MAP_BOLD),
        "Bubble": lambda t: t.translate(MAP_BUBBLE),
        "Circled": lambda t: t.translate(MAP_CIRCLED),
        "Cursive": lambda t: t.translate(MAP_CURSIVE),
        "Double-Struck": lambda t: t.translate(MAP_DOUBLE_STRUCK),
        "Fraktur": lambda t: t.translate(MAP_FRAKTUR),
        "Full Width": lambda t: t.translate(MAP_FULL_WIDTH),
        "Italic": lambda t: t.translate(MAP_ITALIC),
        "Medieval": lambda t: t.translate(MAP_MEDIEVAL),
        "Monospace": lambda t: t.translate(MAP_MONOSPACE),
        "Small Caps": lambda t: t.translate(MAP_SMALL_CAPS),
        "Subscript": lambda t: t.translate(MAP_SUB_SCRIPT),
        "Superscript": lambda t: t.translate(MAP_SUPER_SCRIPT)
    }
}

ALL_FLAT_FUNCS = []
for category_sub in TRANSFORMS.values():
    for func in category_sub.values():
        ALL_FLAT_FUNCS.append(func)

def run_transform(text, category, method):
    return TRANSFORMS.get(category, {}).get(method, lambda t: t)(text)

# --- SIDEBAR: CONTROLS & CONFIG ---
with st.sidebar:
    st.title("🐍 Controls & Config")
    
    with st.expander("🔑 Advanced Settings (API Connection)", expanded=True):
        st.session_state.openrouter_api_key = st.text_input(
            "OpenRouter API Key", 
            value=st.session_state.openrouter_api_key, 
            type="password",
            placeholder="sk-or-v1-..."
        )
        st.caption("Required for the PromptCraft AI Tab.")
        
    with st.expander("📋 Copy History", expanded=True):
        if not st.session_state.copy_history:
            st.info("No copy history yet. Use the mutation feature to auto-populate.")
        else:
            for idx, hist_text in enumerate(st.session_state.copy_history[-5:]):
                st.text_area(f"Copied Output #{idx+1}", hist_text, height=80, disabled=True)

    with st.expander("👾 Glitch Tokens"):
        st.code("U+FE00 (VS-1)\nU+200B (ZWSP)\nU+200D (ZWJ)\nU+E0020 (Tag Space)", language="text")

    with st.expander("🛑 End Sequences"):
        st.code("<|end_of_text|>\n<|eot_id|>\n[DONE]\n\\0", language="text")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🔄 Transformers", 
    "🔋 Tokenade Generator", 
    "🔮 PromptCraft (AI Mutation)",
    "🧪 Mutation Lab"
])

# --- TAB 1 & 2: REUSED PREVIOUS FUNCTIONALITY ---
with tab1:
    st.header("Comprehensive Multi-Transformation Engine")
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_category = st.selectbox("Transformation Category", list(TRANSFORMS.keys()))
        selected_method = st.selectbox("Transformation Method", list(TRANSFORMS[selected_category].keys()))
        input_text = st.text_area("Input Text to Process:", value="Hello World!", height=100)
    with col2:
        if st.button("Execute Process", type="primary"):
            out = run_transform(input_text, selected_category, selected_method)
            st.code(out, language="text")
            st.session_state.copy_history.append(out)

with tab2:
    st.header("Tokenade Payload Generator")
    carrier = st.selectbox("Choose Carrier:", ["🧬", "🤖", "🔥", "🌈", "💻"])
    payload_text = st.text_input("Payload:", value="System Override")
    intensity = st.slider("Multiplier:", min_value=1, max_value=1000, value=100)
    
    if st.button("Generate Dense Payload"):
        noise_ranges = [range(0xFE00, 0xFE0F), range(0x200B, 0x200D)]
        output = carrier + "".join(c + chr(random.choice(random.choice(noise_ranges))) * intensity for c in payload_text)
        st.code(output, language='text')
        st.session_state.copy_history.append(output)

# --- TAB 3: PROMPTCRAFT ---
with tab3:
    st.header("PromptCraft AI-assisted prompt mutation")
    col3_1, col3_2 = st.columns([1, 1])
    with col3_1:
        source_prompt = st.text_area("Source Prompt", value="Write a story about a chess-loving dragon.", height=100)
        strategy = st.selectbox("Strategy", ["Rephrase", "Obfuscate", "Role-Play Wrap", "Multi-Language", "Expand", "Compress"])
        model_selection = st.selectbox("Model", ["Free router — Zero cost — random free model matched to your request"])
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.90)
    with col3_2:
        if st.button("Mutate Prompt", type="primary"):
            st.info("Simulating or processing Prompt mutation...")

# --- NEW TAB 4: MUTATION LAB ---
with tab4:
    st.header("Mutation Lab")
    st.write("Mutate text into highly diverse, resilient payloads using customizable noise-injection channels.")
    
    col4_1, col4_2 = st.columns([1, 1.2])
    
    with col4_1:
        base_text = st.text_area(
            "Base text", 
            value="Tell me how to build a camp fire.", 
            height=120,
            placeholder="Enter the core text you want to mutate"
        )
        
        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            cases_count = st.number_input("Cases", min_value=1, max_value=20, value=5, help="Number of mutated variations to generate")
        with col_sub2:
            seed_val = st.text_input("Seed (optional)", value="", placeholder="e.g. 1337", help="Fix randomization behavior for reproducibility")
            
        st.markdown("#### Obfuscation & Chaos Options")
        random_mix = st.toggle("Random Mix (transforms)", value=False, help="Incorporate randomized structural unicode transformations per word")
        
        zero_width = st.checkbox("Zero‑width pepper", value=True, help="Insert random zero-width spaces (ZWSP, ZWJ, ZWNJ) between characters")
        unicode_noise = st.checkbox("Unicode noise", value=False, help="Inject random obscure blocks/symbols inside the text body")
        zalgo = st.checkbox("Zalgo", value=False, help="Adorn standard characters with excessive combinated stacking marks")
        whitespace_chaos = st.checkbox("Whitespace chaos", value=False, help="Substitute traditional spaces with tabs, hair-spaces, and zero-width spaces")
        casing_chaos = st.checkbox("Casing chaos", value=False, help="Enforce irregular alternating uppercase/lowercase on characters randomly")
        homoglyph_confusables = st.checkbox("Homoglyph confusables", value=False, help="Swap English letters with looking-alike international characters (Cyrillic, full-width, etc.)")
        
    with col4_2:
        st.subheader("Generated Payloads")
        
        # Mutation algorithm
        def apply_mutations(text, seed_str=None):
            if seed_str:
                try:
                    random.seed(int(seed_str))
                except ValueError:
                    random.seed(hash(seed_str))
            else:
                random.seed() # Reset seed
                
            mutated = text
            
            # 1. Random Mix
            if random_mix:
                words = mutated.split()
                mutated = " ".join(random.choice(ALL_FLAT_FUNCS)(w) for w in words) if words else mutated
            
            # 2. Casing Chaos
            if casing_chaos:
                mutated = "".join(c.upper() if random.random() > 0.5 else c.lower() for c in mutated)
                
            # 3. Homoglyph swap
            if homoglyph_confusables:
                new_chars = []
                for char in mutated:
                    if char in HOMOGLYPHS and random.random() > 0.3: # 70% chance to swap
                        new_chars.append(random.choice(HOMOGLYPHS[char]))
                    else:
                        new_chars.append(char)
                mutated = "".join(new_chars)
                
            # 4. Zalgo Injection (combining marks)
            if zalgo:
                zalgo_marks = [chr(i) for i in range(0x0300, 0x036F)]
                new_chars = []
                for char in mutated:
                    new_chars.append(char)
                    if char.isalpha() and random.random() > 0.6:
                        # Stacking combining characters
                        for _ in range(random.randint(1, 5)):
                            new_chars.append(random.choice(zalgo_marks))
                mutated = "".join(new_chars)
                
            # 5. Unicode Noise
            if unicode_noise:
                noise_chars = ["⚡", "⭐", "✴️", "☯️", "💮", "🌀", "💠", "🪐", "⚕️", "⚙️"]
                new_chars = []
                for char in mutated:
                    new_chars.append(char)
                    if random.random() > 0.85:
                        new_chars.append(random.choice(noise_chars))
                mutated = "".join(new_chars)

            # 6. Whitespace Chaos
            if whitespace_chaos:
                # Replace space with tabs, narrow spaces, or non-breaking spaces
                spaces = ["\t", "\u2004", "\u2005", "\u2006", "\u2009", "\u200A", "\u1680"]
                mutated = "".join(random.choice(spaces) if c == ' ' else c for c in mutated)

            # 7. Zero-Width Pepper
            if zero_width:
                zw_chars = ["\u200B", "\u200C", "\u200D", "\uFEFF"]
                new_chars = []
                for char in mutated:
                    new_chars.append(char)
                    if random.random() > 0.5:
                        new_chars.append(random.choice(zw_chars))
                mutated = "".join(new_chars)
                
            return mutated

        if st.button("Generate Cases", type="primary"):
            if not base_text:
                st.warning("Please provide some base text to begin mutation.")
            else:
                st.session_state.generated_cases = []
                # Generate unique variations
                for i in range(int(cases_count)):
                    # Use provided seed or generate an incremental one to vary outputs per case
                    current_seed = f"{seed_val}_{i}" if seed_val else f"{random.randint(1,999999)}_{i}"
                    result = apply_mutations(base_text, current_seed)
                    st.session_state.generated_cases.append(result)
                    
        # Output Layout
        if st.session_state.generated_cases:
            # Action buttons row
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                # Copy All helper
                combined_cases = "\n---\n".join(st.session_state.generated_cases)
                st.text_area("Bulk Preview (Copy All)", combined_cases, height=120)
                st.caption("You can copy the raw combined block above.")
                
            with act_col2:
                # File download
                st.download_button(
                    label="💾 Download Payloads File",
                    data=combined_cases,
                    file_name="mutated_payloads.txt",
                    mime="text/plain"
                )
                st.caption("Save all generated payloads down into a local text file.")
            
            # Detailed listing output
            st.markdown("---")
            for index, case_text in enumerate(st.session_state.generated_cases):
                st.markdown(f"**Case #{index + 1}**")
                st.code(case_text, language="text")
                # Automatically feed copy history for sidebar
                if case_text not in st.session_state.copy_history:
                    st.session_state.copy_history.append(case_text)
