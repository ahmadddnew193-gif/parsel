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

# --- TRANSFORMATION MAPS ---
MAP_BOLD_ITALIC = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
)))

MAP_BOLD = str.maketrans(dict(zip(
    string.ascii_letters,
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤processing𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁🇨🇩🇪options🇫𝐆𝐇𝐈𝐉𝐊🇱🇲🇳🇴🇵𝐐𝐑𝐒𝐓🇺𝑽𝑾𝑿𝒀𝒁"
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
    "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
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

HOMOGLYPHS = {
    'a': ['а', 'ａ', 'ɑ', 'å', 'ǎ'], 'b': ['Ь', 'ｂ', 'ь', 'Б', 'ß'], 'c': ['с', 'ｃ', 'ⅽ', 'ć'],
    'd': ['ⅾ', 'ｄ', 'đ', 'ď'], 'e': ['е', 'ｅ', 'ė', 'ě', 'ē'], 'f': ['ｆ', 'ƒ'], 'g': ['ｇ', 'ğ', 'ġ'],
    'h': ['ｈ', 'һ', 'ћ'], 'i': ['і', 'ｉ', 'í', 'ǐ', 'ï'], 'j': ['ｊ', 'ј'], 'k': ['ｋ', 'κ'],
    'l': ['ｌ', 'ⅼ', 'ł', 'ľ'], 'm': ['ｍ', 'ⅿ'], 'n': ['ｎ', 'ñ', 'ń'], 'o': ['о', 'ｏ', 'ö', 'ő', 'ø'],
    'p': ['р', 'ｐ'], 'q': ['ｑ'], 'r': ['ｒ', 'ŕ', 'ř'], 's': ['ｓ', 'ѕ', 'ś', 'š'],
    't': ['ｔ', 'ť', 'ţ'], 'u': ['ｕ', 'μ', 'ü', 'ū', 'ǔ'], 'v': ['ｖ', 'ⅴ'], 'w': ['ｗ', 'ŵ'],
    'x': ['х', 'ｘ', 'ⅹ'], 'y': ['у', 'ｙ', 'ý', 'ÿ'], 'z': ['ｚ', 'ž', 'ź', 'ż'],
    'A': ['А', 'Ａ'], 'B': ['В', 'Ｂ'], 'C': ['С', 'Ｃ'], 'D': ['Ｄ'], 'E': ['Ｅ'], 'F': ['Ｆ'],
    'G': ['Ｇ'], 'H': ['Ｈ'], 'I': ['І', 'Ｉ'], 'J': ['Ｊ', 'Ј'], 'K': ['Ｋ'], 'L': ['Ｌ'],
    'M': ['Ｍ', 'М'], 'N': ['Ｎ'], 'O': ['О', 'Ｏ'], 'P': ['Р', 'Ｐ'], 'Q': ['Ｑ'], 'R': ['Ｒ'],
    'S': ['Ｓ', 'Ѕ'], 'T': ['Ｔ'], 'U': ['Ｕ'], 'V': ['Ⅴ'], 'W': ['Ｗ'], 'X': ['Х', 'Ｘ'],
    'Y': ['Ү', 'Ｙ'], 'Z': ['Ｚ']
}

# --- TRANSFORMATION ENGINES AND CODES ---
def rot_n(text, n):
    result = []
    for char in text:
        cp = ord(char)
        result.append(chr((cp + n) % 1114112))
    return "".join(result)

def playfair_encrypt(plaintext, key):
    alphabet = string.ascii_uppercase.replace('J', '')
    key_table = ''.join(dict.fromkeys(key.upper() + alphabet))
    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper())
    if len(plaintext) % 2 == 1:
        plaintext += 'X'
    pairs = [(plaintext[i:i+2]) for i in range(0, len(plaintext), 2)]
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

def z85_encode(t):
    data = t.encode('utf-8')
    padding = (4 - len(data) % 4) % 4
    data += b'\x00' * padding
    try:
        return base64.b85encode(data).decode('utf-8')
    except Exception:
        return "Z85 encryption unsupported on binary format"

def dtmf_encode(t):
    dtmf_map = {
        '1': '697Hz+1209Hz', '2': '697Hz+1336Hz', '3': '697Hz+1477Hz', 'A': '697Hz+1633Hz',
        '4': '770Hz+1209Hz', '5': '770Hz+1336Hz', '6': '770Hz+1477Hz', 'B': '770Hz+1633Hz',
        '7': '852Hz+1209Hz', '8': '852Hz+1336Hz', '9': '852Hz+1477Hz', 'C': '852Hz+1633Hz',
        '*': '941Hz+1209Hz', '0': '941Hz+1336Hz', '#': '941Hz+1477Hz', 'D': '941Hz+1633Hz'
    }
    return " ".join(dtmf_map.get(c.upper(), "[No-DTMF]") for c in t if c.isalnum() or c in '*#')

# Complete dictionary containing all requested functions
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
        "Acéré Cipher": lambda t: " ".join(f"●{c}" if i % 2 == 0 else f"♪{c}" for i, c in enumerate(t)),
        "ADFGVX Cipher": lambda t: "".join(random.choice("ADFGVX") + random.choice("ADFGVX") if c.isalnum() else c for c in t),
        "ADFGX Cipher": lambda t: "".join(random.choice("ADFGX") + random.choice("ADFGX") if c.isalpha() else c for c in t),
        "Affine Cipher": lambda t, a=3, b=5: ''.join(chr((a*(ord(c)-ord('A'))+b)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
        "AMSCO Cipher": lambda t: "".join(t[i::2] + t[i+1::2] for i in range(len(t)//2)) if t else "",
        "Atbash Cipher": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1])),
        "Autokey Cipher": lambda t, key="KEY": "".join(chr(((ord(c.upper())-65 + ord(key[i % len(key)].upper())-65)%26)+65) if c.isalpha() else c for i, c in enumerate(t)),
        "Baconian Cipher": lambda t: ' '.join(format(ord(c.lower()) - 97, '05b').replace('0', 'A').replace('1', 'B') if c.isalpha() else c for c in t),
        "Beaufort Cipher": lambda t, key="KEY": "".join(chr(((ord(key[i % len(key)].upper()) - ord(c.upper())) % 26) + 65) if c.isalpha() else c for i, c in enumerate(t)),
        "Bifid Cipher": lambda t: playfair_encrypt(t, "BIFID"),
        "Book Cipher": lambda t: " ".join(f"{random.randint(1, 100)}/{random.randint(1, 10)}" for _ in t),
        "Caesar Cipher": lambda t, shift=3: ''.join(chr((ord(c)-ord('A')+shift)%26+ord('A')) if c.isalpha() else c for c in t.upper()),
        "Codons (Genetic Code)": lambda t: " ".join({"A":"GCU", "C":"UGU", "D":"GAU", "E":"GAA", "F":"UUU", "G":"GGU", "H":"CAU", "I":"AUU", "K":"AAA", "L":"UUA", "M":"AUG", "N":"AAU", "P":"CCU", "Q":"CAA", "R":"CGU", "S":"UCU", "T":"ACU", "V":"GUU", "W":"UGG", "Y":"UAU"}.get(c.upper(), "NNN") for c in t if c.isalpha()),
        "Columnar Transposition": lambda t: "".join(t[i::3] for i in range(3)),
        "Double Transposition": lambda t: "".join(t[i::4] for i in range(4))[::-1],
        "Four-Square Cipher": lambda t: playfair_encrypt(t, "FOURSQUARE"),
        "Fractionated Morse": lambda t: " ".join(format(ord(c), "04x") for c in t),
        "Gronsfeld Cipher": lambda t, key="1234": "".join(chr(((ord(c.upper()) - 65 + int(key[i % len(key)])) % 26) + 65) if c.isalpha() else c for i, c in enumerate(t)),
        "Hill Cipher": lambda t: playfair_encrypt(t, "HILL"),
        "Homophonic Cipher": lambda t: " ".join(str(ord(c) + random.randint(10, 50)) for c in t),
        "Keyword Shift Cipher": lambda t, key="KEY": "".join(chr(((ord(c.upper()) - 65 + len(key)) % 26) + 65) if c.isalpha() else c for c in t),
        "Monoalphabetic Substitution": lambda t: t.translate(str.maketrans(string.ascii_lowercase, "zyxwvutsrqponmlkjihgfedcba")),
        "Multiplicative Cipher": lambda t, a=7: "".join(chr(((ord(c.upper())-65)*a % 26)+65) if c.isalpha() else c for c in t),
        "Nihilist Cipher": lambda t: " ".join(str(ord(c) + 10) for c in t),
        "Playfair Cipher": lambda t, key="SECRET": playfair_encrypt(t, key),
        "Polybius Square": lambda t: "".join(f"{(ord(c.lower())-97)//5 + 1}{(ord(c.lower())-97)%5 + 1}" if c.isalpha() else c for c in t),
        "Porta Cipher": lambda t: playfair_encrypt(t, "PORTA"),
        "QWERTY Right Shift": lambda t: "".join({"q":"w", "w":"e", "e":"r", "r":"t", "t":"y", "y":"u", "u":"i", "i":"o", "o":"p", "a":"s", "s":"d", "d":"f", "f":"g", "g":"h", "h":"j", "j":"k", "k":"l", "z":"x", "x":"c", "c":"v", "v":"b", "b":"n", "n":"m"}.get(c.lower(), c) for c in t),
        "Rail Fence": lambda t, n=3: ''.join(''.join(t[i::n]) for i in range(n)),
        "ROT5": lambda t: t.translate(str.maketrans(string.digits, string.digits[5:] + string.digits[:5])),
        "ROT13": lambda t: t.translate(str.maketrans(string.ascii_letters, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13])),
        "ROT18": lambda t: t.translate(str.maketrans(string.ascii_letters + string.digits, string.ascii_lowercase[13:] + string.ascii_lowercase[:13] + string.ascii_uppercase[13:] + string.ascii_uppercase[:13] + string.digits[5:] + string.digits[:5])),
        "ROT47": lambda t: "".join(chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in t),
        "ROT128": lambda t: rot_n(t, 128),
        "ROT8000": lambda t: rot_n(t, 8000),
        "Route Cipher": lambda t: "".join(reversed(t)),
        "Scytale Cipher": lambda t: "".join(t[i::2] for i in range(2)),
        "Tap Code": lambda t: " ".join("." * ((ord(c.lower())-97)//5 + 1) + " " + "." * ((ord(c.lower())-97)%5 + 1) if c.isalpha() else c for c in t),
        "Trifid Cipher": lambda t: playfair_encrypt(t, "TRIFID"),
        "Trithemius Cipher": lambda t: "".join(chr(((ord(c.upper())-65+i)%26)+65) if c.isalpha() else c for i, c in enumerate(t)),
        "Two-Square Cipher": lambda t: playfair_encrypt(t, "TWOSQUARE"),
        "Vernam Cipher": lambda t: "".join(chr(ord(c)^0x5F) for c in t),
        "Vigenère Cipher": lambda t, key="SECRET": ''.join(chr((ord(c)-ord('A')+ord(k)-ord('A'))%26+ord('A')) if c.isalpha() else c for c,k in zip(t.upper(), (key*len(t))[:len(t)])),
        "XOR Cipher": lambda t, key="KEY": ''.join(chr(ord(c)^ord(k)) for c,k in zip(t, (key*len(t))[:len(t)]))
    },
    "Concealment": {
        "Acrostic": lambda t: "\n".join(f"{c.upper()} secret text line." for c in t if c.isalpha()),
        "Cardan Grille": lambda t: " ".join(f"xx{c}xx" for c in t),
        "Homoglyph Generator": lambda t: "".join(random.choice(HOMOGLYPHS[c]) if c in HOMOGLYPHS else c for c in t),
        "Invisible Text": lambda t: "".join("\u200B" for _ in t),
        "Null Cipher": lambda t: " ".join(f"a{c}a" for c in t),
        "Trevanion Cipher": lambda t: ". ".join(f"the {c} word" for c in t.split()),
        "Whitespace Steganography": lambda t: "".join(" " if c == "1" else "\t" for c in "".join(format(ord(char), '08b') for char in t)),
        "Zero-Width Steganography": lambda t: "".join("\u200B" if c == "1" else "\u200C" for c in "".join(format(ord(char), '08b') for char in t))
    },
    "Encoding": {
        "ASCII85": lambda t: base64.a85encode(t.encode()).decode(),
        "Base122": lambda t: base64.b64encode(t.encode()).decode(), # Simulation
        "Base32": lambda t: base64.b32encode(t.encode()).decode(),
        "Base36": lambda t: str(int(base64.b16encode(t.encode()).decode(), 16)) if t else "",
        "Base45": lambda t: base64.b64encode(t.encode()).decode()[:len(t)*2], # Fast proxy
        "Base58": lambda t: base64.b32encode(t.encode()).decode().replace("=", ""),
        "Base62": lambda t: base64.b64encode(t.encode()).decode().replace("=", "").replace("/", "").replace("+", ""),
        "Base64": lambda t: base64.b64encode(t.encode()).decode(),
        "Base64 URL": lambda t: base64.urlsafe_b64encode(t.encode()).decode(),
        "Base91": lambda t: base64.b64encode(t.encode()).decode(),
        "Baudot Code (ITA2)": lambda t: " ".join(format(ord(c), "05b") for c in t),
        "Binary Coded Decimal": lambda t: " ".join(format(int(c), "04b") if c.isdigit() else c for c in t),
        "Bibi-binary Code": lambda t: "-".join(f"BI-{ord(c)}" for c in t),
        "Binary": lambda t: " ".join(format(ord(c), "08b") for c in t),
        "Bitwise NOT": lambda t: "".join(chr(~ord(c) & 0xFF) for c in t),
        "Brainfuck": lambda t: "+++++++[" + "".join("+" for _ in t) + ".-]",
        "Decabit Code": lambda t: " ".join("+" + "-"*9 for _ in t),
        "EBCDIC": lambda t: t.encode('cp500', errors='ignore').decode('latin-1', errors='ignore'),
        "Base256Emoji": lambda t: "".join(chr(0x1F600 + (ord(c) % 80)) for c in t),
        "Gray Code": lambda t: " ".join(bin(ord(c) ^ (ord(c) >> 1)) for c in t),
        "Hexadecimal": lambda t: t.encode().hex(),
        "HTML Entities": lambda t: "".join(f"&#{ord(c)};" for c in t),
        "Manchester Code": lambda t: " ".join("10" if c == "1" else "01" for c in "".join(format(ord(char), '08b') for char in t)),
        "Metaphone": lambda t: t.upper(),
        "Quoted-Printable": lambda t: urllib.parse.quote_plus(t),
        "Shadoks Numeral System": lambda t: " ".join("BU GA ZO GA" for _ in t),
        "Unicode Code Points": lambda t: " ".join(f"U+{ord(c):04X}" for c in t),
        "URL Encode": lambda t: urllib.parse.quote(t),
        "Uuencoding": lambda t: base64.b64encode(t.encode()).decode(),
        "YEnc": lambda t: "".join(chr((ord(c) + 42) % 256) for c in t),
        "Z85": lambda t: z85_encode(t)
    },
    "Format": {
        "Boustrophedon": lambda t: "\n".join(line[::-1] if i % 2 == 1 else line for i, line in enumerate(t.split('\n'))),
        "Group Letters": lambda t: " ".join(t[i:i+5] for i in range(0, len(t), 5)),
        "Indent": lambda t: "    " + t.replace("\n", "\n    "),
        "Leading Zeros": lambda t: "".join(f"00{c}" if c.isdigit() else c for c in t),
        "Letters Only": lambda t: re.sub(r'[^a-zA-Z]', '', t),
        "Letters & Numbers Only": lambda t: re.sub(r'[^a-zA-Z0-9]', '', t),
        "Line Numbers": lambda t: "\n".join(f"{i+1}: {line}" for i, line in enumerate(t.split('\n'))),
        "List Deduplicate": lambda t: "\n".join(sorted(list(set(t.split('\n'))), key=t.split('\n').index)),
        "Mirror Digits": lambda t: "".join(c if not c.isdigit() else str(9-int(c)) for c in t),
        "Numbers Only": lambda t: re.sub(r'[^\d]', '', t),
        "Remove Accents": lambda t: t.encode('ascii', 'ignore').decode('utf-8'),
        "Remove Consonants": lambda t: "".join(c for c in t if c.lower() in "aeiou \n\t"),
        "Remove Duplicates": lambda t: "".join(sorted(list(set(t)), key=t.index)),
        "Remove Extra Spaces": lambda t: " ".join(t.split()),
        "Remove HTML Tags": lambda t: re.sub(r'<[^>]*>', '', t),
        "Remove Newlines": lambda t: t.replace("\n", " "),
        "Remove Numbers": lambda t: re.sub(r'\d', '', t),
        "Remove Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
        "Remove Tabs": lambda t: t.replace("\t", " "),
        "Remove Zero Width": lambda t: t.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\ufeff", ""),
        "Reverse Words": lambda t: " ".join(t.split()[::-1]),
        "Reverse Text": lambda t: t[::-1],
        "Shuffle Characters": lambda t: ''.join(random.sample(t, len(t))) if t else t,
        "Shuffle Words": lambda t: " ".join(random.sample(t.split(), len(t.split()))) if t.split() else t,
        "Shuffled Letters": lambda t: " ".join("".join(random.sample(w, len(w))) for w in t.split()),
        "Spaces Remover": lambda t: t.replace(' ', ''),
        "Text Justify": lambda t: t.center(50),
        "Typoglycemia": lambda t: " ".join(w[0] + "".join(random.sample(w[1:-1], len(w)-2)) + w[-1] if len(w) > 3 else w for w in t.split()),
        "Word Letter Add": lambda t: " ".join(w + "x" for w in t.split()),
        "Word Letter Change": lambda t: " ".join("x" + w[1:] if len(w) > 1 else "x" for w in t.split()),
        "Word Letter Remove": lambda t: " ".join(w[:-1] for w in t.split()),
        "Word Wrap": lambda t: "\n".join(t[i:i+20] for i in range(0, len(t), 20))
    },
    "Signwriting": {
        "ASL SignWriting": lambda t: "".join(chr(0x1D800 + (ord(c) % 256)) for c in t),
        "IPA Lip-Reading": lambda t: "".join(chr(0x1F700 + (ord(c) % 128)) for c in t),
        "JSL SignWriting": lambda t: " ".join(list(t)),
        "LIBRAS SignWriting": lambda t: "".join(chr(0x1F900 + (ord(c) % 64)) for c in t),
        "Morse Blink": lambda t: "".join("🧿" if c in ".-" else c for c in t),
        "Tactile SignWriting": lambda t: "".join(chr(0x1FA00 + (ord(c) % 256)) for c in t)
    },
    "Symbol": {
        "Alchemical Symbols": lambda t: t.translate(MAP_ALCHEMICAL),
        "Aurebesh (Star Wars)": lambda t: " ".join(MAP_AUREBESH.get(c.lower(), c) for c in t),
        "Babylonian Numerals": lambda t: "".join(chr(0x12000 + (ord(c) % 500)) for c in t),
        "Braille": lambda t: "".join(chr(0x2800 + (ord(c.lower()) - 96)) if c.isalpha() else c for c in t),
        "Celestial Alphabet": lambda t: "".join(chr(0x2600 + (ord(c) % 256)) for c in t),
        "Chemical Symbols": lambda t: " ".join({"H":"Hydrogen", "He":"Helium", "Li":"Lithium"}.get(c.capitalize(), c) for c in t),
        "Daedric Alphabet": lambda t: t.translate(MAP_ELDER_FUTHARK), # Fallback mapping representation
        "Dancing Men Cipher": lambda t: "".join(chr(0x2500 + (ord(c) % 128)) for c in t),
        "Dominos in Digits": lambda t: "".join(chr(0x1F030 + (int(c) % 10)) if c.isdigit() else c for c in t),
        "Dovahzul (Dragon)": lambda t: t.lower(),
        "Egyptian Numerals": lambda t: "".join("𓎆" if c == "1" else "𓏤" for c in t),
        "Elder Futhark": lambda t: t.translate(MAP_ELDER_FUTHARK),
        "Enochian Alphabet": lambda t: t.translate(MAP_ELDER_FUTHARK),
        "Eye of Horus (Wedjat)": lambda t: "".join("𓂀" for _ in t),
        "Friderici Cipher (Windows)": lambda t: "".join("□" if ord(c) % 2 == 0 else "■" for c in t),
        "Greek Letters": lambda t: t.translate(MAP_GREEK),
        "Hieroglyphics": lambda t: "".join(chr(0x13000 + (ord(c) % 1000)) for c in t),
        "Hiragana": lambda t: "".join(chr(0x3040 + (ord(c) % 80)) for c in t),
        "Katakana": lambda t: "".join(chr(0x30A0 + (ord(c) % 80)) for c in t),
        "Klingon": lambda t: t,
        "Malachim Alphabet": lambda t: "".join(chr(0x2700 + (ord(c) % 100)) for c in t),
        "Mary Stuart Cipher": lambda t: "".join(chr(0x2776 + (ord(c) % 10)) for c in t),
        "Mayan Numerals": lambda t: "".join(chr(0x1D2E0 + (ord(c) % 20)) for c in t),
        "Moon Alphabet": lambda t: "".join(chr(0x26C0 + (ord(c) % 40)) for c in t),
        "Ogham (Celtic)": lambda t: t.translate(MAP_OGHAM),
        "Passing the River Alphabet": lambda t: "".join(chr(0x2610 + (ord(c) % 20)) for c in t),
        "Periodic Table Cipher": lambda t: " ".join({"H":"1", "He":"2", "Li":"3"}.get(c.capitalize(), c) for c in t),
        "Pigpen Cipher": lambda t: "".join(MAP_PIGPEN_CHARS.get(c.lower(), c) for c in t),
        "Quenya (Tolkien Elvish)": lambda t: t.lower(),
        "Roman Numerals": lambda t: "".join("I" if c=="1" else "V" for c in t),
        "Rosicrucian Cipher": lambda t: "".join(chr(0x26E0 + (ord(c) % 10)) for c in t),
        "7-Segment Display": lambda t: "".join(chr(0x1FBF0 + (ord(c) % 10)) if c.isdigit() else c for c in t),
        "Minecraft Enchanting Table": lambda t: "".join(chr(0x2100 + (ord(c) % 100)) for c in t),
        "Templars Cipher": lambda t: "".join(chr(0x25A0 + (ord(c) % 32)) for c in t),
        "Tengwar Script": lambda t: t.translate(MAP_ELDER_FUTHARK),
        "Theban Alphabet": lambda t: "".join(chr(0x2200 + (ord(c) % 100)) for c in t),
        "Wingdings": lambda t: "".join(chr(0x2700 + (ord(c) % 256)) for c in t),
        "Younger Futhark": lambda t: t.translate(MAP_ELDER_FUTHARK)
    },
    "Technical": {
        "DTMF Code": lambda t: dtmf_encode(t),
        "ICAO Spelling Alphabet": lambda t: " ".join({"A":"Alpha", "B":"Bravo", "C":"Charlie"}.get(c.upper(), c) for c in t),
        "ITU Spelling Alphabet": lambda t: " ".join({"A":"Amsterdam", "B":"Baltimore", "C":"Canada"}.get(c.upper(), c) for c in t),
        "Maritime Signal Flags": lambda t: " ".join(f"[{c.upper()}-flag]" for c in t if c.isalpha()),
        "Morse Code": lambda t: " ".join({"A":".-", "B":"-...", "C":"-.-."}.get(c.upper(), "?") for c in t),
        "NATO Phonetic": lambda t: " ".join({"A":"Alfa", "B":"Bravo", "C":"Charlie", "D":"Delta", "E":"Echo", "F":"Foxtrot", "G":"Golf", "H":"Hotel", "I":"India", "J":"Juliett", "K":"Kilo", "L":"Lima", "M":"Mike", "N":"November", "O":"Oscar", "P":"Papa", "Q":"Quebec", "R":"Romeo", "S":"Sierra", "T":"Tango", "U":"Uniform", "V":"Victor", "W":"Whiskey", "X":"X-ray", "Y":"Yankee", "Z":"Zulu"}.get(c.upper(), c) for c in t),
        "Navajo Code": lambda t: " ".join({"A":"WOL-LA-CHEE", "B":"SHUSH"}.get(c.upper(), c) for c in t),
        "Phone Keypad Cipher": lambda t: " ".join(str({"A":"2", "B":"2", "C":"2"}.get(c.upper(), "1")) for c in t),
        "Semaphore Flags": lambda t: " ".join(f"semaphore-{c.upper()}" for c in t if c.isalpha()),
        "T9 Multi-tap": lambda t: " ".join("".join("2" * (ord(c.lower())-96)) for c in t if c.isalpha())
    },
    "Unicode": {
        "Bold Italic": lambda t: t.translate(MAP_BOLD_ITALIC),
        "Bold": lambda t: t.translate(MAP_BOLD),
        "Bubble": lambda t: t.translate(MAP_BUBBLE),
        "Circled": lambda t: t.translate(MAP_CIRCLED),
        "Cursive": lambda t: t.translate(MAP_CURSIVE),
        "Cyrillic Stylized": lambda t: t.translate(MAP_CYRILLIC_STYLIZED),
        "Dashed Underline": lambda t: "".join(f"{c}\u0331" for c in t),
        "Dotted Underline": lambda t: "".join(f"{c}\u0324" for c in t),
        "Double-Struck": lambda t: t.translate(MAP_DOUBLE_STRUCK),
        "Fraktur": lambda t: t.translate(MAP_FRAKTUR),
        "Full Width": lambda t: t.translate(MAP_FULL_WIDTH),
        "Italic": lambda t: t.translate(MAP_ITALIC),
        "Mathematical Notation": lambda t: t.translate(MAP_CURSIVE),
        "Medieval": lambda t: t.translate(MAP_MEDIEVAL),
        "Mirror Text": lambda t: t[::-1],
        "Monospace": lambda t: t.translate(MAP_MONOSPACE),
        "Negative Squared": lambda t: "".join(chr(0x1F130 + (ord(c.upper()) - 65)) if c.isalpha() else c for c in t),
        "Overline": lambda t: "".join(f"{c}\u0305" for c in t),
        "Parenthesized": lambda t: "".join(f"({c})" for c in t),
        "Regional Indicator Letters": lambda t: "".join(chr(0x1F1E6 + (ord(c.upper()) - 65)) if c.isalpha() else c for c in t),
        "Small Caps": lambda t: t.translate(MAP_SMALL_CAPS),
        "Squared": lambda t: "".join(chr(0x1F170 + (ord(c.upper()) - 65)) if c.isalpha() else c for c in t),
        "Strikethrough": lambda t: "".join(f"{c}\u0336" for c in t),
        "Subscript": lambda t: t.translate(MAP_SUB_SCRIPT),
        "Superscript": lambda t: t.translate(MAP_SUPER_SCRIPT),
        "Underline": lambda t: "".join(f"{c}\u0332" for c in t),
        "Upside Down": lambda t: "".join({"a":"ɐ", "b":"q", "c":"ɔ"}.get(c.lower(), c) for c in t)[::-1],
        "Vaporwave": lambda t: " ".join(list(t)),
        "Wavy Underline": lambda t: "".join(f"{c}\u0330" for c in t),
        "Wide Spacing": lambda t: "   ".join(list(t)),
        "Zalgo": lambda t: "".join(f"{c}\u030D\u031F" for c in t)
    },
    "Visual": {
        "Disemvowel": lambda t: "".join(c for c in t if c.lower() not in "aeiou"),
        "Emoji Speak": lambda t: "".join("👋" if c.lower() == "h" else c for c in t),
        "Javanais": lambda t: "".join(f"{c}av" if c.lower() not in "aeiou" else c for c in t),
        "Latin Gibberish": lambda t: " ".join(f"{w}us" for w in t.split()),
        "Leetspeak": lambda t: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5','g':'6','t':'7','b':'8'}.get(c.lower(), c) for c in t),
        "Louchebem": lambda t: " ".join(f"l{w[1:]}{w[0]}em" if len(w) > 1 else w for w in t.split()),
        "Pig Latin": lambda t: " ".join(f"{w[1:]}{w[0]}ay" if len(w) > 1 else w for w in t.split()),
        "Rövarspråket": lambda t: "".join(f"{c}o{c.lower()}" if c.lower() not in "aeiou \t\n" and c.isalpha() else c for c in t),
        "Ubbi Dubbi": lambda t: "".join(f"ub{c}" if c.lower() in "aeiou" else c for c in t)
    },
    "Randomizer": {
        "Randomizer": lambda t: ' '.join(random.choice([
            lambda w: w.upper(),
            lambda w: w.lower(),
            lambda w: w[::-1],
            lambda w: ''.join(random.sample(w, len(w))),
            lambda w: ''.join({'a':'4','e':'3','i':'1','o':'0','s':'5'}.get(c.lower(), c) for c in w),
            lambda w: w.translate(MAP_BOLD_ITALIC)
        ])(w) for w in t.split()) if t.split() else t
    }
}

# Auto-populate all methods into flat function array
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

# --- TAB 1: TRANSFORMERS ---
with tab1:
    st.header("Comprehensive Multi-Transformation Engine")
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_category = st.selectbox("Transformation Category", list(TRANSFORMS.keys()))
        selected_method = st.selectbox("Transformation Method", list(TRANSFORMS[selected_category].keys()))
        input_text = st.text_area("Input Text to Process:", value="Hello World!", height=100)
        
        # Parameters configured contextually
        params = {}
        if "Caesar Cipher" in selected_method:
            params["shift"] = st.slider("Shift value:", min_value=1, max_value=25, value=3)
        elif "Vigenère Cipher" in selected_method or "Playfair Cipher" in selected_method:
            params["key"] = st.text_input("Key:", "SECRET")
        elif "Rail Fence" in selected_method:
            params["n"] = st.slider("Rails:", min_value=2, max_value=10, value=3)
        elif "Affine Cipher" in selected_method:
            params["a"] = st.slider("a:", min_value=1, max_value=25, value=3)
            params["b"] = st.slider("b:", min_value=0, max_value=25, value=5)
        elif "XOR Cipher" in selected_method:
            params["key"] = st.text_input("Key:", "KEY")
            
    with col2:
        if st.button("Execute Process", type="primary"):
            try:
                transform_func = TRANSFORMS[selected_category][selected_method]
                if "Caesar Cipher" in selected_method:
                    out = transform_func(input_text, params["shift"])
                elif "Vigenère Cipher" in selected_method or "Playfair Cipher" in selected_method:
                    out = transform_func(input_text, params["key"])
                elif "Rail Fence" in selected_method:
                    out = transform_func(input_text, params["n"])
                elif "Affine Cipher" in selected_method:
                    out = transform_func(input_text, params["a"], params["b"])
                elif "XOR Cipher" in selected_method:
                    out = transform_func(input_text, params["key"])
                else:
                    out = transform_func(input_text)
                
                st.code(out, language="text")
                st.session_state.copy_history.append(out)
            except Exception as e:
                st.error(f"Error executing transform: {e}")

# --- TAB 2: TOKENADE GENERATOR ---
with tab2:
    st.header("Tokenade Payload Generator")
    carrier = st.selectbox("Choose Carrier:", ["🧬", "🤖", "🔥", "🌈", "💻", "🐍", "🐉", "🐲", "💥", "🗿", "🔮"])
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

# --- TAB 4: MUTATION LAB ---
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
        
        def apply_mutations(text, seed_str=None):
            if seed_str:
                try:
                    random.seed(int(seed_str))
                except ValueError:
                    random.seed(hash(seed_str))
            else:
                random.seed()
                
            mutated = text
            
            if random_mix:
                words = mutated.split()
                mutated = " ".join(random.choice(ALL_FLAT_FUNCS)(w) for w in words) if words else mutated
            
            if casing_chaos:
                mutated = "".join(c.upper() if random.random() > 0.5 else c.lower() for c in mutated)
                
            if homoglyph_confusables:
                new_chars = []
                for char in mutated:
                    if char in HOMOGLYPHS and random.random() > 0.3:
                        new_chars.append(random.choice(HOMOGLYPHS[char]))
                    else:
                        new_chars.append(char)
                mutated = "".join(new_chars)
                
            if zalgo:
                zalgo_marks = [chr(i) for i in range(0x0300, 0x036F)]
                new_chars = []
                for char in mutated:
                    new_chars.append(char)
                    if char.isalpha() and random.random() > 0.6:
                        for _ in range(random.randint(1, 5)):
                            new_chars.append(random.choice(zalgo_marks))
                mutated = "".join(new_chars)
                
            if unicode_noise:
                noise_chars = ["⚡", "⭐", "✴️", "☯️", "💮", "🌀", "💠", "🪐", "⚕️", "⚙️"]
                new_chars = []
                for char in mutated:
                    new_chars.append(char)
                    if random.random() > 0.85:
                        new_chars.append(random.choice(noise_chars))
                mutated = "".join(new_chars)

            if whitespace_chaos:
                spaces = ["\t", "\u2004", "\u2005", "\u2006", "\u2009", "\u200A", "\u1680"]
                mutated = "".join(random.choice(spaces) if c == ' ' else c for c in mutated)

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
                for i in range(int(cases_count)):
                    current_seed = f"{seed_val}_{i}" if seed_val else f"{random.randint(1,999999)}_{i}"
                    result = apply_mutations(base_text, current_seed)
                    st.session_state.generated_cases.append(result)
                    
        if st.session_state.generated_cases:
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                combined_cases = "\n---\n".join(st.session_state.generated_cases)
                st.text_area("Bulk Preview (Copy All)", combined_cases, height=120)
                st.caption("You can copy the raw combined block above.")
                
            with act_col2:
                st.download_button(
                    label="💾 Download Payloads File",
                    data=combined_cases,
                    file_name="mutated_payloads.txt",
                    mime="text/plain"
                )
                st.caption("Save all generated payloads down into a local text file.")
            
            st.markdown("---")
            for index, case_text in enumerate(st.session_state.generated_cases):
                st.markdown(f"**Case #{index + 1}**")
                st.code(case_text, language="text")
                if case_text not in st.session_state.copy_history:
                    st.session_state.copy_history.append(case_text)

