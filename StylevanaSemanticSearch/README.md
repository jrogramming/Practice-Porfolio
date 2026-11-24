# ♠ &nbsp; Stylevana Product Discovery &nbsp; ♠

<p align="center">
  <em>A semantic search app for exploring a scraped catalog of Stylevana beauty products.</em>
</p>

---

### &nbsp; ♜ &nbsp; ABOUT THE PROJECT

Stylevana Product Discovery searches product titles, brands, attributes, and scraped descriptions using natural-language queries. The Streamlit interface ranks products with Sentence Transformer embeddings and includes a TF-IDF baseline for comparison.

The source file, `stylevana-raw.csv`, contains 360 scraped product listings. Since the scrape has no human relevance judgments, the included evaluation uses transparent keyword-based relevance proxies.

---

### &nbsp; ♛ &nbsp; FEATURES

- Search the catalog with natural-language queries.
- Switch between Sentence Transformer and TF-IDF ranking.
- Filter search results by product price range.
- View product brand, rating, price, scraped description, and relevance score.
- Open the matching product page on Stylevana.
- Compare ranking approaches with Precision@5, Recall@10, and nDCG@10.

---

### &nbsp; ♞ &nbsp; HOW IT WORKS

1. The loader reads the CSV, cleans whitespace and `#NAME?` scraper artifacts, and drops rows without a product name.
2. It combines each product's name, brand, attributes, and description into search text. Missing descriptions leave a title and brand based document.
3. Sentence Transformers encodes the products with `sentence-transformers/all-MiniLM-L6-v2`. Normalized embeddings are ranked by cosine similarity.
4. The TF-IDF option uses unigram and bigram features with cosine similarity.
5. The app applies the selected price range to ranked results and displays up to the requested number of products.

The evaluation runs six fixed skincare queries against both ranking methods. Product relevance is assigned by matching query-specific terms to product names, descriptions, and attributes. These weak labels make the comparison repeatable, but they are not a substitute for human judgments and can favor literal keyword matches.

---

### &nbsp; ♜ &nbsp; GETTING STARTED

Use Python 3.10 or newer. From the project folder, create and activate a virtual environment, then install the dependencies:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the web app:

```powershell
python -m streamlit run app.py
```

The first semantic search downloads the Sentence Transformer model from Hugging Face. The interface also loads Cantarell from Google Fonts; if external fonts are unavailable, it falls back to the system sans-serif font.

Run a terminal search:

```powershell
python stylevana_search.py "gentle sunscreen for sensitive skin" --top 5
python stylevana_search.py "hydrating barrier cream" --backend tfidf
```

Run the TF-IDF versus Sentence Transformer evaluation:

```powershell
python stylevana_search.py --evaluate
```

---

### &nbsp; ♞ &nbsp; UNDERSTANDING THE CODE

| File or function | Responsibility |
|:---|:---|
| `app.py` | Streamlit interface, ranking selector, price filter, and product result cards. |
| `load_products()` | Reads and cleans the scraped CSV; prepares searchable product records. |
| `ProductSearch` | Fits TF-IDF or creates Sentence Transformer embeddings, then ranks products. |
| `evaluate()` | Compares mean Precision@5, Recall@10, and nDCG@10 across the proxy query set. |
| `stylevana-raw.csv` | Original Stylevana Web Scraper export used by the app. |

---

### &nbsp; ♦ &nbsp; EVALUATION NOTES

The included benchmark is a lightweight, reproducible comparison rather than a validated quality score. Relevance is inferred from keyword rules because the dataset has no human-labeled query–product pairs. Scrape gaps, generic query terms, and shared product-title words can affect the results. For a stronger evaluation, judge a representative set of query–product pairs and use those judgments as relevance labels.

---

### &nbsp; ♣ &nbsp; TECHNOLOGIES

| Technology | Role |
|:---|:---|
| Python | Data preparation, retrieval, ranking metrics, and application logic. |
| Streamlit | Interactive search interface. |
| Sentence Transformers | Deep-learning text embeddings for semantic retrieval. |
| scikit-learn | TF-IDF vectorization and cosine similarity. |
| NumPy | Similarity ranking and metric calculations. |
| Stylevana Web Scraper export | Source product catalog in CSV format. |

---

<p align="center">
  <em>Jrogramming's Workshop — Consistent structure, individual projects.</em>
</p>
