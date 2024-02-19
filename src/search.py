"""
This module contains functionality around searching for papers.
"""

from typing import Dict, List, Callable

import streamlit as st

from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.utilities import TextRequestsWrapper

from bs4 import BeautifulSoup


def _top_n_results_factory(n: int) -> Callable:
    """
    Factory function to create a function that returns the top n results from a search query.

    Args:
    - n: int: The number of results to return

    Returns:
    - Callable: A function that returns the top n results from a search query
    """

    @st.cache_data
    def top_n_results(query) -> List[dict]:
        """
        Get the top n search results for a query.

        Args:
        - query: str: The query

        Returns:
        - List[dict]: The top n search results
        """
        search = GoogleSearchAPIWrapper()
        return search.results(query, n)

    return top_n_results


def _get_search_tool(search_func: Callable) -> Tool:
    """
    Get a search tool.

    Args:
    - search_func: Callable: The search function

    Returns:
    - Tool: The search tool
    """
    return Tool(
        name="Google Search",
        description="Search Google for recent results.",
        func=search_func,
    )


def get_search_results(query: str, n: int) -> List[dict]:
    """
    Get the top n search results for a query.

    Args:
    - query: str: The query
    - n: int: The number of results to return

    Returns:
    - List[dict]: The top n search results
    """
    search_func = _top_n_results_factory(n)
    search_tool = _get_search_tool(search_func)
    return search_tool.run(query)


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
    # Get the link from the search result
    result = request_wrapper.get(search_result["link"])

    # Change the soup features based on the link
    if "harvard" in search_result["link"]:
        soup_kwargs = {"features": "lxml"}
    elif "arxiv" in search_result["link"]:
        soup_kwargs = {"features": "xml"}
    else:
        soup_kwargs = {}

    # Initialize the soup
    soup = BeautifulSoup(result, **soup_kwargs)

    # Get the abstract, title, and authors
    abstract = soup.find("meta", property="og:description")["content"]
    title = soup.find("meta", property="og:title")["content"]
    if "arxiv" in search_result["link"]:
        authors = soup.find_all("meta", attrs={"name": "citation_author"})
    elif "harvard" in search_result["link"]:
        authors = soup.find_all("meta", property="article:author")
    else:
        ValueError("Unsupported link type")

    authors = [author["content"].replace(",", "") for author in authors]
    if len(authors) > 3:
        authors = authors[:3]
        authors.append("et al.")
    authors = ", ".join(authors)

    return {"title": title, "authors": authors, "abstract": abstract}
