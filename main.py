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

# Check if the selected language has changed
# if st.session_state.get("prev_input_language") != input_language or st.session_state.get("prev_output_language") != output_language:
#     # Reset the uploaded file
#     uploaded_file = None
if os.path.exists("audio_to_save.wav"):
    os.remove('audio_to_save.wav')

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.header("orignal file")
    st.audio(uploaded_file, format='audio/wav')


def preprocess_audio(data):
    time.sleep(20)
    rate, data =wavfile.read(data)
    return rate,data


rev_ai = RevAI(token=token,input_lang=input_language_code,output_lang=output_language_code)
# result = rev_ai.process_audio(uploaded_file.getvalue())
# print(uploaded_file.getvalue())
# print(uploaded_file)


# if uploaded_file is not None:
    # Save the uploaded file to disk
    # with open("uploaded_file.wav", "wb") as f:
    #     f.write(uploaded_file.getvalue())

    # Pass the file path to the submit_job_local_file method
    # job = client.submit_job_local_file("uploaded_file.wav")
    # result= rev_ai.process_audio("uploaded_file.wav")

import os


if uploaded_file is not None:
    with st.spinner("Audio is translation please wait..."):
        temp_name="audio_to_save.wav"
        # rate, data = wavfile.read(uploaded_file)
        with open(temp_name, "wb") as f:
            f.write(uploaded_file.getvalue())
        # rate,data= rev_ai.process_audio(uploaded_file)
        location= rev_ai.process_audio(temp_name)
        os.remove(temp_name)
        # Save preprocessed data to a new wav file
        # wavfile.write('preprocessed.wav', rate, preprocessed_data.astype(np.int16))

        # wavfile.write('preprocessed.wav', rate, data.astype(np.int16))
    
    # Display the preprocessed audio file in a playlist
    st.header("Translate file")
    st.audio(location, format='audio/wav')


# print(uploaded_file)