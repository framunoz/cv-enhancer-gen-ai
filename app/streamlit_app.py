import streamlit as st

# Get the api_key
with st.sidebar:
    api_key = st.text_input("Enter your API Key", key="GOOGLE_API_KEY", type="password")
    st.title("CV Enhancer Gen AI")
    st.markdown("Enhance your CV using Generative AI.")

st.title("Welcome to CV Enhancer Gen AI")
st.markdown("Upload your CV and let AI help you improve it!")
st.file_uploader("Upload your CV", type=["pdf", "docx", "txt"])
st.button("Enhance CV")
st.markdown("Enhanced CV will be displayed here.")
