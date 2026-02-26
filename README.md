# Academic Search & Citation Manager Bot

An AI-powered assistant that helps students and faculty search for academic papers and generate citations — built with a LangGraph ReAct agent, Groq LLM, and a Streamlit web UI.

---

## What it does

You type a research topic or paste a DOI, and the bot:
- Searches **OpenAlex** and **Crossref** for relevant academic papers
- Returns titles, authors, year, and DOI/URL for each result
- Fetches full metadata for any paper when you provide its DOI
- Generates ready-to-use **BibTeX** citation entries

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Llama 3.3 70B via [Groq](https://groq.com) |
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) ReAct agent |
| LLM Orchestration | [LangChain](https://github.com/langchain-ai/langchain) |
| UI | [Streamlit](https://streamlit.io) |
| Paper Search APIs | [OpenAlex](https://openalex.org) · [Crossref](https://crossref.org) |

---

## Project Structure

```
Academic-Search-and-Citation-Manager-Bot/
│
├── agent.py          # LangGraph ReAct agent setup + system prompt
├── tools.py          # 4 LangChain tools: search, DOI fetch, BibTeX generator
├── utils.py          # LLM initialization (Groq + Llama 3.3)
├── streamlit_app.py  # Streamlit web UI (Search tab + DOI tab)
├── runapp.py         # Launcher: checks env/deps then starts Streamlit
├── test_import.py    # Smoke test for agent import
└── requirements.txt  # Python dependencies
```

---

## How it works

The agent follows a **ReAct** (Reason + Act) loop:

1. User sends a query (e.g., *"search: graph neural networks healthcare 2021"*)
2. The LLM decides which tool(s) to call
3. Tool results are fed back to the LLM
4. The LLM formats a final answer

### Tools

| Tool | Description |
|------|-------------|
| `openalex_search` | Searches OpenAlex by keyword, returns top 5 papers |
| `crossref_search` | Searches Crossref by keyword/title/author, returns top 5 papers |
| `fetch_by_doi` | Fetches full paper metadata from Crossref using a DOI |
| `make_bibtex` | Converts metadata JSON into a formatted BibTeX entry |

---

## UI

Two tabs in the Streamlit app:

**Search tab**
- Enter any keyword query (topic, author, year, etc.)
- Toggle OpenAlex and/or Crossref as sources
- Adjust result count per source (1–10)

**DOI → Citations tab**
- Paste any DOI (e.g., `10.1145/3534678.3539479`)
- Choose output formats: BibTeX, RIS, CSL-JSON
- Get formatted citation output instantly

---

## Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/jahin-tasnia/Academic-Search-and-Citation-Manager-Bot.git
cd Academic-Search-and-Citation-Manager-Bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 4. Run the app

```bash
python runapp.py
```

Or directly:

```bash
streamlit run streamlit_app.py
```

---

## Example Queries

| What you type | What happens |
|---------------|-------------|
| `search: transformer models NLP 2023` | Searches OpenAlex + Crossref, lists top papers |
| `search: attention mechanism Vaswani` | Finds papers by author + keyword |
| DOI: `10.1145/3534678.3539479` | Fetches metadata and generates BibTeX |

---

## Dependencies

```
langchain
langchain_core
langchain-groq
langgraph
pydantic
python-dotenv
requests
streamlit
rich
```

---

## Why I built this

Manually searching across databases and formatting citations is tedious. This project automates that entire workflow — from keyword search to a copy-paste-ready BibTeX entry — using a conversational AI agent that calls real academic APIs under the hood.
