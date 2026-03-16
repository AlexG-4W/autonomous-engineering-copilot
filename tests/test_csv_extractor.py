import pytest
from pathlib import Path
from src.ingestion.csv_extractor import extract_text_from_csv


def test_extract_text_from_csv_success(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("header1,header2\nval1,val2\n", encoding="utf-8")

    result = extract_text_from_csv(str(csv_file))

    assert "header1 header2" in result
    assert "val1 val2" in result
    assert result == "header1 header2\nval1 val2"


def test_extract_text_from_csv_failure() -> None:
    with pytest.raises(RuntimeError) as exc_info:
        extract_text_from_csv("non_existent.csv")
    assert "Failed to process CSV" in str(exc_info.value)
