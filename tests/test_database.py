from pathlib import Path
from src.rag.database import Database


def test_database_integration(tmp_path: Path) -> None:
    db_uri = str(tmp_path / "lancedb")
    db = Database(uri=db_uri)

    table_name = "test_table"
    # Using small dimension for test simplicity
    db.create_table(table_name, dimension=2)

    chunks = [
        {"text": "chunk one", "metadata": {"source": "doc1.pdf", "page": 1}},
        {"text": "chunk two", "metadata": {"source": "doc1.pdf", "page": 2}},
    ]
    embeddings = [[0.1, 0.2], [0.8, 0.9]]

    db.add_chunks(table_name, chunks, embeddings)

    # Search with vector close to [0.1, 0.2]
    results = db.search(table_name, [0.1, 0.2], limit=1)

    assert len(results) == 1
    assert results[0]["text"] == "chunk one"
    assert results[0]["metadata"]["source"] == "doc1.pdf"
    assert results[0]["metadata"]["page"] == 1

    # Open existing table
    table = db.create_table(table_name, dimension=2)
    assert table.name == table_name
