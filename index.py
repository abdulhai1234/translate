from dotenv import load_dotenv

import os
import streamlit as st
load_dotenv()




password = os.environ.get("token")

# Use the password in your app
st.write(f"The password is: {password}")