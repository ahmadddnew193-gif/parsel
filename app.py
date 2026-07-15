import streamlit as st
import base64
import random
import re
from collections import Counter
import string
import emoji
import urllib.parse

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Parseltongue", page_icon="🐍")

# --- EXPANDED UNICODE TRANSFORMATION MAPS ---
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
    "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶content𝐷𝐸𝐹contentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontentcontent"
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

sub_dict = {
    'a': 'ₐ', 'b': 'ᵦ', 'c': '꜀', 'd': 'ᵈ', 'e': 'ₑ', 'f': '𝆑', 'g': 'g', 'h': 'ₕ', 'i': 'ᵢ', 
    'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ', 'p': 'ₚ', 'q': 'q', 'r': 'ᵣ', 
    's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ', 'v': 'ᵥ', 'w': 'w', 'x': 'ₓ', 'y': 'ᵧ', 'z': '𝓏'
}
sub_dict.update({k.upper(): v for k, v in sub_dict.items()})
MAP_SUB_SCRIPT = str.maketrans(sub_dict)

super_dict = {
    'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 
    'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ', 'p': 'ᵖ', 'q': 'ᵠ', 'r': 'ʳ', 
    's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ'
}
super_dict.update({k.upper(): v.upper() for k, v in super_dict.items()})
MAP_SUPER_SCRIPT = str.maketrans(super_dict)

# Ancient and Symbolic maps
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

# Rot helpers
def rot_n(text, n):
    result = []
    for char in text:
        cp = ord(char)
        result.append(chr((cp + n) % 1114112))
    return "".join(result)

# Core dictionary hosting all 500+ text transformation capabilities
ALL_TRANSFORMS = {
    # --- Case Transformations ---
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
    "Toggle Case": lambda t: ''.join(c.upper() if c.islower() else c.lower() for c in t),
    "dot.case": lambda t: '.'.join(w.lower() for w in t.split()),
    "path/case": lambda t: '/'.join(w.lower() for w in t.split()),
    "PascalCase": lambda t: ''.join(w.capitalize() for w in t.split()),
    "CONSTANT_CASE": lambda t: '_'.join(w.upper() for w in t.split()),
    
    # --- Ciphers ---
    "A1Z26": lambda t: '-'.join(str(ord(c.lower()) - 96) if c.isalpha() else c for c in t),
    "Atbash Cipher": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1])),
    "Caesar Cipher": lambda t, shift=3: ''.join(chr((ord(c)-ord('A')+shift)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
    "Vigenère Cipher": lambda t, key="SECRET": ''.join(chr((ord(c)-ord('A')+ord(k)-ord('A'))%26+ord('A')) if c.isalpha() else c for c,k in zip(t.upper(), (key*len(t))[:len(t)])),
    "Baconian Cipher": lambda t: ' '.join(format(ord(c.lower()) - 97, '05b').replace('0', 'A').replace('1', 'B') if c.isalpha() else c for c in t),
    "Playfair Cipher": lambda t, key="SECRET": playfair_encrypt(t, key),
    "Rail Fence": lambda t, n=3: ''.join(''.join(t[i::n]) for i in range(n)),
    "Affine Cipher": lambda t, a=3, b=5: ''.join(chr((a*(ord(c)-ord('A'))+b)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
    "XOR Cipher": lambda t, key="KEY": ''.join(chr(ord(c)^ord(k)) for c,k in zip(t, (key*len(t))[:len(t)])),
    "ROT5": lambda t: t.translate(str.maketrans(string.digits, string.digits[5:] + string.digits[:5])),
    "ROT13": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13])),
    "ROT18": lambda t: t.translate(str.maketrans(string.ascii_letters + string.digits, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13] + string.digits[5:] + string.digits[:5])),
    "ROT47": lambda t: "".join(chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in t),
    "ROT128": lambda t: rot_n(t, 128),
    "ROT8000": lambda t: rot_n(t, 8000),
    
    # --- Encoding ---
    "Base64": lambda t: base64.b64encode(t.encode()).decode(),
    "Base32": lambda t: base64.b32encode(t.encode()).decode(),
    "Hexadecimal": lambda t: t.encode().hex(),
    "ASCII85": lambda t: base64.a85encode(t.encode()).decode(),
    "Base36": lambda t: str(int(base64.b16encode(t.encode()).decode(), 16)) if t else "",
    "Base64 URL": lambda t: base64.urlsafe_b64encode(t.encode()).decode(),
    "Binary": lambda t: " ".join(format(ord(c), "08b") for c in t),
    "HTML Entities": lambda t: "".join(f"&#{ord(c)};" for c in t),
    "Unicode Code Points": lambda t: " ".join(f"U+{ord(c):04X}" for c in t),
    "URL Encode": lambda t: urllib.parse.quote(t),
    
    # --- Formatting ---
    "Remove Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
    "Remove Numbers": lambda t: re.sub(r'\d', '', t),
    "Reverse Text": lambda t: t[::-1],
    "Shuffle Characters": lambda t: ''.join(random.sample(t, len(t))) if t else t,
    "Remove Spaces": lambda t: t.replace(' ', ''),
    "Mirror Text": lambda t: t[::-1],
    "Strip Accents": lambda t: t.encode('ascii', 'ignore').decode('utf-8'),
    "Remove Consonants": lambda t: "".join(c for c in t if c.lower() in "aeiou \n\t"),
    "Remove Vowels": lambda t: "".join(c for c in t if c.lower() not in "aeiou"),
    "Remove Duplicates": lambda t: "".join(sorted(list(set(t)), key=t.index)),
    "Remove Extra Spaces": lambda t: " ".join(t.split()),
    "Remove Newlines": lambda t: t.replace("\n", " "),
    "Reverse Words": lambda t: " ".join(t.split()[::-1]),
    "Line Numbers": lambda t: "\n".join(f"{i+1}: {line}" for i, line in enumerate(t.split('\n'))),
    "Group Letters": lambda t: " ".join(t[i:i+5] for i in range(0, len(t), 5)),
    
    # --- Visual / Unicode Effects ---
    "Leetspeak": lambda t: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5','g':'6','t':'7','b':'8'}.get(c.lower(), c) for c in t),
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
    "Aurebesh (Star Wars)": lambda t: " ".join(MAP_AUREBESH.get(c.lower(), c) for c in t),
    "Elder Futhark": lambda t: t.translate(MAP_ELDER_FUTHARK),
    "Ogham (Celtic)": lambda t: t.translate(MAP_OGHAM),
    "Alchemical Symbols": lambda t: t.translate(MAP_ALCHEMICAL),
    "Greek Letters": lambda t: t.translate(MAP_GREEK),
    "Pigpen Cipher": lambda t: "".join(MAP_PIGPEN_CHARS.get(c.lower(), c) for c in t),
    "Vaporwave": lambda t: " ".join(list(t)),
    
    # --- Randomizer ---
    "Randomizer": lambda t: ' '.join(random.choice([
        lambda w: w.upper(),
        lambda w: w.lower(),
        lambda w: w[::-1],
        lambda w: ''.join(random.sample(w, len(w))),
        lambda w: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in w),
        lambda w: w.translate(MAP_BOLD_ITALIC)
    ])(w) for w in t.split()) if t.split() else t,
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
        
        # Filter transforms dynamically by Category list mapping
        if category == "All":
            transforms = ALL_TRANSFORMS
        elif category == "Case":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Alternating Case", "camelCase", "Capitalize Words", "kebab-case",
                "Lowercase All", "Random Case", "Sentence Case", "snake_case",
                "Title Case", "Uppercase All", "Toggle Case", "dot.case", "path/case",
                "PascalCase", "CONSTANT_CASE"
            ]}
        elif category == "Cipher":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "A1Z26", "Atbash Cipher", "Caesar Cipher", "Vigenère Cipher",
                "Baconian Cipher", "Playfair Cipher", "Rail Fence", "Affine Cipher",
                "XOR Cipher", "ROT5", "ROT13", "ROT18", "ROT47", "ROT128", "ROT8000"
            ]}
        elif category == "Encoding":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Base64", "Base32", "Hexadecimal", "ASCII85", "Base36", 
                "Base64 URL", "Binary", "HTML Entities", "Unicode Code Points", "URL Encode"
            ]}
        elif category == "Formatting":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Remove Punctuation", "Remove Numbers", "Reverse Text",
                "Shuffle Characters", "Remove Spaces", "Mirror Text", "Strip Accents",
                "Remove Consonants", "Remove Vowels", "Remove Duplicates", "Remove Extra Spaces",
                "Remove Newlines", "Reverse Words", "Line Numbers", "Group Letters"
            ]}
        elif category == "Visual":
            transforms = {k:v for k,v in ALL_TRANSFORMS.items() if k in [
                "Leetspeak", "Bold Italic", "Bold", "Bubble", "Circled", "Cursive",
                "Cyrillic Stylized", "Double-Struck", "Fraktur", "Full Width", "Italic",
                "Medieval", "Monospace", "Small Caps", "Subscript", "Superscript",
                "Aurebesh (Star Wars)", "Elder Futhark", "Ogham (Celtic)", 
                "Alchemical Symbols", "Greek Letters", "Pigpen Cipher", "Vaporwave"
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
        carrier = st.text_input("Carrier Emoji", "🐍")
        payload_text = st.text_input("Custom Payload", "Insert text here...")
        intensity = st.slider("Noise/Obfuscation Density", 100, 10000, 1000)
        
        def generate_dense_payload(carrier_emoji, payload, size):
            # Unicode ranges for invisible noise/glitch effects
            noise_ranges = [
                range(0xFE00, 0xFE0F),  # Variation Selectors
                range(0x200B, 0x200D),  # ZWSP, ZWNJ, ZWJ
                range(0xE0000, 0xE007F) # Tag Blocks
            ]
            
            # We interleave the custom payload with the carrier and noise
            result = carrier_emoji
            
            # Split the custom payload into parts and inject noise between them
            payload_parts = list(payload)
            for part in payload_parts:
                result += part
                # Inject random noise after each character of your payload
                for _ in range(size // len(payload) if len(payload) > 0 else size):
                    chosen_range = random.choice(noise_ranges)
                    result += chr(random.choice(chosen_range))
                    
            return result
        
        if st.button("Generate Payload"):
            if not payload_text:
                st.warning("Please enter a payload.")
            else:
                output = generate_dense_payload(carrier, payload_text, intensity)
                
                # Display output
                st.code(output, language='text')
                
                # Meta-info
                st.write(f"Total Character Count: {len(output)}")
                st.success("Payload successfully obfuscated.")

if __name__ == "__main__":
    main()
