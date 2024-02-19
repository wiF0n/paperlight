"""
Functions for the QA chain
"""

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def _unique_values_dict(list_):
    return list(dict.fromkeys(list_))


def _format_section_metadata(docs):
    sections = _unique_values_dict(
        [doc.metadata.get("section", "Unknown") for doc in docs]
    )
    return "Information was retrieved from following sections: " + ", ".join(sections)


def _tex_to_splits(paper_details, tex_content, chunk_size=2024, chunk_overlap=256):
    """
    Split a TeX content (dict of section texts) into splits for vector database.

    Args:
    - tex_content: str: The TeX content

    """

    docs = [
        Document(
            page_content=f"""Title: {paper_details["title"]},
            Authors": {paper_details["authors"]},
            """,
            metadata={"section": "Info"},
        ),
        Document(
            page_content=paper_details["abstract"], metadata={"section": "Abstract"}
        ),
    ]

    docs.extend(
        [
            Document(page_content=text, metadata={"section": section})
            for section, text in tex_content.items()
        ]
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(docs)
    return splits


def _get_embedder(embedding_model: str):
    """
    Get embedder for vector database.

    Args:
    - model: str: The model to use

    """

    return OpenAIEmbeddings(model=embedding_model)


def _get_paper_retriever(paper_details, paper_tex, embedding_model):
    """
    Get the vector database retriever for a paper.

    Args:
    - paper_tex: str: The TeX content of the paper
    - embedder: str: Embedder to use

    """
    splits = _tex_to_splits(paper_details, paper_tex)
    vectorstore = Chroma.from_documents(
        splits, embedding=_get_embedder(embedding_model)
    )
    return vectorstore.as_retriever()


def _get_llm(model: str):
    """
    Get the LLM model.

    Args:
    - model: str: The model to use

    """
    return ChatOpenAI(model=model)


# TODO: move to a separate file
def get_prompt_template(prompt_name: str):
    """
    Get a prompt template.

    Args:
    - prompt_name: str: The name of the prompt

    """

    return load_prompt("prompts/" + prompt_name + ".yaml")


def get_qa_chain(
    paper_details,
    tex_content,
    llm="gpt-3.5-turbo",
    embedding_model="text-embedding-ada-002",
    prompt_name: str = "pb",
):
    """
    Get the QA chain.

    Args:

    """

    prompt_template = get_prompt_template(prompt_name)
    retriever = _get_paper_retriever(paper_details, tex_content, embedding_model)
    llm = _get_llm(llm)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(
            context=(lambda x: _format_docs(x["raw_context"])),
        )
        | prompt_template
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {
            "raw_context": retriever,
            "question": RunnablePassthrough(),
        }
    ).assign(
        answer=rag_chain_from_docs,
        sources=(lambda x: _format_section_metadata(x["raw_context"])),
    )

    return rag_chain_with_source
