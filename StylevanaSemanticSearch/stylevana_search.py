"""Semantic and TF-IDF search over the Stylevana scraped product catalog."""
from __future__ import annotations

import argparse
import csv
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_DATA = Path(__file__).with_name("stylevana-raw.csv")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _clean(value: str | None) -> str:
    value = (value or "").replace("#NAME?", " ")
    return re.sub(r"\s+", " ", value).strip()


def load_products(path: str | Path = DEFAULT_DATA) -> list[dict]:
    """Load and normalize the scraper export, dropping rows without a name."""
    products = []
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            name = _clean(row.get("item_page_title") or row.get("data"))
            if not name:
                continue
            description = _clean(row.get("undefined10"))
            brand = _clean(row.get("undefined11"))
            attrs = " ".join(filter(None, (_clean(row.get("title")), _clean(row.get("undefined12")))))
            rating = _clean(row.get("ratingValue"))
            # Repeat title/brand to retain product identity when descriptions are sparse.
            text = " ".join(filter(None, (name, name, brand, attrs, description)))
            products.append({
                "name": name, "brand": brand, "description": description,
                "attributes": attrs, "rating": rating,
                "price": _clean(row.get("price2") or row.get("price")),
                "url": _clean(row.get("item_page_link")), "text": text,
            })
    return products


class ProductSearch:
    def __init__(self, products: list[dict], backend: str = "semantic", model_name: str = MODEL_NAME):
        if backend not in {"semantic", "tfidf"}:
            raise ValueError("backend must be 'semantic' or 'tfidf'")
        self.products, self.backend = products, backend
        self.documents = [p["text"] for p in products]
        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
            self.matrix = self.vectorizer.fit_transform(self.documents)
        else:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError("Install dependencies with `pip install -r requirements.txt` to use semantic search.") from exc
            self.model = SentenceTransformer(model_name)
            self.matrix = self.model.encode(self.documents, normalize_embeddings=True, show_progress_bar=False)

    def search(self, query: str, k: int = 10) -> list[dict]:
        if not query.strip():
            return []
        if self.backend == "tfidf":
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.matrix).ravel()
        else:
            query_vec = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
            scores = np.asarray(self.matrix) @ query_vec
        indices = np.argsort(-scores)[:max(0, k)]
        return [{**self.products[i], "score": float(scores[i])} for i in indices]


@lru_cache(maxsize=2)
def get_search(backend: str = "semantic") -> ProductSearch:
    return ProductSearch(load_products(), backend)


# Weak labels based on transparent product-text keyword matching. These are
# evaluation proxies, not human judgments or clinical skincare recommendations.
EVAL_QUERIES = {
    "gentle sunscreen for sensitive skin": ("sunscreen", "sun lotion", "spf", "sun cream"),
    "hydrating moisturizer for dry skin": ("moistur", "hydrating", "hydration", "cream", "dry skin"),
    "centella calming skincare": ("centella", "cica", "soothing", "calming"),
    "vitamin c brightening serum": ("vitamin c", "brightening", "dark spot", "serum"),
    "cleansing oil for removing makeup": ("cleansing oil", "cleansing balm", "makeup remover", "cleansing"),
    "acne care with salicylic acid": ("salicylic", "acne", "blemish", "pore"),
}


def is_relevant(product: dict, terms: Iterable[str]) -> bool:
    haystack = (product["name"] + " " + product["description"] + " " + product["attributes"]).lower()
    return any(term in haystack for term in terms)


def ranking_metrics(ranked: list[dict], relevant: set[str], total_relevant: int, k: int = 10) -> dict[str, float]:
    ids = [p["name"] for p in ranked]
    hits = [1 if name in relevant else 0 for name in ids]
    p5 = sum(hits[:5]) / 5
    recall = sum(hits[:k]) / total_relevant if total_relevant else 0.0
    dcg = sum(hit / np.log2(i + 2) for i, hit in enumerate(hits[:k]))
    ideal = sum(1 / np.log2(i + 2) for i in range(min(total_relevant, k)))
    return {"precision@5": p5, "recall@10": recall, "ndcg@10": dcg / ideal if ideal else 0.0}


def evaluate(products: list[dict], model_name: str = MODEL_NAME) -> dict:
    searches = {"TF-IDF": ProductSearch(products, "tfidf"), "Sentence Transformer": ProductSearch(products, "semantic", model_name)}
    per_backend = {}
    for label, engine in searches.items():
        values = []
        for query, terms in EVAL_QUERIES.items():
            relevant = {p["name"] for p in products if is_relevant(p, terms)}
            values.append(ranking_metrics(engine.search(query, 10), relevant, len(relevant)))
        per_backend[label] = {metric: float(np.mean([row[metric] for row in values])) for metric in values[0]}
    return per_backend


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="natural-language product query")
    parser.add_argument("--backend", choices=("semantic", "tfidf"), default="semantic")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--evaluate", action="store_true", help="compare both models on the included proxy query set")
    args = parser.parse_args()
    products = load_products(args.data)
    if args.evaluate:
        for label, metrics in evaluate(products).items():
            print(f"{label}: " + " | ".join(f"{k}={v:.3f}" for k, v in metrics.items()))
        return
    query = " ".join(args.query).strip()
    if not query:
        parser.error("provide a query or use --evaluate")
    for i, p in enumerate(ProductSearch(products, args.backend).search(query, args.top), start=1):
        print(f"{i:>2}. {p['name']}  [score={p['score']:.3f}]  {p['price']}  {p['url']}")


if __name__ == "__main__":
    main()
