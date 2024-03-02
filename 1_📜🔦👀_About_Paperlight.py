import argparse

import streamlit as st

# Define arguments
parser = argparse.ArgumentParser(prog="Paperlight", description="Look at scientific papers with more clarity")

parser.add_argument("--debug", action="store_true", help="Enable debug mode")

args = parser.parse_args()

st.session_state["debug"] = args.debug

st.set_page_config(
    initial_sidebar_state="expanded",
    layout="wide",
)

st.title("Paperlight 📜🔦👀")
st.header("Look at scientific papers with more clarity")

st.markdown(
    """
    Paperlight is designed to make reading and understanding scientific papers easier.
    Currently, it consists of two main features/tools:
    - **Icebreaker**: Summarizes scientific papers' abstracts
    to a specific audience and language. Currently, you can choose from the
    following audiences:
        - High School Students
        - College Students
        - University Students

        As of now, only papers from the [arXiv](https://arxiv.org/) and
        [astrophysics data system](https://ui.adsabs.harvard.edu/) are supported.
    - **Paper Buddy**: Tool to help you understand the paper more deeply. It allows you to ask questions about the paper and get the desired answers.

        As of now, only papers from the [arXiv](https://arxiv.org/) are supported.
    """
)
