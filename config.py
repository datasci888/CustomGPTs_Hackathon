import dotenv
import os
import streamlit as st

dotenv.load_dotenv()

class Config :
    # open_ai_key = os.getenv("OPENAI_API_KEY")
    # assembly_ai_key = os.getenv("ASSEMBLY_AI_API_KEY")
    open_ai_key = st.secrets("open_ai_key")
    assembly_ai_key = st.secrets("assembly_ai_key")
    