import streamlit as st
from streamlit_extras.stoggle import stoggle

from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from src.search import (
    top_n_results_factory,
    get_paper_details,
    # streamify_abstract,
    streamify_llm_response,
)
from src.langchain import icebreaker_prompt_template
from src.debug import RESULTS

DEBUG = True

if "selected_abstract" not in st.session_state:
    st.session_state["selected_abstract"] = None

if "icebreaker_abstract" not in st.session_state:
    st.session_state["icebreaker_abstract"] = None

# Sidebar
st.sidebar.title("Search Settings")
st.sidebar.number_input(
    "Enter a number of results to display",
    key="icebreaker_num_results",
    value=3,
    min_value=1,
    max_value=5,
)
st.sidebar.title("Summary Settings")
st.sidebar.selectbox(
    "Select the audience to summarize for:",
    ["High School Students", "College Students", "Gen Z", "Gen X", "Gen Y"],
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


search_func = top_n_results_factory(st.session_state.icebreaker_num_results)

search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search_func,
)

if len(st.session_state.icebreaker_query) != 0:
    if DEBUG:
        results = RESULTS
    else:
        results = search_tool.run(st.session_state.icebreaker_query)

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


for i in range(st.session_state.icebreaker_num_results):
    if st.session_state.get(f"icebreaker_select_abstract_{i}"):
        st.session_state["selected_abstract"] = get_paper_details(results[i])[
            "abstract"
        ]

st.markdown("### Icebreaking")

st.session_state["icebreaker_abstract"] = st.text_area(
    "Abstract to summarize:",
    value=st.session_state["selected_abstract"],
    height=200,
)

# print(icebreaker_abstract)

summarize_button = st.button("Summarize", key="icebreaker_summarize")

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", streaming=True)

if summarize_button:
    placeholder = st.empty()
    write_summarizing = placeholder.write("Summarizing...")
    icebreaker_prompt = icebreaker_prompt_template.format(
        audience=st.session_state.icebreaker_audience,
        language=st.session_state.icebreaker_language,
        abstract=st.session_state.icebreaker_abstract,
    )
    st.write_stream(streamify_llm_response(llm, icebreaker_prompt))
    placeholder.empty()
