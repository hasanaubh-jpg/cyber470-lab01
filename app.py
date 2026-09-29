import streamlit as st

# Set up the web page title and description
st.title("🔐 Crypto Challenge: Chosen Plaintext Attack")
st.write("Your goal is to figure out the secret keys by entering different plaintexts and analyzing the resulting ciphertexts!")

# -------------------------------------------------------------
# SECRET KEYS (Completely hidden from students on the web app)
# -------------------------------------------------------------
SECRET_CAESAR_SHIFT = 7
SECRET_VIGENERE_KEY = "MATH"

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
    key = key.upper()
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
# USER INTERFACE (What your students actually see)
# -------------------------------------------------------------

# Tab layout to separate the two challenges
tab1, tab2 = st.tabs(["Level 1: Caesar Cipher", "Level 2: Vigenère Cipher"])

with tab1:
    st.header("Level 1: Find the Shift Key")
    st.write("Enter text below to see how the system encrypts it.")
    
    # Input field for students
    user_plaintext_1 = st.text_input("Enter Plaintext:", placeholder="Type here...", key="caesar_in")
    
    if user_plaintext_1:
        # Encrypt using the hidden shift key
        ciphertext_1 = caesar_encrypt(user_plaintext_1, SECRET_CAESAR_SHIFT)
        st.info(f"**Ciphertext Output:** `{ciphertext_1}`")
        
    # Verification section
    st.divider()
    student_guess_1 = st.number_input("Think you found the key? Enter the shift number:", min_value=0, max_value=25, value=0)
    if st.button("Verify Caesar Key"):
        if student_guess_1 == SECRET_CAESAR_SHIFT:
            st.success("🎉 Correct! You cracked the Caesar shift!")
        else:
            st.error("❌ Not quite. Keep analyzing the inputs and outputs!")

with tab2:
    st.header("Level 2: Find the Keyword")
    st.write("This algorithm shifts letters based on a repeating keyword.")
    
    user_plaintext_2 = st.text_input("Enter Plaintext:", placeholder="Type here...", key="vig_in")
    
    if user_plaintext_2:
        # Encrypt using the hidden word key
        ciphertext_2 = vigenere_encrypt(user_plaintext_2, SECRET_VIGENERE_KEY)
        st.info(f"**Ciphertext Output:** `{ciphertext_2}`")
        
    # Verification section
    st.divider()
    student_guess_2 = st.text_input("Think you found the key? Enter the keyword (ALL CAPS):")
    if st.button("Verify Vigenère Key"):
        if student_guess_2.strip().upper() == SECRET_VIGENERE_KEY:
            st.success("🏆 Brilliant! You successfully broke the Vigenère cipher!")
        else:
            st.error("❌ Incorrect keyword. Try entering strings of repeated letters (like 'AAAAA') to spot patterns!")
