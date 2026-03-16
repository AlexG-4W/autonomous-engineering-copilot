from unittest.mock import patch, MagicMock
from src.rag.generator import Generator


@patch("src.rag.generator.Llama")
def test_generator_rag_response(mock_llama_class: MagicMock) -> None:
    mock_llm_instance = MagicMock()
    # Mocking the __call__ method of Llama instance
    mock_llm_instance.return_value = {
        "choices": [{"text": " This is the mocked answer. "}]
    }
    mock_llama_class.return_value = mock_llm_instance

    generator = Generator("fake/path/to/model.gguf")

    contexts = ["Context 1", "Context 2"]
    query = "What is this?"
    response = generator.generate_rag_response(query, contexts)

    assert response == "This is the mocked answer."

    # Verify the internal prompt string
    expected_prompt = (
        "You are a strict and professional technical assistant. "
        "Answer the user's question concisely using ONLY "
        "the information in the Context. "
        "Do not repeat the raw context.\n\n"
        "Context:\nContext 1\nContext 2\n\n"
        "Question:\nWhat is this?\n\n"
        "Answer:"
    )
    mock_llm_instance.assert_called_once_with(
        expected_prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        stream=False,
        stop=["Question:", "Context:", "<|eot_id|>", "\n\n\n"],
    )
