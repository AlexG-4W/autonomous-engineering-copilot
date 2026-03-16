from src.rag.chunker import chunk_text


def test_chunk_text() -> None:
    text = "A" * 2000
    metadata = {"source": "doc1.pdf"}

    chunks = chunk_text(text, chunk_size=1000, overlap=200, metadata=metadata)

    assert len(chunks) == 3
    assert len(chunks[0]["text"]) == 1000
    assert chunks[0]["metadata"] == {"source": "doc1.pdf"}
    assert len(chunks[1]["text"]) == 1000
    assert len(chunks[2]["text"]) == 400


def test_chunk_text_empty() -> None:
    chunks = chunk_text("", chunk_size=1000, overlap=200)
    assert chunks == []


def test_chunk_text_no_metadata() -> None:
    text = "Hello world"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert len(chunks) == 3
    assert chunks[0]["text"] == "Hello"
    assert chunks[1]["text"] == "lo wo"
    assert chunks[2]["text"] == "world"
    assert chunks[0]["metadata"] == {}
