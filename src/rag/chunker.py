from typing import List, Dict, Any, Optional


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
    metadata: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of `chunk_size` characters with `overlap` characters.
    Attaches metadata to each chunk.
    """
    if metadata is None:
        metadata = {}

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk_str = text[start:end]
        chunks.append({"text": chunk_str, "metadata": metadata.copy()})
        if end >= text_length:
            break
        start += chunk_size - overlap

    return chunks
