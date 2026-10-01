import streamlit as st

st.set_page_config(page_title="CYBR 470: Cryptography - Lab Exercise 01: Classical Ciphers", layout="wide")
st.title("CYBR 470: Cryptography \n Lab Exercise 01: Classical Ciphers")

# -------------------------------------------------------------
# CORE ALGORITHMS
# -------------------------------------------------------------

def build_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)
    for i in range(26):
        char = chr(ord('A') + i)
        if char != 'J' and char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_playfair_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None

def playfair_encrypt(text, key):
    matrix = build_playfair_matrix(key)
    # Filter text and substitute J with I
    text = "".join([c for c in text if c.isalpha()]).upper().replace('J', 'I')
    
    # Process text into bigrams with filler rules
    prepared_chars = []
    i = 0
    while i < len(text):
        prepared_chars.append(text[i])
        if i + 1 < len(text):
            if text[i] == text[i+1]:
                prepared_chars.append('X')
                i += 1
            else:
                prepared_chars.append(text[i+1])
                i += 2
        else:
            prepared_chars.append('X')
            i += 1

    ciphertext = ""
    for idx in range(0, len(prepared_chars), 2):
        b1, b2 = prepared_chars[idx], prepared_chars[idx+1]
        r1, c1 = find_playfair_position(matrix, b1)
        r2, c2 = find_playfair_position(matrix, b2)
        
        if r1 == r2:  # Same row
            ciphertext += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:  # Same column
            ciphertext += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
        else:  # Rectangle
            ciphertext += matrix[r1][c2] + matrix[r2][c1]
            
    return ciphertext

def rail_fence_encrypt(text, depth):
    text = "".join([c for c in text if c.isalpha()]).upper()
    if depth <= 1 or not text:
        return text
    
    # Initialize grid paths
    rows = [[] for _ in range(depth)]
    rail = 0
    direction = 1
    
    for char in text:
        rows[rail].append(char)
        rail += direction
        if rail == depth - 1 or rail == 0:
            direction *= -1
            
    return "".join(["".join(r) for r in rows])

def row_transposition_encrypt(text, key_str):
    text = "".join([c for c in text if c.isalpha()]).upper()
    # Key expected as string of digits like '4312567' (1-indexed base)
    key = [int(x) for x in key_str]
    num_cols = len(key)
    
    # Pad to make perfect rectangle matrix
    while len(text) % num_cols != 0:
        text += "X"
        
    num_rows = len(text) // num_cols
    grid = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
    
    ciphertext = ""
    # Read columns sequentially based on sorted order value of the key digits
    # e.g., if key has 1 at index 2, read index 2 column first.
    for target_col in range(1, num_cols + 1):
        col_idx = key.index(target_col)
        for r in range(num_rows):
            ciphertext += grid[r][col_idx]
            
    return ciphertext

def vigenere_autokey_encrypt(text, key):
    text = "".join([c for c in text if c.isalpha()]).upper()
    key = key.upper()
    if not text or not key:
        return ""
        
    # Standard Autokey Keystream: Keyword string followed by plaintext string
    keystream = key + text
    ciphertext = []
    
    for i, char in enumerate(text):
        shift = ord(keystream[i]) - ord('A')
        c_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        ciphertext.append(c_char)
        
    return "".join(ciphertext)

# -------------------------------------------------------------
# USER INTERFACE TABS
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Challenge 1: Playfair Geometry Map", 
    "Challenge 2: Rail Fence Zig-Zag Depth", 
    "Challenge 3: Row Transposition Key Matrix", 
    "Challenge 4: Vigenère Autokey Key Stream"
])

with tab1:
    st.subheader("Challenge 1: Playfair Geometry Map")
    p_id = st.selectbox("Select Challenge ID:", ["P1", "P2", "P3", "P4", "P5"], key="p_sel")
    user_text_p = st.text_input("Plaintext:", value="EXAMPLE", key="p_in")
    
    if user_text_p:
        try:
            res_p = playfair_encrypt(user_text_p, st.secrets[f"{p_id}_KEY"])
            st.write(f"Ciphertext: `{res_p}`")
        except Exception:
            st.error("Configuration Error.")

with tab2:
    st.subheader("Challenge 2: Rail Fence Zig-Zag Depth")
    r_id = st.selectbox("Select Challenge ID:", ["R1", "R2", "R3", "R4", "R5"], key="r_sel")
    user_text_r = st.text_input("Plaintext:", value="CRYPTOGRAPHYLABTEST", key="r_in")
    
    if user_text_r:
        try:
            res_r = rail_fence_encrypt(user_text_r, int(st.secrets[f"{r_id}_DEPTH"]))
            st.write(f"Ciphertext: `{res_r}`")
        except Exception:
            st.error("Configuration Error.")

with tab3:
    st.subheader("Challenge 3: Row Transposition Key Matrix")
    t_id = st.selectbox("Select Challenge ID:", ["T1", "T2", "T3", "T4", "T5"], key="t_sel")
    user_text_t = st.text_input("Plaintext (Exactly 28 alphabetic characters required):", 
                                value="CYBR", max_chars=28, key="t_in")
    
    clean_t = "".join([c for c in user_text_t if c.isalpha()])
    if len(clean_t) == 28:
        try:
            res_t = row_transposition_encrypt(clean_t, st.secrets[f"{t_id}_KEY"])
            st.write(f"Ciphertext: `{res_t}`")
        except Exception:
            st.error("Configuration Error.")
    else:
        st.write("Input string must be exactly 28 letters long.")

with tab4:
    st.subheader("Challenge 4: Vigenère Autokey Key Stream")
    v_id = st.selectbox("Select Challenge ID:", ["V1", "V2", "V3", "V4", "V5"], key="v_sel")
    user_text_v = st.text_input("Plaintext:", value="EXAMPLLAB", key="v_in")
    
    if user_text_v:
        try:
            res_v = vigenere_autokey_encrypt(user_text_v, st.secrets[f"{v_id}_KEY"])
            st.write(f"Ciphertext: `{res_v}`")
        except Exception:
            st.error("Configuration Error.")
