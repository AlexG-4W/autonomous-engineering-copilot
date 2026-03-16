import pytest
from unittest.mock import patch, MagicMock
from src.ingestion.pdf_extractor import extract_text_from_pdf


def test_extract_text_from_pdf_success() -> None:
    # Setup mock
    mock_doc = MagicMock()
    mock_page1 = MagicMock()
    mock_page1.get_text.return_value = "Page 1 Text"
    mock_page2 = MagicMock()
    mock_page2.get_text.return_value = "Page 2 Text"

    # doc acts like a list of pages
    mock_doc.__iter__.return_value = [mock_page1, mock_page2]

    # mock the context manager
    mock_doc.__enter__.return_value = mock_doc

    with patch("src.ingestion.pdf_extractor.fitz.open", return_value=mock_doc):
        result = extract_text_from_pdf("dummy.pdf")

        assert "Page 1 Text" in result
        assert "Page 2 Text" in result
        assert result == "Page 1 Text\nPage 2 Text"


def test_extract_text_from_pdf_failure() -> None:
    with patch(
        "src.ingestion.pdf_extractor.fitz.open", side_effect=Exception("File not found")
    ):
        with pytest.raises(RuntimeError) as exc_info:
            extract_text_from_pdf("missing.pdf")

        assert "Failed to process PDF missing.pdf: File not found" in str(
            exc_info.value
        )
