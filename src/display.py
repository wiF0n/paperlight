import time
import streamlit as st


def display_pdf(base64_pdf: str, ui_width: int) -> None:
    """
    Display a PDF file in the UI.

    Parameters:
    - base64_pdf (str): The base64 encoded representation of the PDF file.
    - ui_width (int): The width of the UI in pixels.

    Returns:
    None
    """

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=100% height={str(ui_width * 8 / 9)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


def streamify_qa_response(chain, question):
    """
    Streamify an LLM response.

    Args:
    - llm_response: str: The LLM response

    Returns:
    - str: The streamified LLM response
    """
    for chunk in chain.stream(question):
        if chunk.get("sources"):
            sources = chunk.get("sources")
        if chunk.get("answer"):
            yield chunk.get("answer")

    yield "\n\n"
    for char in sources:
        yield char
        time.sleep(0.01)


def streamify_text(text: str):
    """
    Streamify text.

    Args:
    - abstract: str: The abstract

    Returns:
    - str: The streamified abstract
    """
    for char in text:
        yield char
        time.sleep(0.01)


def streamify_llm_response(llm, prompt):
    """
    Streamify an LLM response.

    Args:
    - llm_response: str: The LLM response

    Returns:
    - str: The streamified LLM response
    """

    for chunk in llm.stream(prompt):
        yield chunk.content
