# Persian Information Retrieval System

A comprehensive information retrieval system designed for Persian (Farsi) text documents. This project implements both traditional inverted index-based retrieval with TF-IDF ranking and modern BERT-based semantic search capabilities.

---

## Features

### Core Retrieval System
- **Inverted Index Construction** — Builds an inverted index from JSON document collections with term frequencies and positional information
- **Champion Lists** — Implements champion list optimization for faster query processing
- **TF-IDF Ranking** — Calculates cosine similarity between queries and documents using TF-IDF weighting
- **Persian Text Processing** — Full support for Persian language normalization, tokenization, and stemming

### Advanced Features (Bonus)
- **BERT-based Semantic Search** — Uses Persian BERT model (`bert-fa-zwnj-base`) for embedding-based retrieval
- **Document Clustering** — KMeans clustering of document embeddings for efficient search
- **FAISS Integration** — Fast approximate nearest neighbor search using Facebook's FAISS library

---

## Project Structure

```
information-retrieval/
├── main.py                 # Main entry point and demo scripts
├── common/
│   └── types.py            # TypedDict definitions (Document, Posting, Posting_List)
├── invertedindex/
│   └── __init__.py         # Inverted index creation and champion list generation
├── linguisticmodule/
│   └── __init__.py         # Persian text normalization, tokenization, stemming
├── retrievingmodule/
│   └── __init__.py         # TF-IDF cosine similarity calculation
└── bert/                   # BERT-based retrieval modules (bonus)
    ├── retrievingmodule.py
    ├── clusteringmodule.py
    └── faiss.py
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Dependencies

```bash
pip install parsivar transformers torch faiss-cpu scikit-learn
```

| Package | Purpose |
|---------|---------|
| `parsivar` | Persian NLP toolkit for stemming |
| `transformers` | Hugging Face library for BERT models |
| `torch` | PyTorch backend for transformers |
| `faiss-cpu` | Facebook AI Similarity Search |
| `scikit-learn` | KMeans clustering |

---

## Usage

### Basic Usage (Inverted Index Search)

```python
from invertedindex import create_inverted_index, create_champion_lists
from retrievingmodule import calculate_cosine_similarity_for_query
from linguisticmodule import tokenize_document

# Build the inverted index from your document collection
inverted_index, docs = create_inverted_index('Data/IR_data_news_12k.json')

# Create champion lists for faster retrieval
champion_lists = create_champion_lists(inverted_index, k=10)

# Process and search
query = "متن جستجوی شما"
query_tokens = tokenize_document(query)

results = calculate_cosine_similarity_for_query(
    inverted_index, 
    docs, 
    query_tokens, 
    number_of_results=10,
    champion_lists=champion_lists,
    use_champion_list=True
)

for doc_id, title, similarity, snippets in results:
    print(f"Document: {title}")
    print(f"Similarity: {similarity:.4f}")
    print(f"Snippets: {snippets}")
```

### Interactive Mode

Run the main script for interactive querying:

```bash
python main.py
```

Enter your query when prompted, and the system will return the top matching documents with their similarity scores and relevant snippets.

---

## Modules

### Linguistic Module (`linguisticmodule`)

Handles Persian text preprocessing:

- **Normalization** — Converts Arabic characters to Persian equivalents (ك→ک, ي→ی), handles half-spaces (نیم‌فاصله), removes diacritics
- **Tokenization** — Splits text into individual tokens
- **Stemming** — Reduces words to their root form using Parsivar's `FindStems`

### Inverted Index (`invertedindex`)

Creates and manages the inverted index:

- **`create_inverted_index(path)`** — Builds inverted index from JSON documents, automatically removes top 50 most frequent terms (stopword-like behavior)
- **`create_champion_lists(inverted_index, k)`** — Creates champion lists containing top-k documents for each term based on term frequency

### Retrieving Module (`retrievingmodule`)

Implements TF-IDF based retrieval:

- **`calculate_cosine_similarity_for_query(...)`** — Computes cosine similarity between query and documents using TF-IDF weighting
- Supports both full index and champion list-based retrieval
- Returns document snippets showing query term context

---

## Data Format

The system expects documents in JSON format:

```json
{
  "0": {
    "title": "عنوان خبر",
    "content": "متن کامل خبر...",
    "tags": ["تگ۱", "تگ۲"],
    "date": "1402/01/01",
    "url": "https://example.com/news/1",
    "category": "سیاسی"
  },
  "1": {
    ...
  }
}
```

---

## Algorithm Details

### TF-IDF Calculation
- **Term Frequency (TF)**: `1 + log₂(term_freq)`
- **Inverse Document Frequency (IDF)**: `log((1 + N) / (1 + df)) + 1`
- **Cosine Similarity**: Normalized dot product of query and document TF-IDF vectors

### Champion Lists
Champion lists store only the top-k documents (by term frequency) for each term, significantly reducing computation time for queries while maintaining good retrieval quality.

---

## License

This project is developed for educational purposes as part of an Information Retrieval course.

---

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
