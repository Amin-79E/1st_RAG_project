# Local RAG Restaurant Review Assistant

A local RAG setup that answers questions about a restaurant based on its actual customer reviews, instead of just whatever the model already "knows." Everything runs on my machine through ollama.

## What it does

I embed a set of restaurant reviews into a local vector database. When an inquiry is provided, it pulls the reviews that are actually relevant and hands them to the LLM to answer with, meaning: the answer is grounded in real  text rather than the model guessing .

## Tech stack

- **LLM**: `llama3.2` (3B)
- **Embeddings**: `mxbai-embed-large`
- **Vector store**: [Chroma](https://www.trychroma.com/) persisted locally in `chrome_langchain_db/`
- **Glue**: [LangChain](https://www.langchain.com/) (`langchain-ollama`, `langchain-chroma`, `langchain-core`)
- **Data**: a CSV of restaurant reviews: title, review text, rating, date

## How it works

1. `vector.py` reads the CSV with pandas, turns each row into a LangChain `Document`, and embeds them into Chroma. After that it just loads what's already there.
2. `main.py` the prompt: play the role of a restaurant expert, answer only from the reviews given, and say so if the reviews don't cover it rather than making something up. 
i.e It takes your question, grabs the closest matching reviews, and feeds everything to the model.
3. It's just a loop in the terminal and ask something, get an answer, type `q` when you want o quit the program.

## Setup

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

ollama pull llama3.2
ollama pull mxbai-embed-large
```

## Known limitations

I ran into a few things while testing this that are worth being upfront about:

- **Bad/inaccurate retrieval.** Even a question totally unrelated to the restaurant ("hey", "what's the weather") still gets matched against the reviews by vector similarity. The model usually notices the context doesn't fit and says so, but nothing's actually stopping a bad match from being retrieved in the first place.
- **It hallucinates.** Early on, I asked about the restaurant's name and it made one up in fact twice twice, with two different guesses even though the reviews never mention a name. It even contradicted its own earlier answer in the same conversation. I tightened the prompt to explicitly say "don't guess, say if it's not there," which helped a lot, but it's not a guarantee. Prompting alone can't fully stop this as repeated testing proved.

## Where I'd take this next

- A similarity threshold, so it skips retrieval (or just says "I don't know") when nothing's a good enough match.
- Some kind of check before retrieval even runs, to catch questions that clearly aren't about the restaurant at all.
- Actual evaluation of retrieval quality.
