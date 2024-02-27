"""
This is the Icebreaker page of the Streamlit app.
"""
from dotenv import load_dotenv

import streamlit as st
from streamlit_extras.stoggle import stoggle

from langchain_openai import ChatOpenAI

from src.search import (
    get_search_results,
    get_paper_details,
)
from src.qa_chain import get_prompt_template
from src.display import streamify_llm_response
from src.debug import RESULTS

load_dotenv()

DEBUG = True

if "icebreaker_selected_abstract" not in st.session_state:
    st.session_state["icebreaker_selected_abstract"] = None

if "icebreaker_abstract" not in st.session_state:
    st.session_state["icebreaker_abstract"] = None

if "icebreaker_model" not in st.session_state:
    st.session_state["icebreaker_model"] = "gpt-3.5-turbo"

if "icebreaker_prompt" not in st.session_state:
    st.session_state["icebreaker_prompt"] = "icebreaker"

# Sidebar
st.sidebar.title("Search Settings")
st.sidebar.number_input(
    "Enter a number of results to display",
    key="num_search_results",
    value=3,
    min_value=1,
    max_value=5,
)
st.sidebar.title("Summary Settings")
st.sidebar.selectbox(
    "Select the audience to summarize for:",
    ["High School Students", "College Students", "University Students", "Researchers"],
    key="icebreaker_audience",
)

st.sidebar.selectbox(
    "Select the language to summarize in:",
    ["English", "Slovak"],
    key="icebreaker_language",
)

st.title("🧊🔨Icebreaker")

st.header("Break the barrier to scientific papers")

st.markdown("### Search for scientific papers' abstracts")
st.text_input(
    "Enter a query for the paper you want to search for (e.g., LayoutLMv3)",
    key="icebreaker_query",
)

if len(st.session_state.icebreaker_query) != 0:
    if DEBUG:
        results = RESULTS
    else:
        results = get_search_results(
            st.session_state.icebreaker_query, st.session_state.num_search_results
        )

    if (
        len(results) == 1
        and results[0].get("Result") == "No good Google Search Result was found"
    ):
        st.write("No results found")
    else:
        for i, result in enumerate(results):
            title, authors, abstract = get_paper_details(result).values()
            stoggle(f"{title} by {authors}", abstract)
            st.button(
                f"**Select abstract #{i + 1}**", key=f"icebreaker_select_abstract_{i}"
            )


for i in range(st.session_state.num_search_results):
    if st.session_state.get(f"icebreaker_select_abstract_{i}"):
        st.session_state["icebreaker_selected_abstract"] = get_paper_details(
            results[i]
        )["abstract"]

st.markdown("### Icebreaking")

st.session_state["icebreaker_abstract"] = st.text_area(
    "Abstract to explain:",
    value=st.session_state["icebreaker_selected_abstract"],
    height=200,
)

explain_button = st.button("Explain", key="icebreaker_explain")

# TODO: Add choice of model
if DEBUG:
    st.sidebar.selectbox(
        "Select the model to use:",
        ["gpt-3.5-turbo", "gpt-4-turbo-preview"],
        key="icebreaker_model",
    )

    st.sidebar.selectbox(
        "Select prompt to use:",
        ["icebreaker", "icebreaker_bad"],
        key="icebreaker_prompt",
    )

llm = ChatOpenAI(
    temperature=0, model_name=st.session_state.icebreaker_model, streaming=True
)

icebreaker_prompt_template = get_prompt_template(st.session_state.icebreaker_prompt)

if explain_button:
    placeholder = st.empty()
    write_summarizing = placeholder.write("Explaining...")
    icebreaker_prompt = icebreaker_prompt_template.format(
        audience=st.session_state.icebreaker_audience,
        language=st.session_state.icebreaker_language,
        abstract=st.session_state.icebreaker_abstract,
    )
    st.write_stream(streamify_llm_response(llm, icebreaker_prompt))
    placeholder.empty()
