import streamlit as st

st.title("🔐 Crypto Challenge: Protected Keys")

# -------------------------------------------------------------
# FETCHING HIDDEN KEYS FROM STREAMLIT SECRETS 
# (Students cannot see these, even if your GitHub repo is public!)
# -------------------------------------------------------------
try:
    SECRET_CAESAR_SHIFT = int(st.secrets["CAESAR_KEY"])
    SECRET_VIGENERE_KEY = st.secrets["VIGENERE_KEY"].upper()
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

# -------------------------------------------------------------
# USER INTERFACE
# -------------------------------------------------------------
tab1, tab2 = st.tabs(["Level 1: Caesar Cipher", "Level 2: Vigenère Cipher"])

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
