from typing import Dict, Optional, Tuple
import re
import base64
import tarfile
import tempfile

from pylatexenc.latex2text import LatexNodes2Text
import arxiv

import streamlit as st


def _extract_arxiv_id(link: str) -> str:
    return link.split("/")[-1]


def _process_tex_paper(tex_text: str) -> Optional[Dict[Dict, str]]:
    """
    Split the given tex text into plain text divided into sections.

    Args:
        text: The input text.

    Returns:
        A dictionary containing the sections as keys and their content as values.
        Returns None if no valid sections are found in the text.
    """
    sections = {}
    current_section_name = ""
    section_pattern = re.compile(r"^(\\section)")
    in_section = False

    for line in tex_text.splitlines():
        if section_pattern.match(line):
            if (
                in_section
            ):  # Ensure previous section was closed before starting a new one
                print(
                    f"Warning: Ignoring overlapping sections. Closing previous section '{current_section_name}'."
                )
            current_section_name = (
                line.strip()[len(r"\\section") :].strip().replace("}", "")
            )
            sections[current_section_name] = ""
            in_section = True
        elif in_section:
            if line.strip():  # Ignore empty lines within sections
                sections[current_section_name] += line.strip() + "\n"
        else:
            # Ignore text outside sections
            pass

    if not sections:
        print("Warning: No valid sections found in LaTeX text.")
        return None

    plain_sections = {
        section: LatexNodes2Text().latex_to_text(content).strip()
        for section, content in sections.items()
    }

    return plain_sections


@st.cache_data
def process_arxiv_paper_from_url(
    paper_url: str,
) -> Tuple[Optional[Dict[Dict, str]], str]:
    """Downloads and processes an arXiv paper, returning its TeX content and PDF content as base64.

    Args:
        paper_url: The URL of the arXiv paper to process.

    Returns:
        A tuple containing:
        - The TeX content of the paper as a string.
        - The PDF content of the paper as a base64-encoded string.
    """

    arxiv_client = arxiv.Client()

    arxiv_paper_obj = next(
        arxiv_client.results(arxiv.Search(id_list=[_extract_arxiv_id(paper_url)]))
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download the source and PDF files
            arxiv_paper_obj.download_source(dirpath=temp_dir, filename="paper.tar.gz")
            arxiv_paper_obj.download_pdf(dirpath=temp_dir, filename="paper.pdf")

            # Extract the TeX content from the tarball
            with tarfile.open(f"{temp_dir}/paper.tar.gz", "r:gz") as tar:
                for member in tar.getmembers():
                    if member.name.endswith(".tex"):
                        file = tar.extractfile(member)
                        tex_content = file.read().decode("utf-8")
                        break

            # Read the PDF content and convert to base64
            with open(f"{temp_dir}/paper.pdf", "rb") as file:
                pdf_content = base64.b64encode(file.read()).decode("utf-8")

            return _process_tex_paper(tex_content), pdf_content

        except Exception as e:
            raise ValueError(f"Error processing arXiv paper: {e}") from e
