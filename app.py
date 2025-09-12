import streamlit as st
import pandas as pd
import os

# Shift key (hardcoded, keep consistent to reverse)
SHIFT_KEY = 3  

def encrypt_text(text):
    result = []
    for char in str(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + SHIFT_KEY) % 26 + base))
        else:
            result.append(char)  # keep digits, spaces, symbols
    return ''.join(result)

def decrypt_text(text):
    result = []
    for char in str(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - SHIFT_KEY) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

st.title("Excel Multi-Column Alphabet Masking Tool")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    base_filename = os.path.splitext(uploaded_file.name)[0]
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded File (First 5 Rows)")
    st.dataframe(df.head())

    columns = st.multiselect("Select Columns to Mask", df.columns)
    action = st.radio("Action", ["Encrypt (Mask)", "Decrypt (Unmask)"])

    if st.button("Process"):
        df_processed = df.copy()
        try:
            for col in columns:
                if action == "Encrypt (Mask)":
                    df_processed[col] = df[col].astype(str).apply(encrypt_text)
                    suffix = "_encrypted"
                else:
                    df_processed[col] = df[col].astype(str).apply(decrypt_text)
                    suffix = "_decrypted"

            st.write("### Preview of Processed File (First 5 Rows)")
            st.dataframe(df_processed.head())

            processed_file = f"{base_filename}{suffix}.xlsx"
            df_processed.to_excel(processed_file, index=False)

            with open(processed_file, "rb") as f:
                st.download_button("Download Processed File", f, file_name=processed_file)

        except Exception as e:
            st.error(f"Error during processing: {e}")
