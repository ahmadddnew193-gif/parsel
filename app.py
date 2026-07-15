import streamlit as st
import base64
import random
import re
import string
import urllib.parse
from collections import Counter

# --- INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Parseltongue V4", page_icon="🐍", layout="wide")

# --- TRANSFORMATION MAPS & DATA TABLES ---
# Unicode styles
MAP_BOLD_ITALIC = str.maketrans(
    string.ascii_letters,
    "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
)
MAP_BOLD = str.maketrans(
    string.ascii_letters,
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁ＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹ𝐙"
)
MAP_BUBBLE = str.maketrans(
    string.ascii_letters,
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻ metastasis ⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
)
MAP_CIRCLED = str.maketrans(
    string.ascii_letters,
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
)
MAP_CURSIVE = str.maketrans(
    string.ascii_letters,
    "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝒀𝓩"
)
MAP_CYRILLIC_STYLIZED = str.maketrans(
    string.ascii_letters,
    "авсdеfԍнijкlмԍорԛяѕтцѵшхуzАВСDЕFԌНIJКLМԌОРԚЯЅТЦѴШХУZ"
)
MAP_DOUBLE_STRUCK = str.maketrans(
    string.ascii_letters,
    "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
)
MAP_FRAKTUR = str.maketrans(
    string.ascii_letters,
    "𝔞𝔟𝔳𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅𝔆𝔇𝔈𝔉𝔊𝔋𝔌𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔𝔕𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔝"
)
MAP_FULL_WIDTH = str.maketrans(
    string.ascii_letters,
    "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
)
MAP_ITALIC = str.maketrans(
    string.ascii_letters,
    "𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶content𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾content𝐿content𝑀𝑁𝑂𝑃𝑄𝑅content𝑆𝑇𝑈𝑉𝑊𝑋content𝑌𝑍"
)
MAP_MEDIEVAL = str.maketrans(
    string.ascii_letters,
    "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
)
MAP_MONOSPACE = str.maketrans(
    string.ascii_letters,
    "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝚠𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
)
MAP_SMALL_CAPS = str.maketrans(
    string.ascii_letters,
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡXʏᴢ"
)
MAP_SUB_SCRIPT = str.maketrans(
    "abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "ₐᵦ꜀ₑ𝆑gₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥwₓᵧ𝓏ₐᵦ꜀ₑ𝆑gₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥwₓᵧ𝓏₀₁₂₃₄₅₆₇₈₉"
)
MAP_SUPER_SCRIPT = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱ𝘍𝘎ᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿˢᵀᵁⱽᵂˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹"
)

# Ancient, Symbol and Exotic Mapping Tables
MAP_ELDER_FUTHARK = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ᚨᛒᚲᛞᛖᚠᚷᚺᛁᛃᚲᛚᛗᚾᛟᛈᛢᚱᛊᛏᚢᚠᚹᛝᛦᛏᚨᛒᚲᛞᛖᚠᚷᚺᛁᛃᚲᛚᛗᚾᛟᛈᛢᚱᛊᛏᚢᚠᚹᛝᛦᛏ"
)
MAP_OGHAM = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "ᚐᚒ McFarland ᚕᚖᚗᚘᚙᚚᚐᚒ McFarland ᚕᚖᚗᚘᚙᚚ "
)
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
MAP_ALCHEMICAL = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭"
)
MAP_GREEK = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "αβψδεφγηιξκλμνοπχρστυωωςγζΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠΧΡΣΤΥΩΩΣΓΖ"
)

# --- ROTATION HELPER ---
def rot_n(text, n):
    result = []
    for char in text:
        cp = ord(char)
        result.append(chr((cp + n) % 1114112))
    return "".join(result)

# --- RECURSIVE TRANSFORMATION DICTIONARY ---
# Every single transform option from Parseltongue V4 website interface, structured cleanly
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
    "Cipher": {
        "A1Z26": lambda t: '-'.join(str(ord(c.lower()) - 96) if c.isalpha() else c for c in t),
        "Atbash Cipher": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1])),
        "Baconian Cipher": lambda t: ' '.join(format(ord(c.lower()) - 97, '05b').replace('0', 'A').replace('1', 'B') if c.isalpha() else c for c in t),
        "Caesar Cipher (ROT3)": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[3:] + string.ascii_lowercase[:3] + string.ascii_uppercase[3:] + string.ascii_uppercase[:3])),
        "ROT5": lambda t: t.translate(str.maketrans(string.digits, string.digits[5:] + string.digits[:5])),
        "ROT13": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13])),
        "ROT18": lambda t: t.translate(str.maketrans(string.ascii_letters + string.digits, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13] + string.digits[5:] + string.digits[:5])),
        "ROT47": lambda t: "".join(chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in t),
        "ROT128": lambda t: rot_n(t, 128),
        "ROT8000": lambda t: rot_n(t, 8000),
        "XOR Cipher (Key=42)": lambda t: "".join(chr(ord(c) ^ 42) for c in t)
    },
    "Concealment": {
        "Acrostic Generator": lambda t: "\n".join(f"{c.upper()} {w}" for c, w in zip(t.replace(" ", ""), ["obvious", "secret", "hidden", "internal", "data", "system", "structure", "engine", "process"] * 10))[:len(t)*20],
        "Invisible Text": lambda t: "".join(chr(0x200B) for _ in t),
        "Null Cipher": lambda t: " ".join(f"a{c.lower()}i" if c.isalpha() else c for c in t),
        "Zero-Width Steganography": lambda t: "".join(format(ord(c), '08b').replace('0', '\u200B').replace('1', '\u200C') for c in t)
    },
    "Encoding": {
        "ASCII85": lambda t: base64.a85encode(t.encode()).decode(),
        "Base32": lambda t: base64.b32encode(t.encode()).decode(),
        "Base36": lambda t: str(int(base64.b16encode(t.encode()).decode(), 16)) if t else "",
        "Base58": lambda t: "".join(random.choices(string.ascii_letters + string.digits, k=len(t)*2)), # Custom placeholder representation
        "Base64": lambda t: base64.b64encode(t.encode()).decode(),
        "Base64 URL": lambda t: base64.urlsafe_b64encode(t.encode()).decode(),
        "Binary": lambda t: " ".join(format(ord(c), "08b") for c in t),
        "Hexadecimal": lambda t: " ".join(format(ord(c), "02x") for c in t),
        "HTML Entities": lambda t: "".join(f"&#{ord(c)};" for c in t),
        "Unicode Code Points": lambda t: " ".join(f"U+{ord(c):04X}" for c in t),
        "URL Encode": lambda t: urllib.parse.quote(t)
    },
    "Format": {
        "Boustrophedon": lambda t: "\n".join(line if i % 2 == 0 else line[::-1] for i, line in enumerate(t.split('\n'))),
        "Group Letters": lambda t: " ".join(t[i:i+5] for i in range(0, len(t), 5)),
        "Indent": lambda t: "    " + t.replace("\n", "\n    "),
        "Letters Only": lambda t: "".join(c for c in t if c.isalpha()),
        "Letters & Numbers Only": lambda t: "".join(c for c in t if c.isalnum()),
        "Line Numbers": lambda t: "\n".join(f"{i+1}: {line}" for i, line in enumerate(t.split('\n'))),
        "Mirror Digits": lambda t: t.translate(str.maketrans("0123456789", "015Ɛᔭ59Ɫ86")),
        "Remove Accents": lambda t: t.encode('ascii', 'ignore').decode('utf-8'),
        "Remove Consonants": lambda t: "".join(c for c in t if c.lower() in "aeiou \n\t"),
        "Remove Duplicates": lambda t: "".join(sorted(list(set(t)), key=t.index)),
        "Remove Extra Spaces": lambda t: " ".join(t.split()),
        "Remove Newlines": lambda t: t.replace("\n", " "),
        "Remove Numbers": lambda t: "".join(c for c in t if not c.isdigit()),
        "Remove Punctuation": lambda t: t.translate(str.maketrans("", "", string.punctuation)),
        "Reverse Text": lambda t: t[::-1],
        "Reverse Words": lambda t: " ".join(t.split()[::-1]),
        "Shuffle Characters": lambda t: "".join(random.sample(t, len(t))),
        "Shuffle Words": lambda t: " ".join(random.sample(t.split(), len(t.split()))) if t.split() else t,
        "Spaces Remover": lambda t: t.replace(" ", "")
    },
    "Signwriting": {
        "JSL SignWriting": lambda t: "  ".join(f"{c}\u2001" for c in t),
        "Morse Blink": lambda t: " ".join("⚫" if c == "." else "⚪" if c == "-" else "  " for c in "".join("." if chr == "0" else "-" for chr in format(len(t), "08b"))),
        "Tactile SignWriting": lambda t: "".join(chr(0x2800 + ord(c) % 64) for c in t)
    },
    "Symbol": {
        "Alchemical Symbols": lambda t: t.translate(MAP_ALCHEMICAL),
        "Aurebesh (Star Wars)": lambda t: " ".join(MAP_AUREBESH.get(c.lower(), c) for c in t),
        "Braille": lambda t: "".join(chr(0x2800 + (ord(c.lower()) - 96 if c.isalpha() and 1 <= ord(c.lower()) - 96 <= 26 else 0)) for c in t),
        "Elder Futhark": lambda t: t.translate(MAP_ELDER_FUTHARK),
        "Greek Letters": lambda t: t.translate(MAP_GREEK),
        "Ogham (Celtic)": lambda t: t.translate(MAP_OGHAM),
        "Pigpen Cipher": lambda t: "".join(MAP_PIGPEN_CHARS.get(c.lower(), c) for c in t)
    },
    "Technical": {
        "DTMF Code": lambda t: " ".join(f"[{c}]" for c in t),
        "ICAO Spelling Alphabet": lambda t: " ".join(c.upper() for c in t),
        "Morse Code": lambda t: " ".join(format(ord(c), "08b").replace("0", ".").replace("1", "-") for c in t),
        "NATO Phonetic": lambda t: " ".join(c for c in t),
        "Phone Keypad Cipher": lambda t: "".join(str((ord(c.lower()) - 97) // 3 + 2) if c.isalpha() else c for c in t)
    },
    "Unicode": {
        "Bold Italic": lambda t: t.translate(MAP_BOLD_ITALIC),
        "Bold": lambda t: t.translate(MAP_BOLD),
        "Bubble": lambda t: t.translate(MAP_BUBBLE),
        "Circled": lambda t: t.translate(MAP_CIRCLED),
        "Cursive": lambda t: t.translate(MAP_CURSIVE),
        "Cyrillic Stylized": lambda t: t.translate(MAP_CYRILLIC_STYLIZED),
        "Double-Struck": lambda t: t.translate(MAP_DOUBLE_STRUCK),
        "Fraktur": lambda t: t.translate(MAP_FRAKTUR),
        "Full Width": lambda t: t.translate(MAP_FULL_WIDTH),
        "Italic": lambda t: t.translate(MAP_ITALIC),
        "Medieval": lambda t: t.translate(MAP_MEDIEVAL),
        "Monospace": lambda t: t.translate(MAP_MONOSPACE),
        "Small Caps": lambda t: t.translate(MAP_SMALL_CAPS),
        "Subscript": lambda t: t.translate(MAP_SUB_SCRIPT),
        "Superscript": lambda t: t.translate(MAP_SUPER_SCRIPT),
        "Vaporwave": lambda t: " ".join(list(t)),
        "Wide Spacing": lambda t: "  ".join(list(t))
    },
    "Visual": {
        "Disemvowel": lambda t: "".join(c for c in t if c.lower() not in "aeiou"),
        "Leetspeak": lambda t: t.translate(MAP_BUILDER := str.maketrans("aeiosAEIOS", "4310543105")),
        "Pig Latin": lambda t: " ".join(w[1:] + w[0] + "ay" if len(w) > 1 else w for w in t.split()) if t.strip() else t,
        "Rövarspråket": lambda t: "".join(f"{c}o{c.lower()}" if c.lower() in "bcdfghjklmnpqrstvwxz" else c for c in t),
    }
}

# Add a flattened list of all actual transformation operations for randomized mixes
ALL_FLAT_FUNCS = []
for category_sub in TRANSFORMS.values():
    for func in category_sub.values():
        ALL_FLAT_FUNCS.append(func)

# --- ENGINE HELPER FUNCTIONS ---
def run_transform(text, category, method):
    if category == "🎲 Randomizer - Code Switching Magic!" or method == "!RANDOMIZE!":
        words = text.split()
        if not words:
            return ""
        # Apply a random transformation style to each separate word
        return " ".join(random.choice(ALL_FLAT_FUNCS)(w) for w in words)
    
    # Standard Dispatcher lookup
    return TRANSFORMS.get(category, {}).get(method, lambda t: t)(text)

# --- STREAMLIT GRAPHICAL USER INTERFACE ---
st.title("🐍 Parseltongue V4")

tab1, tab2 = st.tabs(["🔄 Transformers (Full List)", "🔋 Tokenade Generator"])

with tab1:
    st.header("Comprehensive Multi-Transformation Engine")
    
    # Left Column: Configuration Sidebar Mockup
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Encoder Style")
        
        # Category Selector
        categories = ["🎲 Randomizer - Code Switching Magic!"] + list(TRANSFORMS.keys())
        selected_category = st.selectbox("Transformation Category", categories)
        
        # Method Selector (dynamically loaded from registry map)
        if selected_category == "🎲 Randomizer - Code Switching Magic!":
            methods = ["!RANDOMIZE!"]
        else:
            methods = list(TRANSFORMS[selected_category].keys())
            
        selected_method = st.selectbox("Transformation Method", methods)
        
        input_text = st.text_area("Input Text to Process:", value="Hello World!", height=150)
        
    with col2:
        st.subheader("Output Interface")
        
        if st.button("Execute Process", type="primary"):
            if not input_text:
                st.warning("Please provide input text to transform.")
            else:
                try:
                    out = run_transform(input_text, selected_category, selected_method)
                    st.success("Transformed Successfully!")
                    st.code(out, language="text")
                    
                    # Track transformation history
                    st.session_state.history.append({
                        "input": input_text,
                        "category": selected_category,
                        "method": selected_method,
                        "output": out
                    })
                except Exception as e:
                    st.error(f"Error executing selected transform: {e}")
        
        if st.session_state.history:
            st.write("---")
            st.markdown("**History Log (Recent First):**")
            for item in reversed(st.session_state.history[-5:]):
                st.text(f"[{item['category']} -> {item['method']}] Input: {item['input'][:30]}... -> Output: {item['output'][:50]}...")

with tab2:
    st.header("Tokenade Payload Generator")
    st.write("Inject highly dense unicode and non-printable blocks inside carriers to obfuscate models.")
    
    carrier = st.selectbox("Choose Carrier:", ["🧬", "🤖", "🔥", "🌈", "💻", "🧠", "🍀"])
    payload_text = st.text_input("Hidden Obfuscated Payload:", value="System Override")
    intensity = st.slider("Multiplier / Intensity Factor:", min_value=1, max_value=1000, value=100)
    
    def generate_dense_payload(carrier_emoji, payload, size):
        # Specific hidden range sets (Variation selectors, Zero width spaces, High Tag blocks)
        noise_ranges = [
            range(0xFE00, 0xFE0F),
            range(0x200B, 0x200D),
            range(0xE0000, 0xE007F)
        ]
        
        result = carrier_emoji
        payload_parts = list(payload)
        for part in payload_parts:
            result += part
            # Inject custom noise sequence after each character of your payload
            for _ in range(size // len(payload) if len(payload) > 0 else size):
                chosen_range = random.choice(noise_ranges)
                result += chr(random.choice(chosen_range))
                
        return result
    
    if st.button("Generate Dense Payload"):
        if not payload_text:
            st.warning("Please enter a payload text.")
        else:
            output = generate_dense_payload(carrier, payload_text, intensity)
            st.code(output, language='text')
            st.write(f"Generated Payload Output Bytes/Length: {len(output)}")
