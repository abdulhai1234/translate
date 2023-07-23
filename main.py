import streamlit as st
from scipy.io import wavfile
import numpy as np
from rev_ai import apiclient as api
# from models.rev_ai import RevAI

# from streamlit.rev_ai import 
import os

from rev_ai_main import RevAI
import time
from dotenv import load_dotenv
load_dotenv()


token = os.environ.get("token")


import sys
sys.path.append(r'D:\amjid\Translation\models')

st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("Audio File Upload")

languages = {
    "English": "en",
    "Urdu": "ur",
    "Polish": "pl",
    "Arabic": "ar"
}

input_language = st.selectbox("Input Language", list(languages.keys()),0)
output_language = st.selectbox("Output Language", list(languages.keys()),1)

input_language_code = languages[input_language]
output_language_code = languages[output_language]

uploaded_file = st.file_uploader("Choose an audio file", type=["wav","mp3"])

if uploaded_file is None:
    st.warning("Please upload a file")
# Check if the selected language has changed
# if st.session_state.get("prev_input_language") != input_language or st.session_state.get("prev_output_language") != output_language:
#     # Reset the uploaded file
#     uploaded_file = None

# Check if the selected input language has changed
if st.session_state.get("prev_input_language") != input_language:
    # Reset the uploaded file
    uploaded_file = None
    # st.experimental_rerun()



# Store the current selected input language in session state
st.session_state["prev_input_language"] = input_language

print(st.session_state.get("prev_input_language"))

if os.path.exists("audio_to_save.wav"):
    os.remove('audio_to_save.wav')

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.header("orignal file")
    st.audio(uploaded_file, format='audio/wav')





rev_ai = RevAI(token=token,input_lang=input_language_code,output_lang=output_language_code)

import os


if uploaded_file is not None:
    with st.spinner("Audio is translation please wait..."):
        temp_name="audio_to_save.wav"
        with open(temp_name, "wb") as f:
            f.write(uploaded_file.getvalue())
        location= rev_ai.process_audio(temp_name)
        os.remove(temp_name)    
    st.header("Translate file")
    uploaded_file=None
    st.audio(location, format='audio/wav')


# print(uploaded_file)