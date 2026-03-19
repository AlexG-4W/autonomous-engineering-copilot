import pytest
from unittest.mock import patch, MagicMock
from src.rag.pipeline import RAGPipeline


@patch("src.rag.pipeline.extract_text_from_pdf")
@patch("src.rag.pipeline.Embedder")
@patch("src.rag.pipeline.Database")
@patch("src.rag.pipeline.Generator")
def test_pipeline_ingest_and_query(
    mock_gen_class: MagicMock,
    mock_db_class: MagicMock,
    mock_embedder_class: MagicMock,
    mock_extract_pdf: MagicMock,
) -> None:
    # Setup mocks
    mock_extract_pdf.return_value = "This is a dummy document."

    mock_embedder_instance = MagicMock()
    mock_embedder_instance.generate_embeddings.return_value = [[0.1, 0.2]]
    mock_embedder_class.return_value = mock_embedder_instance

    mock_db_instance = MagicMock()
    mock_db_instance.search.return_value = [{"text": "dummy context", "metadata": {}}]
    mock_db_class.return_value = mock_db_instance

    mock_gen_instance = MagicMock()
    mock_gen_instance.generate_rag_response.return_value = "Mocked answer."
    mock_gen_class.return_value = mock_gen_instance

    # Initialize Pipeline
    pipeline = RAGPipeline(db_uri="fake_db", model_path="fake_model")

    # Test Ingestion
    pipeline.ingest_document("dummy.pdf")

    mock_extract_pdf.assert_called_once_with("dummy.pdf")
    assert mock_embedder_instance.generate_embeddings.call_count == 1
    mock_db_instance.add_chunks.assert_called_once()

    # Test Query
    answer = pipeline.query("What is this?", top_k=5, temperature=0.1)

    assert answer == "Mocked answer."
    mock_db_instance.search.assert_called_once_with(
        "knowledge_base", [0.1, 0.2], limit=5
    )
    mock_gen_instance.generate_rag_response.assert_called_once_with(
        "What is this?", ["dummy context"], temperature=0.1
    )


@patch("src.rag.pipeline.extract_text_from_csv")
@patch("src.rag.pipeline.Embedder")
@patch("src.rag.pipeline.Database")
@patch("src.rag.pipeline.Generator")
def test_pipeline_unsupported_file(
    mock_gen_class: MagicMock,
    mock_db_class: MagicMock,
    mock_embedder_class: MagicMock,
    mock_extract_csv: MagicMock,
) -> None:
    pipeline = RAGPipeline(db_uri="fake_db", model_path="fake_model")

    with pytest.raises(ValueError, match="Unsupported file format"):
        pipeline.ingest_document("unsupported.txt")
