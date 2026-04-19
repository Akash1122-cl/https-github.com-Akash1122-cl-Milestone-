"""
scripts/index.py — Phase 13: Chunking & Embedding Pipeline
===========================================================
Reads targeted_schemes.json produced by ingest.py,
converts each record into semantically-coherent text chunks, generates
384-dim embeddings via BAAI/bge-small-en-v1.5 (sentence-transformers),
and upserts every chunk into the correct ChromaDB collection (one per AMC).

All processing logic uses local embedding creation but syncs to Chroma Cloud vector DB.

Dependencies:
    pip install chromadb sentence-transformers python-dotenv
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()

# ── Third-party imports ────────────────────────────────────────────────────────
try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    sys.exit("❌  chromadb not installed. Run: pip install chromadb")




# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

DATA_RAW_DIR      = "data/raw"
MANIFEST_PATH     = os.path.join(DATA_RAW_DIR, "targeted_schemes.json")

# Chroma Cloud keys
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT  = os.getenv("CHROMA_TENANT", "default_tenant")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "default_database")

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
EMBED_DIMS  = 384
BATCH_SIZE  = 100   # chunks per upsert call

# The 6 factual fields extracted by ingest.py and their human-readable labels
FACTUAL_FIELDS: dict[str, str] = {
    "nav":           "Current NAV",
    "min_sip":       "Minimum SIP amount",
    "fund_size_aum": "Fund size (AUM)",
    "expense_ratio": "Expense ratio",
    "exit_load":     "Exit load",
    "rating":        "Rating",
}

# AMC keyword → ChromaDB collection name mapping
# Collection names must be 3-63 chars, start/end with alphanumeric, no spaces
AMC_COLLECTION_MAP: list[tuple[str, str]] = [
    ("icici",  "icici_prudential"),
    ("axis",   "axis_mf"),
    ("nippon", "nippon_india"),
    ("aditya", "aditya_birla"),
    ("birla",  "aditya_birla"),
    ("absl",   "aditya_birla"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Helper: Collection Name Resolver
# ─────────────────────────────────────────────────────────────────────────────

def resolve_collection(scheme_name: str, source_url: str) -> str:
    """
    Derives the ChromaDB collection name from scheme name or URL
    by matching known AMC keywords (case-insensitive).
    Falls back to 'general' for unrecognised AMCs.
    """
    text = (scheme_name + " " + source_url).lower()
    for keyword, collection in AMC_COLLECTION_MAP:
        if keyword in text:
            return collection
    return "general"


# ─────────────────────────────────────────────────────────────────────────────
# Helper: Stable Chunk ID Builder
# ─────────────────────────────────────────────────────────────────────────────

def build_chunk_id(scheme_name: str, field: str, last_updated: str, suffix: str = "") -> str:
    """
    Builds a deterministic, URL-safe chunk ID from key metadata fields.
    Upserting to ChromaDB with the same ID overwrites stale embeddings.

    Format:  <scheme_slug>-<field>-<date>[-<suffix_hash>]
    Example: axis-large-cap-fund-exit_load-2026-04-14
    """
    slug = re.sub(r"[^a-z0-9]+", "-", scheme_name.lower()).strip("-")
    base = f"{slug}-{field}-{last_updated}"
    if suffix:
        short_hash = hashlib.md5(suffix.encode()).hexdigest()[:6]
        base = f"{base}-{short_hash}"
    return base[:200]   # ChromaDB ID limit


# ─────────────────────────────────────────────────────────────────────────────
# Stage 1A — Chunk Manifest JSON (Structured Factual Data)
# ─────────────────────────────────────────────────────────────────────────────

def chunk_manifest_record(record: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Converts one manifest record into self-contained natural-language sentences,
    one per factual field. Each sentence becomes a standalone chunk with full
    metadata so the RAG retriever can filter by field or scheme directly.

    Returns a list of chunk objects:
    {
        "id":         str,
        "text":       str,
        "metadata":   dict,
        "collection": str
    }
    """
    scheme     = record.get("scheme_name", "Unknown Scheme")
    url        = record.get("source_url", "")
    updated    = record.get("last_updated", "N/A")
    collection = resolve_collection(scheme, url)

    chunks: list[dict[str, Any]] = []

    for field_key, field_label in FACTUAL_FIELDS.items():
        raw_value = record.get(field_key, "N/A")

        # Skip fields that were not scraped
        if not raw_value or raw_value == "N/A":
            continue

        # Natural-language sentence for high-quality embedding
        text = f"The {field_label.lower()} for {scheme} is {raw_value}."

        chunk = {
            "id": build_chunk_id(scheme, field_key, updated),
            "text": text,
            "metadata": {
                "scheme_name":  scheme,
                "amc":          collection,
                "field":        field_key,
                "doc_type":     "manifest",
                "source_url":   url,
                "last_updated": updated,
                "chunk_text":   text,
            },
            "collection": collection,
        }
        chunks.append(chunk)

    return chunks


# PDF processing logic removed as per new architecture (No PDF scope)


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — Embedding (BAAI/bge-small-en-v1.5 via sentence-transformers)
# ─────────────────────────────────────────────────────────────────────────────

def build_embedding_function():
    """
    Loads the BGE-small embedding function via ChromaDB's built-in wrapper.
    The model is downloaded once and cached locally by sentence-transformers.
    normalize_embeddings=True improves cosine similarity retrieval quality.
    """
    try:
        bge_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL,
            normalize_embeddings=True,
        )
        print(f"  ✅ Embedding function loaded: {EMBED_MODEL} (dim={EMBED_DIMS})")
        return bge_ef
    except Exception as exc:
        sys.exit(f"❌  Failed to load embedding model '{EMBED_MODEL}': {exc}\n"
                 f"    Run: pip install sentence-transformers")


# ─────────────────────────────────────────────────────────────────────────────
# Stage 3 — ChromaDB Upsert (one collection per AMC)
# ─────────────────────────────────────────────────────────────────────────────

def upsert_to_chroma(
    chroma_client: chromadb.CloudClient,
    embedding_fn,
    chunks: list[dict[str, Any]],
) -> None:
    """
    Groups chunks by collection name and upserts them to ChromaDB.
    Uses .upsert() so re-running the pipeline overwrites stale embeddings
    rather than creating duplicates (idempotent daily runs).

    ChromaDB handles embedding internally via the embedding_function.
    """
    # Group by collection
    by_collection: dict[str, list[dict[str, Any]]] = {}
    for chunk in chunks:
        col = chunk["collection"]
        by_collection.setdefault(col, []).append(chunk)

    for col_name, col_chunks in by_collection.items():
        # Get or create collection — embedding function is stored in config
        collection = chroma_client.get_or_create_collection(
            name=col_name,
            embedding_function=embedding_fn,
            metadata={"hnsw:space": "cosine"},   # cosine similarity metric
        )
        print(f"\n  📌 Upserting {len(col_chunks)} chunks → collection '{col_name}'")

        # ChromaDB upsert in batches
        for batch_start in range(0, len(col_chunks), BATCH_SIZE):
            batch = col_chunks[batch_start : batch_start + BATCH_SIZE]
            collection.upsert(
                ids=[c["id"] for c in batch],
                documents=[c["text"] for c in batch],
                metadatas=[c["metadata"] for c in batch],
            )
            print(f"    ✅ Upserted batch {batch_start // BATCH_SIZE + 1} "
                  f"({len(batch)} records) into '{col_name}'")


# ─────────────────────────────────────────────────────────────────────────────
# Main Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("📦  Phase 13 — Chunking & Embedding Pipeline (Cloud)")
    print(f"    Embedding Model : {EMBED_MODEL} ({EMBED_DIMS} dims)")
    print(f"    Vector Store    : Chroma Cloud (Tenant: {CHROMA_TENANT}, DB: {CHROMA_DATABASE})")
    print("=" * 60)

    # ── Ensure manifest exists ────────────────────────────────────────────────
    if not os.path.exists(MANIFEST_PATH):
        sys.exit(f"❌  Manifest not found at '{MANIFEST_PATH}'. Run ingest.py first.")

    with open(MANIFEST_PATH, "r", encoding="utf-8-sig") as f:
        manifest: list[dict] = json.load(f)

    print(f"\n📋  Loaded {len(manifest)} scheme records from manifest.json")

    # ── Initialise ChromaDB CloudClient ──────────────────────────────────────
    if not CHROMA_API_KEY or CHROMA_API_KEY == "your-chroma-cloud-api-key":
        sys.exit("❌  CHROMA_API_KEY environment variable is required and must be valid for Cloud synchronization.")

    chroma_client = chromadb.CloudClient(
        tenant=CHROMA_TENANT,
        database=CHROMA_DATABASE,
        api_key=CHROMA_API_KEY
    )
    print(f"  ✅ Chroma CloudClient initialised")

    # ── Initialise BGE embedding function ────────────────────────────────────
    embedding_fn = build_embedding_function()

    # ── Build all chunks ──────────────────────────────────────────────────────
    all_chunks: list[dict[str, Any]] = []

    for record in manifest:
        scheme_name = record.get("scheme_name", "Unknown")
        print(f"\n🔍  Processing: {scheme_name}")

        # Stage 1A — Structured (manifest JSON) chunks
        json_chunks = chunk_manifest_record(record)
        print(f"    ✅ {len(json_chunks)} structured field chunk(s) built")
        all_chunks.extend(json_chunks)

        # PDF chunks removed (Stage 1B)

    print(f"\n🧱  Total chunks to embed & store: {len(all_chunks)}")

    if not all_chunks:
        print("⚠️  No chunks generated — nothing to embed. Exiting.")
        return

    # ── Stage 3: Upsert to ChromaDB (embedding is done internally by Chroma) ──
    print("\n💾  Upserting to ChromaDB (BGE embeddings computed locally) …")
    upsert_to_chroma(chroma_client, embedding_fn, all_chunks)

    # ── Summary ───────────────────────────────────────────────────────────────
    collections = chroma_client.list_collections()
    print("\n" + "=" * 60)
    print("🎉  Phase 13 complete!")
    print(f"    Schemes processed  : {len(manifest)}")
    print(f"    Total chunks       : {len(all_chunks)}")
    print(f"    Embedding model    : {EMBED_MODEL}")
    print(f"    Collections created: {', '.join(c.name for c in collections)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
