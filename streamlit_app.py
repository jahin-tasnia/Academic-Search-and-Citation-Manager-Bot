# streamlit_app.py
import streamlit as st
from agent import agent
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="Academic Search & Citation Manager", page_icon="📚", layout="centered"
)

st.title("📚 Academic Search & Citation Manager")

tabs = st.tabs(["🔎 Search", "🧾 DOI → Citations"])

# Search Tab

with tabs[0]:
    st.subheader("Search articles")
    q = st.text_input(
        "Query", placeholder="e.g., transformer interpretability healthcare 2022"
    )
    cols = st.columns(3)
    use_oa = cols[0].checkbox("OpenAlex", True)
    use_cr = cols[1].checkbox("Crossref", True)
    limit = st.slider("Results per source", 1, 10, 5)

    if st.button("Search"):
        if not q.strip():
            st.warning("Enter a query.")
        else:
            ask = "search: " + q.strip()
            hints = []
            if use_oa:
                hints.append("Use OpenAlex.")
            if use_cr:
                hints.append("Use Crossref.")

            ask += " " + " ".join(hints) + f" Limit each source to {limit}."
            with st.spinner("Searching…"):
                out = agent.invoke({"messages": [HumanMessage(content=ask)]})
            ai = next((m for m in reversed(out["messages"]) if m.type == "ai"), None)
            st.write(ai.content if ai else "No response.")

#  DOI → Citations Tab
with tabs[1]:
    st.subheader("Fetch & format by DOI")
    doi = st.text_input("DOI", placeholder="10.1145/3534678.3539479")
    formats = st.multiselect(
        "Formats", ["BibTeX", "RIS", "CSL-JSON"], default=["BibTeX", "CSL-JSON"]
    )

    if st.button("Generate"):
        if not doi.strip():
            st.warning("Enter a DOI.")
        else:
            with st.spinner("Fetching metadata…"):
                out_meta = agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=f"Resolve this DOI and prepare citations: {doi.strip()}"
                            )
                        ]
                    }
                )
            ai = next(
                (m for m in reversed(out_meta["messages"]) if m.type == "ai"), None
            )
            st.write(ai.content if ai else "No response.")
            st.caption(
                "Tip: Ask me for specific styles (APA/IEEE) and I’ll guide you using these exports."
            )
