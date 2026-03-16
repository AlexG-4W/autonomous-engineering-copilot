import csv


def extract_text_from_csv(file_path: str) -> str:
    """
    Extracts raw text from a given CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        str: The extracted text from the CSV.
    """
    text = ""
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                text += " ".join(row) + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to process CSV {file_path}: {e}")

    return text.strip()
