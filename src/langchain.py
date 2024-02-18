"""
Functions for langchain
"""

from langchain.prompts import PromptTemplate

bad_icebreaker_prompt_template = PromptTemplate.from_template(
    """You are a seasoned researcher, teacher and a popularizer of science that can explain scientific concepts to the wide variety of audiences.
    You will be given an abstract of a scientific paper, an audience (e.g. high-school students) and a language, and you will have to explain the scientific paper it in a way that is understandable for the audience and translate that explanation to given language. 
    Please be concise and clear, make a summary and few bulletpoints. Please only include the translation without any introductory sentences.

    Audience: {audience}.

    Language: {language}.

    Abstract: {abstract}
    """
)

icebreaker_prompt_template = PromptTemplate.from_template(
    """
Imagine you're explaining a cool science discovery to a person from {audience} in {language} language.

Briefly introduce the paper's topic in a way that would grab their attention.
Explain the main question or problem the researchers were trying to answer in a simple and understandable way.
Describe what the researchers did to investigate the question (e.g., experiments, observations, etc.).
Summarize the key findings of the research in a way that would surprise or excite your audience.
Briefly mention any limitations or future directions of the research, if relevant.
Conclude by emphasizing the importance or potential impact of the findings in a language they can understand.

Remember:

Use simple language and avoid technical jargon (unless the topic of the paper is meant for that audience).
Focus on the most interesting and engaging aspects of the research.
Keep the summary concise and to the point (e.g., 3-5 sentences).
Use {language} language.

Tips:

You can use metaphors, analogies, or relatable examples to explain complex concepts.
Encourage questions and be prepared to explain things in more detail if needed.
Make it fun and engaging!

Optional:

You can also personalize the prompt based on the specific details of the paper you're summarizing. For example, if the research has implications for everyday life, you can highlight those in your summary.
I hope this template helps you write clear and engaging summaries of scientific paper abstracts for your chosen audience!

Abstract:

{abstract}
"""
)
