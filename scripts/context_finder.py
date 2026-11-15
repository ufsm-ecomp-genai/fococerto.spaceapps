#!/usr/bin/env python3
"""Local Context Finder for AI Coding Agents.

Fast, zero-dependency TF-IDF / BM25 keyword search across project documentation,
papers, manuals, schemas, and task boards.
Usage:
    python scripts/context_finder.py "<search query>"
    python scripts/context_finder.py "Wooster FRP equation" --top 3
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SEARCH_PATHS = [
    ROOT_DIR / "CLAUDE.md",
    ROOT_DIR / "AGENTS.md",
    ROOT_DIR / "CONTEXT.md",
    ROOT_DIR / "docs" / "spaceapps",
    ROOT_DIR / "tasks",
]


def tokenize(text: str) -> list[str]:
    """Tokenize and normalize text into clean words."""
    return re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())


def collect_documents() -> list[tuple[Path, str]]:
    """Gather all markdown documentation files."""
    docs = []
    for p in SEARCH_PATHS:
        if p.is_file() and p.suffix == ".md":
            docs.append((p, p.read_text(encoding="utf-8", errors="ignore")))
        elif p.is_dir():
            for f in p.rglob("*.md"):
                docs.append((f, f.read_text(encoding="utf-8", errors="ignore")))
    return docs


def split_into_chunks(doc_path: Path, text: str, chunk_lines: int = 35) -> list[dict]:
    """Split markdown documents into logical sections/chunks."""
    lines = text.splitlines()
    chunks = []
    current_lines = []
    current_header = doc_path.name

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                chunk_text = "\n".join(current_lines)
                chunks.append({
                    "file": doc_path.relative_to(ROOT_DIR),
                    "header": current_header,
                    "text": chunk_text,
                    "tokens": tokenize(chunk_text),
                })
                current_lines = []
            current_header = line.strip("# ").strip()
        current_lines.append(line)

    if current_lines:
        chunk_text = "\n".join(current_lines)
        chunks.append({
            "file": doc_path.relative_to(ROOT_DIR),
            "header": current_header,
            "text": chunk_text,
            "tokens": tokenize(chunk_text),
        })

    return chunks


def search(query: str, top_k: int = 4) -> list[tuple[float, dict]]:
    """BM25-style ranked keyword retrieval."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    raw_docs = collect_documents()
    all_chunks = []
    for doc_path, text in raw_docs:
        all_chunks.extend(split_into_chunks(doc_path, text))

    if not all_chunks:
        return []

    # Calculate document frequencies
    n_chunks = len(all_chunks)
    df = Counter()
    for chunk in all_chunks:
        unique_tokens = set(chunk["tokens"])
        for t in unique_tokens:
            df[t] += 1

    # Average chunk length
    avg_len = sum(len(c["tokens"]) for c in all_chunks) / n_chunks
    k1 = 1.5
    b = 0.75

    scored_chunks = []
    for chunk in all_chunks:
        score = 0.0
        doc_len = len(chunk["tokens"])
        tf = Counter(chunk["tokens"])

        for q in query_tokens:
            if q in tf:
                # IDF calculation with smoothing
                doc_freq = df.get(q, 0)
                idf = math.log((n_chunks - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
                term_tf = tf[q]
                numerator = term_tf * (k1 + 1)
                denominator = term_tf + k1 * (1 - b + b * (doc_len / avg_len))
                score += idf * (numerator / denominator)

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return scored_chunks[:top_k]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Search query keywords (e.g. 'FRP formula', 'MODIS bow-tie')")
    parser.add_argument("--top", type=int, default=3, help="Number of top results to return")
    args = parser.parse_args()

    results = search(args.query, top_k=args.top)

    if not results:
        print(f"No relevant context found for: '{args.query}'")
        return 0

    print(f"\n🔍 Found {len(results)} relevant context sections for: '{args.query}'\n" + "=" * 80)
    for rank, (score, chunk) in enumerate(results, start=1):
        print(f"\n[Result {rank}] Score: {score:.2f} | File: {chunk['file']} | Section: {chunk['header']}")
        print("-" * 80)
        # Display first 15 lines of snippet
        snippet_lines = chunk["text"].splitlines()[:18]
        print("\n".join(snippet_lines))
        if len(chunk["text"].splitlines()) > 18:
            print("... (truncated)")
        print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
