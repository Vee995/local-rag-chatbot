import pytest
from types import SimpleNamespace

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Test the split_documents function from ingestion.text_splitter
def test_split_documents(monkeypatch):
    from ingestion.text_splitter import split_documents

    # Mock docs input
    docs = ["doc1", "doc2"]
    # Mock config
    config = {"splitter": {"chunk_size": 10, "chunk_overlap": 2}}

    # Patch RecursiveCharacterTextSplitter to track input and simulate splitting
    class MockSplitter:
        def __init__(self, chunk_size, chunk_overlap):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_documents(self, docs_arg):
            assert docs_arg == docs
            return ["chunk1", "chunk2"]

    monkeypatch.setattr(
        "ingestion.text_splitter.RecursiveCharacterTextSplitter", MockSplitter
    )

    chunks = split_documents(docs, config)
    assert chunks == ["chunk1", "chunk2"]
