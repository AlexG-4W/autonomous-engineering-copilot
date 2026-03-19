from unittest.mock import patch, MagicMock
from src.rag.generator import Generator


@patch("src.rag.generator.Llama")
def test_generator_rag_response(mock_llama_class: MagicMock) -> None:
    mock_llm_instance = MagicMock()
    # Mocking the create_chat_completion method of Llama instance
    mock_llm_instance.create_chat_completion.return_value = {
        "choices": [{"message": {"content": " This is the mocked answer. "}}]
    }
    mock_llama_class.return_value = mock_llm_instance

    generator = Generator("fake/path/to/model.gguf")

    contexts = ["Context 1", "Context 2"]
    query = "What is this?"
    response = generator.generate_rag_response(query, contexts)

    assert response == "This is the mocked answer."

    # Verify the internal messages array
    expected_messages = [
        {
            "role": "system",
            "content": (
                "You are a strict and professional technical assistant. "
                "Answer the user's question concisely using ONLY the "
                "information in the Context. Do not repeat the raw context. "
                "If the answer is not in the context, say so."
            ),
        },
        {
            "role": "user",
            "content": "Context:\nContext 1\nContext 2\n\nQuestion:\nWhat is this?",
        },
    ]

    mock_llm_instance.create_chat_completion.assert_called_once_with(
        messages=expected_messages,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        stream=False,
    )
