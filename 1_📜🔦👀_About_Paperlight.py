import streamlit as st


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
        - Parents
        As of now, only papers from the [arXiv](https://arxiv.org/) and
        [astrophysics data system](https://ui.adsabs.harvard.edu/) are supported.
    - **Paper Buddy**: Tool to help you understand the paper. It allows you to ask questions about the paper and get the answers.
    """
)
