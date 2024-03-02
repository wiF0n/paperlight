"""
Paper Buddy 🧻🤸
"""

from dotenv import load_dotenv

import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_javascript import st_javascript

from src.search import get_paper_details, get_search_results
from src.process import process_arxiv_paper_from_url
from src.qa_chain import get_qa_chain
from src.display import display_pdf, streamify_qa_response

load_dotenv()

if "paper_pdf" not in st.session_state:
    st.session_state["paper_pdf"] = None

if "paper_tex" not in st.session_state:
    st.session_state["paper_tex"] = None

if "paper_details" not in st.session_state:
    st.session_state["paper_details"] = None


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

if len(st.session_state.ib_query) != 0:
    results = get_search_results(st.session_state.ib_query + "+arxiv", st.session_state.num_search_results)

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
        st.session_state.paper_details = get_paper_details(results[i])
        st.session_state.paper_tex, st.session_state.paper_pdf = (
            process_arxiv_paper_from_url(results[i]["link"])
        )

# Chat and PDF display
if st.session_state.paper_pdf and st.session_state.paper_tex:

    qa_chain = get_qa_chain(st.session_state.paper_details, st.session_state.paper_tex)
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
                    response = st.write_stream(streamify_qa_response(qa_chain, prompt))
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
