import streamlit as st
import random

st.title("🔐 Crypto Challenge: Protected Keys")
st.write("Analyze plaintexts and ciphertexts to uncover the hidden keys. Your code is public, but your variables are perfectly safe!")

# -------------------------------------------------------------
# FETCHING HIDDEN KEYS FROM STREAMLIT SECRETS 
# -------------------------------------------------------------
try:
    SECRET_CAESAR_SHIFT = int(st.secrets["CAESAR_KEY"])
    SECRET_VIGENERE_KEY = st.secrets["VIGENERE_KEY"].upper()
    SECRET_VERNAM_SEED = st.secrets["VERNAM_SEED"]
except Exception:
    st.error("⚠️ Setup Error: Secrets are not configured in the Streamlit Dashboard yet.")
    st.stop()

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def vigenere_encrypt(text, key):
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(char) - start + shift) % 26 + start))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def vernam_encrypt(text, seed_string):
    """
    Generates a deterministic random key stream matching the length 
    of the input text using a shared hidden seed string.
    """
    # Initialize a local random generator anchored strictly to our secret seed
    # This ensures identical inputs produce identical key streams during the session
    rng = random.Random(seed_string)
    
    result = []
    key_stream_used = []
    
    for char in text:
        # Generate a shift between 0 and 25 for every single character slot
        shift = rng.randint(0, 25)
        key_char = chr(ord('A') + shift)
        key_stream_used.append(key_char)
        
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            result.append(char)
            
    return "".join(result), "".join(key_stream_used)

# -------------------------------------------------------------
# USER INTERFACE
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Level 1: Caesar", "Level 2: Vigenère", "Level 3: Vernam (One-Time Pad)"])

# --- LEVEL 1 & 2 REMAIN SECURELY INTACT ---
with tab1:
    st.header("Level 1: Find the Shift Key")
    user_plaintext_1 = st.text_input("Enter Plaintext:", placeholder="Type here...", key="caesar_in")
    if user_plaintext_1:
        if len(user_plaintext_1.strip()) < 5 or set(user_plaintext_1.upper().replace(" ", "")) == {'A'}:
            st.warning("⚠️ Shortcut blocked! Please enter a real word or phrase (min 5 chars).")
        else:
            ciphertext_1 = caesar_encrypt(user_plaintext_1, SECRET_CAESAR_SHIFT)
            st.info(f"**Ciphertext Output:** `{ciphertext_1}`")
    st.divider()
    student_guess_1 = st.number_input("Think you found the key? Enter the shift number:", min_value=0, max_value=25, value=0)
    if st.button("Verify Caesar Key"):
        if student_guess_1 == SECRET_CAESAR_SHIFT:
            st.success("🎉 Correct! You cracked the Caesar shift!")
        else:
            st.error("❌ Not quite. Keep analyzing!")

with tab2:
    st.header("Level 2: Find the Keyword")
    user_plaintext_2 = st.text_input("Enter Plaintext:", placeholder="Type here...", key="vig_in")
    if user_plaintext_2:
        if len(user_plaintext_2.strip()) < 6 or set(user_plaintext_2.upper().replace(" ", "")) == {'A'}:
            st.warning("⚠️ Shortcut blocked! Please enter a real word or phrase (min 6 chars).")
        else:
            ciphertext_2 = vigenere_encrypt(user_plaintext_2, SECRET_VIGENERE_KEY)
            st.info(f"**Ciphertext Output:** `{ciphertext_2}`")
    st.divider()
    student_guess_2 = st.text_input("Think you found the key? Enter the keyword (ALL CAPS):")
    if st.button("Verify Vigenère Key"):
        if student_guess_2.strip().upper() == SECRET_VIGENERE_KEY:
            st.success("🏆 Brilliant! You broke the Vigenère cipher!")
        else:
            st.error("❌ Incorrect keyword.")

# --- NEW LEVEL 3: VERNAM CIPHER ---
with tab3:
    st.header("Level 3: The Unbreakable One-Time Pad")
    st.write("A true Vernam cipher uses a key stream that is completely random and **exactly as long as your plaintext**.")
    st.markdown("*Hint: Because the key stream is generated sequentially based on a hidden seed, typing the **same length** of text will reuse the exact same stream positions!*")
    
    user_plaintext_3 = st.text_input("Enter Plaintext to observe encryption:", placeholder="Type a test phrase...", key="vernam_in")
    
    if user_plaintext_3:
        # Encrypt and get the exact key stream character slice used for this length
        ciphertext_3, exact_key_stream = vernam_encrypt(user_plaintext_3, SECRET_VERNAM_SEED)
        st.info(f"**Ciphertext Output:** `{ciphertext_3}`")
        
    st.divider()
    st.subheader("🕵️‍♂️ The Challenge: Intercept the Key Stream")
    st.write("Type a 5-letter plaintext above. Find out what exact 5-letter Key Stream was generated to encrypt it!")
    
    student_guess_3 = st.text_input("Enter the 5-letter Key Stream generated for a 5-letter input (ALL CAPS):", max_chars=5)
    
    if st.button("Verify Vernam Key Stream"):
        if user_plaintext_3 and len(user_plaintext_3) == 5:
            # Generate the true 5-letter answer using a dummy string of 5 characters
            _, target_stream = vernam_encrypt("AAAAA", SECRET_VERNAM_SEED)
            
            if student_guess_3.strip().upper() == target_stream:
                st.success(f"👑 Legendary! You intercepted the One-Time Pad stream segment: `{target_stream}`")
            else:
                st.error("❌ Incorrect key stream mapping. Remember: Inputting 'AAAAA' forces the cipher text output to match the key stream exactly!")
        else:
            st.warning("⚠️ To verify, you must first input exactly a **5-character string** into the Plaintext box above so the system can evaluate your guess against a matching size!")
