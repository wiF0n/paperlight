# PaperLight 📜🔦👀: Let's Shine a Light on Science

# About

PaperLight is a project to create a AI-powered web-based app for the exploration and visualization of scientific papers. The goal is to provide a tool that can help people to find and understand the scientific papers of their choice.

The project started as a demonstration app for the workshop [End-to-End AI App Engineering with Open Source](https://www.meetup.com/machine-learning-meetup-kosice/events/298773899/), and it's secondary goal is to serve as a learning resource on AI-powered applications for (not only) the workshop participants.


## Features

- You can find papers of your interest based on your search criteria.

- **Icebreaker**:  Summarize the papers (based on their abstract) in a way that makes it easy to understand what they are about. You can choose the audience level of the summary (e.g. high-school, college, university students), and also a language of the summary (e.g. English, Slovak).

- **Paper Buddy**: A tool that allows you to view the papers and ask questions about them. The questions are answered by the AI agents, and the answers are based on the content of the papers. 

## Main tools and technologies

- **App**: [streamlit](https://streamlit.io/)
- **Data**: [arxiv](https://arxiv.org/), [astrophsics data system](https://ui.adsabs.harvard.edu/), 
- **Gen AI framework**: [langchain](https://python.langchain.com/docs/get_started/introduction)
- **LLM and Embedding models**: [openai](https://openai.com/)

## Current state

This project is currently in the early stages of development. The core functionality is tested on a small number of papers, and the user interface still needs to be improved. So you can expect to see some bugs, inconsistencies, and inaccuracies both in code and results.

Additionaly, only arxiv and astrophysics data system are currently supported as paper sources.

## Possible enhancements

- **More paper sources**: Add support for more paper sources (e.g. PubMed)
- **Chat history**: Add a chat history to the internal prompt of the Paper Buddy tool. This would allow LLM to not only take into account the current question and the paper content, but also the previous questions and answers. 

 
## How to run the app

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Install the requirements: `pip install -r requirements.txt`
4.  
    - Create [Google project](https://console.cloud.google.com/projectcreate)
    - Enable [Custom Search API](https://console.cloud.google.com/apis/api/customsearch.googleapis.com)
    - Create new [Google API key](https://console.cloud.google.com/apis/credentials).
    - Create new [Google Custom Search Engine](https://programmablesearchengine.google.com/controlpanel/create) (CSE) and get the CSE ID. Enable only the arxiv (\*.arxiv.org/abs/\*) and astrophysics data system (\*.ui.adsabs.harvard.edu/abs/\*) domains.
    - Create an [OpenAI API key]().
5. Create .env file in the root of this repo with the following content:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CSE_ID=your_google_cse_id
GOOGLE_API_KEY=your_google_api_key
```
6. Run the app: `streamlit run 1_📜🔦👀_About_Paperlight.py`
7. Open the app in your browser: `http://localhost:8501/`
8. Enjoy!
