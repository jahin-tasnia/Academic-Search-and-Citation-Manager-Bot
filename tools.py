import json, requests
from langchain_core.tools import tool


# OpenAlex Search


@tool()
def openalex_search(query: str):
    """Search OpenAlex for academic papers by keyword."""
    try:
        r = requests.get(
            "https://api.openalex.org/works",
            params={"search": query, "per_page": 5, "sort": "relevance_score:desc"},
            timeout=10,
        )
        r.raise_for_status()
        items = []
        for w in r.json().get("results", []):
            items.append(
                {
                    "title": w.get("title"),
                    "authors": [
                        a["author"]["display_name"] for a in w.get("authorships", [])
                    ],
                    "year": (w.get("publication_year") or ""),
                    "doi": w.get("doi") or "",
                    "url": w.get("primary_location", {}).get("landing_page_url", ""),
                }
            )
        return json.dumps(items, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Crossref Search
@tool()
def crossref_search(query: str):
    """Search Crossref for papers by title, author, or keyword."""
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params={"query": query, "rows": 5},
            timeout=10,
        )
        r.raise_for_status()
        items = []
        for it in r.json().get("message", {}).get("items", []):
            title = " ".join(it.get("title", []))
            authors = [
                f"{a.get('family','')}, {a.get('given','')}"
                for a in it.get("author", [])[:3]
            ]
            items.append(
                {
                    "title": title,
                    "authors": authors,
                    "year": it.get("issued", {}).get("date-parts", [[None]])[0][0],
                    "doi": it.get("DOI", ""),
                    "url": f"https://doi.org/{it.get('DOI', '')}",
                }
            )
        return json.dumps(items, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Fetch Metadata by DOI
@tool()
def fetch_by_doi(doi: str):
    """Fetch detailed metadata for a paper using DOI."""
    try:
        r = requests.get(f"https://api.crossref.org/works/{doi.strip()}", timeout=10)
        r.raise_for_status()
        it = r.json().get("message", {})
        meta = {
            "title": " ".join(it.get("title", [])),
            "authors": [
                f"{a.get('family','')}, {a.get('given','')}"
                for a in it.get("author", [])
            ],
            "year": it.get("issued", {}).get("date-parts", [[None]])[0][0],
            "journal": (it.get("container-title") or [""])[0],
            "doi": it.get("DOI", ""),
            "url": f"https://doi.org/{it.get('DOI', '')}",
        }
        return json.dumps(meta, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Generate BibTeX


@tool()
def make_bibtex(metadata_json: str):
    """Convert metadata JSON to a BibTeX entry."""
    try:
        m = json.loads(metadata_json)
        authors = " and ".join(m.get("authors", []))
        bib = f"""@article{{{m.get('doi','').replace('/','_')},
  title={{ {m.get('title','')} }},
  author={{ {authors} }},
  year={{ {m.get('year','')} }},
  journal={{ {m.get('journal','')} }},
  doi={{ {m.get('doi','')} }},
  url={{ {m.get('url','')} }}
}}"""
        return bib
    except Exception as e:
        return f"Error: {e}"
