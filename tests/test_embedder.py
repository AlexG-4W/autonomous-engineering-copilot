import numpy as np
from unittest.mock import patch, MagicMock
from src.rag.embedder import Embedder


@patch("src.rag.embedder.SentenceTransformer")
def test_embedder_initialization(mock_st_class: MagicMock) -> None:
    Embedder("fake-model-name")
    mock_st_class.assert_called_once_with("fake-model-name")


@patch("src.rag.embedder.SentenceTransformer")
def test_generate_embeddings_success(mock_st_class: MagicMock) -> None:
    mock_model = MagicMock()
    mock_st_class.return_value = mock_model

    # Use a real numpy array to simulate the encode output
    mock_array = np.array([[0.1, 0.2], [0.3, 0.4]])
    mock_model.encode.return_value = mock_array

    embedder = Embedder("fake-model")
    texts = ["chunk one", "chunk two"]
    embeddings = embedder.generate_embeddings(texts)

    mock_model.encode.assert_called_once_with(texts, convert_to_numpy=True)
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]


@patch("src.rag.embedder.SentenceTransformer")
def test_generate_embeddings_empty(mock_st_class: MagicMock) -> None:
    mock_model = MagicMock()
    mock_st_class.return_value = mock_model

    embedder = Embedder("fake-model")
    embeddings = embedder.generate_embeddings([])

    # encode should not be called for an empty list
    mock_model.encode.assert_not_called()
    assert embeddings == []
