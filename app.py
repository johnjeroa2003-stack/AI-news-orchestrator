import os
import streamlit as st
from fetcher import NewsFetcher, load_sample_articles
from analyzer import TimelineBuilder
from summarizer import Summarizer

st.set_page_config(page_title="AI News Orchestrator", layout="wide")

st.title("AI News Orchestrator — Event Timeline Generator")
st.write("Enter an event/topic and the app will fetch articles, extract milestones, and build a timeline.")

col1, col2 = st.columns([3,1])
with col1:
    query = st.text_input("Event title or keywords (e.g., 'Chandrayaan-3 mission')", value="Chandrayaan-3")
    max_articles = st.slider("Max articles to fetch", 1, 20, 8)
    use_sample = st.checkbox("Use bundled sample dataset (no API keys)", value=False)
    provider = st.selectbox("API Provider (if not using sample)", ["newsapi.org"], index=0)
with col2:
    st.markdown("### API keys & options")
    st.text("Provide API keys as environment variables:")
    st.code("NEWSAPI_KEY=your_key_here", language="bash")
    st.markdown("---")
    st.markdown("Outputs")
    show_sources = st.checkbox("Show source authenticity checks", value=True)

if not query:
    st.info("Type an event or keywords to begin.")
    st.stop()

# Fetch articles
if use_sample:
    st.success("Loading sample articles from bundled dataset.")
    articles = load_sample_articles(limit=max_articles)
else:
    api_key = os.environ.get("NEWSAPI_KEY", "")
    if not api_key:
        st.warning("No NEWSAPI_KEY found in environment — using bundled sample dataset instead.")
        articles = load_sample_articles(limit=max_articles)
    else:
        fetcher = NewsFetcher(api_key=api_key)
        with st.spinner("Fetching articles..."):
            articles = fetcher.fetch(query=query, limit=max_articles)

st.write(f"Found **{len(articles)}** articles.")

# Basic source list
if st.checkbox("Show fetched article list", value=False):
    for i, a in enumerate(articles, 1):
        st.markdown(f"**{i}. {a.get('title','(no title)')}** — {a.get('source','(unknown)')} — {a.get('publishedAt','')}")
        st.write(a.get("url", ""))

# Analyze and build timeline
builder = TimelineBuilder(articles)
timeline = builder.build_timeline()

st.header("Event Timeline")
for item in timeline:
    st.markdown(f"- **{item['date']}** → {item['event']}")
    if "sources" in item:
        st.caption("Sources: " + ", ".join(item["sources"]))

st.header("Combined Summary")
summ = Summarizer()
summary_text = summ.summarize_timeline(timeline, context_articles=articles)
st.write(summary_text)

if show_sources:
    st.header("Source authenticity / quick checks")
    checks = builder.source_checks()
    for src, score in checks.items():
        st.markdown(f"- **{src}** — authenticity score: **{score:.2f}**")

st.markdown("---")
st.markdown("### Notes")
st.write(
    """
This is a prototype. For better summaries and fact-checking, provide an OpenAI API key (or other LLM) and enable advanced summarization in `summarizer.py`.
See README.md for setup, running, and packaging instructions.
"""
)
