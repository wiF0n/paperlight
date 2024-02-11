import streamlit as st
from streamlit_extras.stoggle import stoggle

st.text_input(
    "Enter a query for the paper you want to search for (e.g., LayoutLMv3)",
    key="query",
)

st.sidebar.number_input(
    "Enter a number of results to display",
    key="num_results",
    value=5,
    min_value=1,
    max_value=10,
)

st.write(st.session_state.query)
for result in range(st.session_state.num_results):
    stoggle(f"Paper {result + 1}", f"paper_{result + 1}")
# st.chat_input("Say something")
