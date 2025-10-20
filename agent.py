from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from utils import llm
from tools import (
    openalex_search,
    crossref_search,
    fetch_by_doi,
    make_bibtex,
)

agent = create_react_agent(
    name="StudentFacultyCitationBot",
    tools=[
        openalex_search,
        crossref_search,
        fetch_by_doi,
        make_bibtex,
    ],
    model=llm,
    prompt="""You are an academic search and citation assistant for students and faculty.
Never give any salutation.
Be concise but precise. Bullet when helpful.
ALWAYS try tools before answering.

Core behaviors:
- If user asks to "search", call one or more of: openalex_search, crossref_search
- If user gives a DOI, first call fetch_by_doi, then produce citation outputs.
- If user asks for citations, call make_bibtex with the metadata you have.
- If a tool returns nothing, say so clearly and suggest changing keywords or adding author/year.

Output rules:
- For search: show top items with: title, authors, year, DOI/URL.
- For citations: print code-fenced blocks with correct format labels (BibTeX/RIS/CSL-JSON).
""",
)


if __name__ == "__main__":

    resp = agent.invoke(
        {
            "messages": [
                HumanMessage(content="search: graph neural networks healthcare 2021")
            ]
        }
    )
    print(resp["messages"][-1].content)
