"""
This module contains functionality around searching for papers.
"""

from typing import Dict
import time

import streamlit as st

from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.utilities import TextRequestsWrapper

from bs4 import BeautifulSoup


def top_n_results_factory(n: int):
    """
    Factory function to create a function that returns the top n results from a search query.

    Args:
    - n: int: The number of results to return

    Returns:
    - function: A function that returns the top n results from a search query
    """

    @st.cache
    def top_n_results(query):
        search = GoogleSearchAPIWrapper()
        return search.results(query, n)

    return top_n_results


request_wrapper = TextRequestsWrapper()


@st.cache_data
def get_paper_details(search_result: Dict[str, str]) -> Dict[str, str]:
    """
    Get the abstract from a search result.

    Args:
    - search_result: Dict[str, str]: The search result

    Returns:
    - str: The abstract
    """

    result = request_wrapper.get(search_result["link"])

    if "harvard" in search_result["link"]:
        soup_kwargs = {"features": "lxml"}
    else:
        soup_kwargs = {}

    soup = BeautifulSoup(result, **soup_kwargs)

    abstract = soup.find("meta", property="og:description")["content"]
    title = soup.find("meta", property="og:title")["content"]
    authors = soup.find_all("meta", property="article:author")
    authors = [author["content"].replace(",", "") for author in authors]
    if len(authors) > 3:
        authors = authors[:3]
        authors.append("et al.")
    authors = ", ".join(authors)
    authors
    return {"title": title, "authors": authors, "abstract": abstract}


def streamify_abstract(abstract: str):
    """
    Streamify an abstract.

    Args:
    - abstract: str: The abstract

    Returns:
    - str: The streamified abstract
    """
    for char in abstract:
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
