import os, textwrap

class Summarizer:
    def __init__(self, openai_api_key=None):
        # If OPENAI_API_KEY provided in env, the code demonstrates how to call it.
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")

    def summarize_timeline(self, timeline, context_articles=None):
        """
        A lightweight summarizer: concatenates top timeline events into a readable paragraph.
        If OPENAI_API_KEY is set, this function shows where you'd call the API (commented).
        """
        if not timeline:
            return "No timeline events to summarize."

        # If OpenAI key present, you can integrate an LLM call here (example commented).
        if self.openai_api_key:
            # Example (commented) - user must install openai and set key:
            # import openai
            # openai.api_key = self.openai_api_key
            # prompt = "Given the following timeline entries, produce a concise summary:\\n" + "\\n".join([f\"{t['date']} -> {t['event']}\" for t in timeline])
            # resp = openai.Completion.create(model='gpt-4o-mini', prompt=prompt, max_tokens=200)
            # return resp['choices'][0]['text'].strip()
            pass

        # Fallback simple summarization
        top = timeline[:6]
        lines = [f"{t['date']}: {t['event']}" for t in top]
        para = " | ".join(lines)
        # wrap nicely
        return textwrap.fill("Combined summary — " + para, width=100)
