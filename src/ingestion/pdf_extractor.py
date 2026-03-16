import fitz  # type: ignore


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts raw text from a given PDF file using PyMuPDF.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to process PDF {file_path}: {e}")

    return text.strip()
