"""
# Paper Buddy 🧻🤸
"""

import base64
import requests

import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_javascript import st_javascript

from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from src.search import (
    top_n_results_factory,
    get_paper_details,
    streamify_abstract,
)
from src.debug import RESULTS


@st.cache_data
def download_pdf_bytes(url):
    """
    Downloads a PDF file from the given URL and returns its content as bytes.

    Args:
      url: The URL of the PDF file.

    Returns:
      The content of the PDF file as base64 encoded byte string, or None if the download fails.

    Raises:
      requests.exceptions.RequestException: If there is an error downloading the file.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    if response.headers.get("Content-Type") != "application/pdf":
        raise ValueError("URL doesn't point to a PDF file")

    content_length = (
        int(response.headers.get("Content-Length"))
        if response.headers.get("Content-Length")
        else None
    )
    chunks = []
    total_downloaded = 0
    for chunk in response.iter_content(1024):
        chunks.append(chunk)
        total_downloaded += len(chunk)
        if content_length:
            print(
                f"Downloaded {total_downloaded}/{content_length} bytes ({total_downloaded / content_length * 100:.2f}%)"
            )

    return base64.b64encode(b"".join(chunks)).decode("utf-8")


def display_pdf(base64_pdf, ui_width):

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=100% height={str(ui_width * 8/9)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


DEBUG = False
if "paper_pdf" not in st.session_state:
    st.session_state["paper_pdf"] = None

# Sidebar
st.sidebar.title("Search Settings")
st.sidebar.number_input(
    "Enter a number of results to display",
    key="num_search_results",
    value=3,
    min_value=1,
    max_value=5,
)

st.markdown(
    """
    ## Paper Buddy 🧻🤸
    """
)
st.markdown("### Search for scientific papers")
st.text_input(
    "Enter a query for the paper you want to search for (e.g., LayoutLMv3)",
    key="ib_query",
)

search_func = top_n_results_factory(st.session_state.num_search_results)

search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search_func,
)

if len(st.session_state.ib_query) != 0:
    if DEBUG:
        results = RESULTS
    else:
        results = search_tool.run(st.session_state.ib_query + "+arxiv")

    if (
        len(results) == 1
        and results[0].get("Result") == "No good Google Search Result was found"
    ):
        st.write("No results found")
    else:
        for i, result in enumerate(results):
            title, authors, abstract = get_paper_details(result).values()
            stoggle(f"{title} by {authors}", abstract)
            st.button(f"**Select paper #{i + 1}**", key=f"pb_select_abstract_{i}")

col1, col2 = st.columns(spec=[2, 1], gap="small")

for i in range(st.session_state.num_search_results):
    if st.session_state.get(f"pb_select_abstract_{i}"):
        st.session_state.paper_pdf = download_pdf_bytes(
            results[i]["link"].replace("abs", "pdf")
        )

# Chat and PDF display
if st.session_state.paper_pdf:
    # add checkbox to show/hide the chat history
    st.sidebar.checkbox("Show chat history", key="show_chat_history", value=False)

    with col1:
        ui_width = st_javascript("window.innerWidth")
        display_pdf(st.session_state.paper_pdf, ui_width)

    with col2:
        st.markdown("#### Brainstorm with Paper Buddy")
        with st.container(height=int(ui_width * 9 / 10)):
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # if the chat history is hidden, don't display it
            if st.session_state.show_chat_history:
                # Display chat messages from history on app rerun
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("Ask me a question about the paper"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Display assistant response in chat message container
                with st.chat_message("ai"):
                    response = f"Echo: {prompt}"
                    st.write_stream(streamify_abstract(response))
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
