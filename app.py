import streamlit as st

st.set_page_config(page_title="Crypto Lab Oracle", layout="wide")
st.title("🕵️‍♂️ Cryptography Lab Oracle")
st.write("Select your assigned Challenge ID inside each tab to interact with the hidden cryptographic systems.")

# -------------------------------------------------------------
# HELPER FUNCTIONS FOR CORE ALGORITHMS
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

def playfair_encrypt_bigram(matrix, b1, b2):
    r1, c1 = find_playfair_position(matrix, b1)
    r2, c2 = find_playfair_position(matrix, b2)
    
    if r1 == r2:  # Same row
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:  # Same column
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:  # Rectangle swap
        return matrix[r1][c2] + matrix[r2][c1]

def rail_fence_encrypt(text, depth):
    text = "".join([c for c in text if c.isalpha()]).upper()
    if depth <= 1 or not text:
        return text
    fence = [[] for _ in range(depth)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == depth - 1 or rail == 0:
            direction *= -1
    return "".join(["".join(row) for row in fence])

def row_transposition_encrypt(text, key_str):
    text = "".join([c for c in text if c.isalpha()]).upper()
    key = [int(x) for x in key_str]
    num_cols = len(key)
    
    # Pad text to exact multiple of key length
    while len(text) % num_cols != 0:
        text += "X"
        
    num_rows = len(text) // num_cols
    grid = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
    
    # Sort columns by key indices
    key_with_indices = sorted(list(enumerate(key)), key=lambda x: x[1])
    
    ciphertext = ""
    for col_idx, _ in key_with_indices:
        for r in range(num_rows):
            ciphertext += grid[r][col_idx]
    return ciphertext

def vigenere_autokey_encrypt(text, key):
    text = "".join([c for c in text if c.isalpha()]).upper()
    key = key.upper()
    if not text:
        return ""
        
    # Build complete key stream by appending plaintext to keyword
    keystream = key + text
    ciphertext = []
    
    for i, char in enumerate(text):
        shift = ord(keystream[i]) - ord('A')
        cipher_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        ciphertext.append(cipher_char)
        
    return "".join(ciphertext)

# -------------------------------------------------------------
# MAIN MULTI-CHALLENGE NAVIGATION UI
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Challenge 2: Playfair Geometry", 
    "Challenge 3: Rail Fence Depth", 
    "Challenge 4: Row Transposition Grid", 
    "Challenge 5: Vigenère Autokey Loop"
])

# --- CHALLENGE 2: PLAYFAIR CIPHER ---
with tab1:
    st.header("Challenge 2: Playfair Geometry Map")
    st.info("💡 **Canvas Task:** Input 2-letter combos to calculate row indices or find keyword lengths.")
    
    p_id = st.selectbox("Select assigned Challenge ID:", ["P1", "P2", "P3", "P4", "P5"], key="p_sel")
    
    try:
        secret_p_key = st.secrets[f"{p_id}_KEY"]
        matrix = build_playfair_matrix(secret_p_key)
        
        user_bigram = st.text_input("Enter a 2-Letter Plaintext Bigram:", max_chars=2, value="TH", key="p_in").upper().replace('J', 'I')
        
        if len(user_bigram) == 2:
            if not user_bigram.isalpha():
                st.warning("⚠️ Bigram must contain letters only.")
            elif user_bigram[0] == user_bigram[1]:
                st.warning("⚠️ Playfair treats double identical letters using an 'X' filler (e.g., 'LX'). Try unique letter pairs.")
            else:
                cipher_out = playfair_encrypt_bigram(matrix, user_bigram[0], user_bigram[1])
                st.success(f"**Ciphertext Output:** `{cipher_out}`")
                
                # Hidden reference value check block for the teacher
                # Find where 'E' is for debugging or variable validation tasks
                e_r, e_c = find_playfair_position(matrix, 'E')
                st.caption(f"Educational Grid Identity Status: Matrix Active.")
        else:
            st.warning("Please type exactly 2 characters.")
    except Exception:
        st.error("Missing configuration secrets in Streamlit Dashboard.")

# --- CHALLENGE 3: RAIL FENCE ---
with tab3:
    st.header("Challenge 3: Shuffling Depth (Rail Fence)")
    st.info("💡 **Canvas Task:** Analyze how letter distributions branch out across depths to solve for integer 'd'.")
    
    r_id = st.selectbox("Select assigned Challenge ID:", ["R1", "R2", "R3", "R4", "R5"], key="r_sel")
    
    try:
        secret_r_depth = int(st.secrets[f"{r_id}_DEPTH"])
        
        # Fixed benchmark phrase to maintain standardized structural alignment
        sample_phrase = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        st.text_area("Standard Benchmark Text provided to all students:", sample_phrase, disabled=True)
        
        user_text_r = st.text_input("Or customize your own dynamic plaintext message here:", value="CRYPTOGRAPHYLABTEST", key="r_in")
        
        if user_text_r:
            cipher_out_r = rail_fence_encrypt(user_text_r, secret_r_depth)
            st.success(f"**Ciphertext Result:** `{cipher_out_r}`")
    except Exception:
        st.error("Missing configuration secrets in Streamlit Dashboard.")

# --- CHALLENGE 4: ROW TRANSPOSITION ---
with tab4:
    st.header("Challenge 4: Permutation Key Order (Row Transposition)")
    st.info("💡 **Canvas Task:** Map output text coordinates back to the original index positions to identify specific digits of the secret key sequence.")
    
    t_id = st.selectbox("Select assigned Challenge ID:", ["T1", "T2", "T3", "T4", "T5"], key="t_sel")
    
    try:
        secret_t_key = st.secrets[f"{t_id}_KEY"]
        num_cols = len(secret_t_key)
        
        st.warning(f"⚠️ This specific oracle module only evaluates blocks that fit perfectly into columns of size {num_cols} (Length must be exactly 28 characters).")
        
        user_text_t = st.text_input("Enter a Plaintext string (exactly 28 letters long):", 
                                    value="ABCDEFGHJKLMNOPQRSTUVWXYZABC", max_chars=28, key="t_in")
        
        clean_text_t = "".join([c for c in user_text_t if c.isalpha()])
        
        if len(clean_text_t) == 28:
            cipher_out_t = row_transposition_encrypt(clean_text_t, secret_t_key)
            st.success(f"**Permuted Ciphertext Result:** `{cipher_out_t}`")
        else:
            st.error(f"Current alpha length is {len(clean_text_t)} letters. Please adjust input text to equal exactly 28 letters.")
    except Exception:
        st.error("Missing configuration secrets in Streamlit Dashboard.")

# --- CHALLENGE 5: VIGENERE AUTOKEY ---
with tab2:
    st.header("Challenge 5: Autokey Loop Tracking")
    st.info("💡 **Canvas Task:** Input repeating streams ('AAAAA...') to track where shifts mirror the raw input, exposing keyword dimensions.")
    
    v_id = st.selectbox("Select assigned Challenge ID:", ["V1", "V2", "V3", "V4", "V5"], key="v_sel")
    
    try:
        secret_v_key = st.secrets[f"{v_id}_KEY"]
        
        user_text_v = st.text_input("Enter Plaintext String:", placeholder="Type a long continuous stream of a single letter...", value="AAAAAAAAAAAAAAAAAAAA", key="v_in")
        
        if user_text_v:
            cipher_out_v = vigenere_autokey_encrypt(user_text_v, secret_v_key)
            st.success(f"**Autokey Ciphertext Result:** `{cipher_out_v}`")
            
            # Simple UI tracking tip to support students conceptually
            st.markdown("**Character Distance Visualization Guide:**")
            st.text(f"Plaintext:  {user_text_v.upper()[:30]}")
            st.text(f"Ciphertext: {cipher_out_v[:30]}")
    except Exception:
        st.error("Missing configuration secrets in Streamlit Dashboard.")
