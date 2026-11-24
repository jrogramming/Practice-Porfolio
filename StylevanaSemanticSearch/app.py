"""Streamlit interface for aesthetic based product discovery."""
import re

import streamlit as st

from stylevana_search import get_search, load_products

st.set_page_config(page_title="Product Discovery", page_icon="🌸", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cantarell:wght@400;700&display=swap');
    :root {
        --pink: #d95787;
        --deep-pink: #b83d6d;
        --soft-pink: #fff1f6;
        --line-pink: #f2c8d8;
    }
    html, body, [class*="st-"] { font-family: 'Cantarell', sans-serif; }
    .stApp { background: #fffafd; }
    [data-testid="stHeader"] { background: rgba(255, 250, 253, 0.92); }
    .block-container { max-width: 1180px; padding-top: 2rem; }
    h1, h2, h3 { color: #3f3f46; }
    .stApp, .stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] {
        color: #404047;
    }
    .stButton > button, .stLinkButton > a {
        background: var(--pink); color: #fff !important; border: 1px solid var(--pink);
        border-radius: 10px;
    }
    .stButton > button *, .stLinkButton > a * { color: #fff !important; }
    .stButton > button:hover, .stLinkButton > a:hover {
        background: var(--deep-pink); color: white; border-color: var(--deep-pink);
    }
    [data-testid="stTextInput"] input {
        border-color: var(--line-pink); background: white; color: #111 !important;
        -webkit-text-fill-color: #111;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-color: var(--line-pink); background: white;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: white; border-color: var(--line-pink) !important; border-radius: 14px;
        padding: 1rem 2.6rem 2rem;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] { background: var(--pink); }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Product Discovery")
st.caption("Find skincare and beauty products by the look, feel, or benefits you have in mind.")

with st.sidebar:
    st.header("Search settings")
    backend = st.selectbox("Ranking model", ["semantic", "tfidf"], format_func=lambda x: "Sentence Transformers" if x == "semantic" else "TF-IDF baseline")
    top_k = st.slider("Results", 3, 20, 10)
    products = load_products()
    def numeric_price(item):
        match = re.search(r"\d+(?:\.\d+)?", item.get("price", "").replace(",", ""))
        return float(match.group()) if match else None

    prices = [numeric_price(item) for item in products]
    prices = [price for price in prices if price is not None]
    if prices:
        min_price, max_price = min(prices), max(prices)
        price_range = st.slider(
            "Price range",
            min_value=float(min_price),
            max_value=float(max_price),
            value=(float(min_price), float(max_price)),
            step=1.0,
            format="$%.0f",
        )
    else:
        price_range = (0.0, float("inf"))
    st.caption(f"Catalog: {len(products):,} products")
query = st.text_input("What are you looking for?", placeholder="e.g. gentle sunscreen for sensitive skin")
if query:
    try:
        engine = get_search(backend)
        results = engine.search(query, len(engine.products))
        results = [
            item for item in results
            if (numeric_price(item) is not None
                and price_range[0] <= numeric_price(item) <= price_range[1])
        ][:top_k]
        if not results:
            st.info("No matching products found.")
        for item in results:
            with st.container(border=True):
                title_col, relevance = st.columns([0.84, 0.16], vertical_alignment="top")
                with title_col:
                    st.subheader(item["name"])
                with relevance:
                    st.markdown(
                        f"<div style='text-align:right;color:#b83d6d;font-size:0.82rem;white-space:nowrap;padding-top:0.5rem'>"
                        f"Relevance<br><strong>{item['score']:.3f}</strong></div>",
                        unsafe_allow_html=True,
                    )
                if item["brand"]:
                    st.caption(item["brand"])
                details, description = st.columns([0.28, 0.72], vertical_alignment="top")
                with details:
                    st.write(f"Rating: **{item['rating'] or 'not listed'}**")
                    st.write(f"Price: **{item['price'] or 'not listed'}**")
                with description:
                    if item["description"]:
                        st.write(item["description"][:420] + ("…" if len(item["description"]) > 420 else ""))
                    else:
                        st.caption("No scraped description available.")
                if item["url"]:
                    st.link_button("View on Stylevana", item["url"])
    except Exception as exc:
        st.error(str(exc))

st.divider()
st.caption("Demo uses scraped catalog data. Evaluation labels are keyword-based proxies; inspect README for methodology and limitations.")
