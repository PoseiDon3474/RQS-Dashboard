import streamlit as st
import pandas as pd

# --- Styling to match the original app ---
st.markdown("""
    <style>
    .main {
        background-color: #222629;
    }
    h1 {
        color: #FFFFFF;
        font-family: system-ui;
        margin-left: 20px;
    }
    label, .stTextInput label {
        color: #86C232;
        font-family: system-ui;
        font-size: 20px;
        margin-left: 20px;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #86C232;
        border-color: #86C232;
        color: #FFFFFF;
        font-family: system-ui;
        font-size: 20px;
        font-weight: bold;
        margin-left: 30px;
        margin-top: 20px;
        width: 140px;
    }
    .stTextInput>div>input {
        color: #222629;
        font-family: system-ui;
        font-size: 20px;
        margin-left: 10px;
        margin-top: 20px;
        width: 100px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>TO THE POWER OF MATH!</h1>", unsafe_allow_html=True)

# --- Input fields ---
base = st.text_input("Base number:", key="base")
exponent = st.text_input("...to the power of:", key="exponent")

# --- Calculate Button ---
if st.button("CALCULATE"):
    try:
        base_num = float(base)
        exp_num = float(exponent)
        # If you want to call an API instead, uncomment below and set your API URL
        # api_url = "YOUR PowerOfMathAPI Invoke URL"
        # response = requests.post(api_url, json={"base": base_num, "exponent": exp_num})
        # result = response.json().get("body", "No result returned.")
        result = base_num ** exp_num
        st.success(f"{base_num} to the power of {exp_num} is {result}")
    except ValueError:
        st.error("Please enter valid numbers for both fields.")
