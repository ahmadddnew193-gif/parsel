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

st.set_page_config(page_title="Parseltongue V4", page_icon="🐍", layout="wide")

# --- SAFE DICTIONARY-BASED TRANSFORMATION MAPS ---
MAP_BOLD_ITALIC = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
)))

MAP_BOLD = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂content𝐃🇪options🇫𝐆𝐇𝐈𝐉𝐊🇱🇲🇳🇴🇵𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
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
    "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹content𝐺contentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontent"
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

# --- ANCIENT & SYMBOLIC ALPHABETS ---
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

def rot_n(text, n):
    result = []
    for char in text:
        cp = ord(char)
        result.append(chr((cp + n) % 1114112))
    return "".join(result)

# --- RECURSIVE TRANSFORMATION DICTIONARY ---
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
        "Base58": lambda t: "".join(random.choices(string.ascii_letters + string.digits, k=len(t)*2)),
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
        "Leetspeak": lambda t: t.translate(str.maketrans("aeiosAEIOS", "4310543105")),
        "Pig Latin": lambda t: " ".join(w[1:] + w[0] + "ay" if len(w) > 1 else w for w in t.split()) if t.strip() else t,
        "Rövarspråket": lambda t: "".join(f"{c}o{c.lower()}" if c.lower() in "bcdfghjklmnpqrstvwxz" else c for c in t),
    }
}

ALL_FLAT_FUNCS = []
for category_sub in TRANSFORMS.values():
    for func in category_sub.values():
        ALL_FLAT_FUNCS.append(func)

def run_transform(text, category, method):
    if category == "🎲 Randomizer - Code Switching Magic!" or method == "!RANDOMIZE!":
        words = text.split()
        if not words:
            return ""
        return " ".join(random.choice(ALL_FLAT_FUNCS)(w) for w in words)
    return TRANSFORMS.get(category, {}).get(method, lambda t: t)(text)

# --- SIDEBAR: SYSTEM OPTIONS, ADVANCED SETTINGS, COPY HISTORY ---
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
        st.code("""
U+FE00 (Variation Selector-1)
U+200B (Zero-Width Space)
U+200D (Zero-Width Joiner)
U+E0020 (Tag Space)
        """, language="text")
        st.caption("Use these dense non-printable characters for stealth obfuscation.")

    with st.expander("🛑 End Sequences"):
        st.code("<|end_of_text|>\n<|eot_id|>\n[DONE]\n\\0", language="text")
        st.caption("Common stopping tokens used to test sequence truncations.")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs([
    "🔄 Transformers (Full List)", 
    "🔋 Tokenade Generator", 
    "🔮 PromptCraft (AI Mutation)"
])

# --- TAB 1: TRANSFORMERS ---
with tab1:
    st.header("Comprehensive Multi-Transformation Engine")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Encoder Style")
        categories = ["🎲 Randomizer - Code Switching Magic!"] + list(TRANSFORMS.keys())
        selected_category = st.selectbox("Transformation Category", categories)
        
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
                    st.session_state.copy_history.append(out)
                    
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
            st.markdown("**Transformation Log (Recent First):**")
            for item in reversed(st.session_state.history[-5:]):
                st.text(f"[{item['category']} -> {item['method']}] Input: {item['input'][:30]}... -> Output: {item['output'][:50]}...")

# --- TAB 2: TOKENADE GENERATOR ---
with tab2:
    st.header("Tokenade Payload Generator")
    st.write("Inject highly dense unicode and non-printable blocks inside carriers to obfuscate models.")
    
    carrier = st.selectbox("Choose Carrier:", ["🧬", "🤖", "🔥", "🌈", "💻", "🧠", "🍀"])
    payload_text = st.text_input("Hidden Obfuscated Payload:", value="System Override")
    intensity = st.slider("Multiplier / Intensity Factor:", min_value=1, max_value=1000, value=100)
    
    def generate_dense_payload(carrier_emoji, payload, size):
        noise_ranges = [
            range(0xFE00, 0xFE0F),
            range(0x200B, 0x200D),
            range(0xE0000, 0xE007F)
        ]
        result = carrier_emoji
        payload_parts = list(payload)
        for part in payload_parts:
            result += part
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
            st.session_state.copy_history.append(output)
            st.write(f"Generated Payload Output Bytes/Length: {len(output)}")

# --- TAB 3: PROMPTCRAFT AI MUTATION ---
with tab3:
    st.header("PromptCraft AI-assisted prompt mutation")
    st.write("Leverage advanced Large Language Models to craft mutations using exact adversarial strategy frameworks.")
    
    if not st.session_state.openrouter_api_key:
        st.warning("⚠️ OpenRouter API Key is missing! Set your API key in the 'Advanced Settings' expander on the left sidebar.")

    col3_1, col3_2 = st.columns([1, 1])
    
    with col3_1:
        source_prompt = st.text_area(
            "Source Prompt", 
            value="Write a story about a dragon who loves playing chess.", 
            height=150
        )
        
        strategy = st.selectbox(
            "Strategy",
            ["Rephrase", "Obfuscate", "Role-Play Wrap", "Multi-Language", "Expand", "Compress", "Metaphor", "Fragment", "Custom"]
        )
        
        custom_instructions = ""
        if strategy == "Custom":
            custom_instructions = st.text_input("Custom strategy instructions:", placeholder="e.g., Rewrite in a Shakespearean Sonnet style")
        
        model_selection = st.selectbox(
            "Model",
            [
                "Free router — Zero cost — random free model matched to your request",
                "Auto router — Smart routing — billed at whichever model is picked",
                "Tencent: Hy3 (free) (tencent) · free",
                "Poolside: Laguna XS 2.1 (free) (poolside) · free",
                "Cohere: North Mini Code (free) (cohere) · free",
                "NVIDIA: Nemotron 3.5 Content Safety (free) (nvidia) · free",
                "NVIDIA: Nemotron 3 Ultra (free) (nvidia) · free",
                "NVIDIA: Nemotron 3 Nano Omni (free) (nvidia) · free",
                "Poolside: Laguna M.1 (free) (poolside) · free",
                "Google: Gemma 4 26B A4B  (free) (google) · free",
                "Google: Gemma 4 31B (free) (google) · free",
                "Google: Lyria 3 Pro Preview (google) · free",
                "Google: Lyria 3 Clip Preview (google) · free",
                "NVIDIA: Nemotron 3 Super (free) (nvidia) · free",
                "NVIDIA: Nemotron 3 Nano 30B A3B (free) (nvidia) · free",
                "NVIDIA: Nemotron Nano 12B 2 VL (free) (nvidia) · free",
                "Qwen: Qwen3 Next 80B A3B Instruct (free) (qwen) · free",
                "NVIDIA: Nemotron Nano 9B V2 (free) (nvidia) · free",
                "OpenAI: gpt-oss-20b (free) (openai) · free",
                "Qwen: Qwen3 Coder 480B A35B (free) (qwen) · free",
                "Venice: Uncensored (free) (cognitivecomputations) · free",
                "Google: Gemma 3 27B (google)",
                "Meta: Llama 3.3 70B Instruct (free) (meta-llama) · free",
                "Meta: Llama 3.2 3B Instruct (free) (meta-llama) · free",
                "Nous: Hermes 3 405B Instruct (free) (nousresearch) · free"
            ]
        )
        
        col_param1, col_param2 = st.columns(2)
        with col_param1:
            variants = st.number_input("Variants", min_value=1, max_value=5, value=1)
        with col_param2:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.90, step=0.05)

    with col3_2:
        st.subheader("Mutation Results")
        mutate_btn = st.button("Mutate Prompt", type="primary")
        
        # Strategy system prompts to steer OpenRouter execution
        strategy_system_prompts = {
            "Rephrase": "Rewrite the source prompt using completely different vocabulary and sentence structures while retaining 100% of the original logic.",
            "Obfuscate": "Rewrite the prompt to disguise or obfuscate its semantic elements using alternative synonyms, specialized terminology, or minor formatting masks while keeping the logic operational.",
            "Role-Play Wrap": "Wrap the source prompt inside an elaborate, fictional role-playing scenario or persona so that the core instruction is integrated seamlessly as a simulation rule.",
            "Multi-Language": "Mutate and translate sections of the key terms inside the instruction into multiple languages (such as French, Spanish, or Russian) interspersed with English guidelines.",
            "Expand": "Flesh out the prompt in highly elaborate, granular detail, adding background context, clear format constraints, step-by-step logic, and operational boundaries.",
            "Compress": "Condense the instructions into a minimal, highly efficient, and punchy format with absolutely zero fluff.",
            "Metaphor": "Express the core action and goal of the prompt using an extended conceptual metaphor or analogy.",
            "Fragment": "Deconstruct the prompt into fragmented, discrete instructional steps and a list of structural constraints.",
            "Custom": f"Apply this custom strategy instruction to mutate the prompt: '{custom_instructions}'"
        }
        
        # Map Selected display names to actual OpenRouter API model tags
        model_mapping = {
            "Free router — Zero cost — random free model matched to your request": "openrouter/free",
            "Auto router — Smart routing — billed at whichever model is picked": "openrouter/auto",
            "Tencent: Hy3 (free) (tencent) · free": "tencent/hy3:free",
            "Poolside: Laguna XS 2.1 (free) (poolside) · free": "poolside/laguna-xs-2.1:free",
            "Cohere: North Mini Code (free) (cohere) · free": "cohere/north-mini-code:free",
            "NVIDIA: Nemotron 3.5 Content Safety (free) (nvidia) · free": "nvidia/nemotron-3.5-content-safety:free",
            "NVIDIA: Nemotron 3 Ultra (free) (nvidia) · free": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "NVIDIA: Nemotron 3 Nano Omni (free) (nvidia) · free": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            "Poolside: Laguna M.1 (free) (poolside) · free": "poolside/laguna-m.1:free",
            "Google: Gemma 4 26B A4B  (free) (google) · free": "google/gemma-4-26b-it:free",
            "Google: Gemma 4 31B (free) (google) · free": "google/gemma-4-31b-it:free",
            "Google: Lyria 3 Pro Preview (google) · free": "google/lyria-3-pro-preview:free",
            "Google: Lyria 3 Clip Preview (google) · free": "google/lyria-3-clip-preview:free",
            "NVIDIA: Nemotron 3 Super (free) (nvidia) · free": "nvidia/nemotron-3-super-120b-a12b:free",
            "NVIDIA: Nemotron 3 Nano 30B A3B (free) (nvidia) · free": "nvidia/nemotron-3-nano-30b-a3b:free",
            "NVIDIA: Nemotron Nano 12B 2 VL (free) (nvidia) · free": "nvidia/nemotron-nano-12b-2-vl:free",
            "Qwen: Qwen3 Next 80B A3B Instruct (free) (qwen) · free": "qwen/qwen3-next-80b-it:free",
            "NVIDIA: Nemotron Nano 9B V2 (free) (nvidia) · free": "nvidia/nemotron-nano-9b-v2:free",
            "OpenAI: gpt-oss-20b (free) (openai) · free": "openai/gpt-oss-20b:free",
            "Qwen: Qwen3 Coder 480B A35B (free) (qwen) · free": "qwen/qwen3-coder-480b-it:free",
            "Venice: Uncensored (free) (cognitivecomputations) · free": "venice/uncensored:free",
            "Google: Gemma 3 27B (google)": "google/gemma-3-27b",
            "Meta: Llama 3.3 70B Instruct (free) (meta-llama) · free": "meta-llama/llama-3.3-70b-instruct:free",
            "Meta: Llama 3.2 3B Instruct (free) (meta-llama) · free": "meta-llama/llama-3.2-3b-instruct:free",
            "Nous: Hermes 3 405B Instruct (free) (nousresearch) · free": "nousresearch/hermes-3-405b:free"
        }

        if mutate_btn:
            if not st.session_state.openrouter_api_key:
                st.error("Cannot mutate prompt: OpenRouter API key must be provided under Advanced Settings.")
            elif not source_prompt.strip():
                st.warning("Please enter a valid Source Prompt first.")
            else:
                target_model_id = model_mapping.get(model_selection, "openrouter/free")
                system_instruction = strategy_system_prompts.get(strategy, "")
                
                # Assemble request
                headers = {
                    "Authorization": f"Bearer {st.session_state.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/streamlit/streamlit",
                    "X-Title": "Parseltongue Mutation Suite"
                }
                
                # Call variants loop
                for var_i in range(int(variants)):
                    st.markdown(f"**Variant #{var_i + 1}**")
                    with st.spinner(f"Mutating variant {var_i + 1}/{int(variants)}..."):
                        payload = {
                            "model": target_model_id,
                            "messages": [
                                {"role": "system", "content": f"{system_instruction} Return ONLY the mutated prompt content. Do not output introduction text, conversational preambles, or analysis."},
                                {"role": "user", "content": f"Source Prompt: {source_prompt}"}
                            ],
                            "temperature": temperature
                        }
                        
                        try:
                            response = requests.post(
                                "https://openrouter.ai/api/v1/chat/completions",
                                json=payload,
                                headers=headers,
                                timeout=45
                            )
                            if response.status_code == 200:
                                res_json = response.json()
                                output_text = res_json['choices'][0]['message']['content'].strip()
                                st.code(output_text, language="text")
                                st.session_state.copy_history.append(output_text)
                            else:
                                st.error(f"API Error ({response.status_code}): {response.text}")
                        except Exception as ex:
                            st.error(f"Network error communicating with OpenRouter: {ex}")
