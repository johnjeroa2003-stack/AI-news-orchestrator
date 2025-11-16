# AI News Orchestrator (Prototype)

This project is a beginner-friendly prototype for the *AI News Orchestrator — Event Timeline Generator*.

## What's included
- Streamlit app (`app.py`) that loads articles (from NewsAPI or bundled sample) and builds a timeline.
- `fetcher.py` — fetches articles from NewsAPI or sample dataset.
- `analyzer.py` — builds a chronological timeline from article titles and content.
- `summarizer.py` — simple summarizer with placeholder for OpenAI integration.
- `sample_articles.json` — bundled sample dataset to run without API keys.
- `requirements.txt` — Python dependencies.

## How to run locally (VS Code)
1. Clone or unzip the project.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows PowerShell
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Create a `.env` file and add API keys:
   ```
   NEWSAPI_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```
5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
6. In the app, enter an event keyword, toggle "Use bundled sample dataset" if you don't have API keys.

## Notes for improvements (mentors will like these)
- Integrate an LLM (OpenAI/GPT/Gemini) for high-quality summarization and contradiction detection.
- Add NER with spaCy to extract names, locations, and more precise dates.
- Implement caching and a database (SQLite) to store fetched articles and incremental updates.
- Add a UI timeline visualization (Plotly Gantt or Mermaid).

## Files to hand in
- `app.py`, `fetcher.py`, `analyzer.py`, `summarizer.py`, `sample_articles.json`, `requirements.txt`, `README.md`, `.env.example`

