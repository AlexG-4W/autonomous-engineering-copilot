from typing import List, Dict, Any, Union, Iterator, cast
from llama_cpp import Llama  # type: ignore


class Generator:
    """
    Handles local LLM inference using llama-cpp-python.
    """

    def __init__(self, model_path: str) -> None:
        """
        Initializes the LLM with the given model path.

        Args:
            model_path (str): The local path to the GGUF model file.
        """
        # ДОБАВЛЕНО: n_ctx=4096 расширяет память для длинных документов
        self.llm = Llama(model_path=model_path, verbose=False, n_ctx=4096)

    def generate_rag_response(
        self,
        query: str,
        contexts: List[str],
        max_tokens: int = 512,
        stream: bool = False,
        temperature: float = 0.7,
        top_p: float = 0.95,
        **kwargs: Any,
    ) -> Union[str, Iterator[str]]:
        """
        Generates a RAG response by combining context and query into a prompt
        using the Chat Completion API for Llama 3 strict formatting.
        """
        context_str = "\n".join(contexts)

        messages = [
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
                "content": f"Context:\n{context_str}\n\nQuestion:\n{query}",
            },
        ]

        response = self.llm.create_chat_completion(
            messages=messages,  # type: ignore
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            **kwargs,
        )

        if stream:

            def stream_generator() -> Iterator[str]:
                for chunk in cast(Iterator[Any], response):
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content

            return stream_generator()

        res_dict = cast(Dict[str, Any], response)
        return str(res_dict["choices"][0]["message"]["content"]).strip()
