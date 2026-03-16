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

    # ИЗМЕНЕНО: Базовый лимит увеличен с 256 до 1024 токенов
    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        stream: bool = False,
        temperature: float = 0.7,
        top_p: float = 0.95,
    ) -> Union[str, Iterator[Any]]:
        """
        Generates text based on a prompt.
        """
        # ДОБАВЛЕНО: Жесткие стоп-слова. Как только модель генерирует
        # одно из них - она останавливается.
        # <|eot_id|> - это встроенный стоп-сигнал Llama 3.
        response: Union[Dict[str, Any], Iterator[Any]] = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=["Question:", "Context:", "<|eot_id|>", "\n\n\n"],
        )  # type: ignore

        if stream:
            return cast(Iterator[Any], response)

        res_dict = cast(Dict[str, Any], response)
        return str(res_dict["choices"][0]["text"]).strip()

    def generate_rag_response(
        self, query: str, contexts: List[str], **kwargs: Any
    ) -> Union[str, Iterator[Any]]:
        """
        Generates a RAG response by combining context and query into a prompt.
        """
        context_str = "\n".join(contexts)
        # ИЗМЕНЕНО: Строгий системный промпт, запрещающий
        # лить воду и повторять текст
        prompt = (
            f"You are a strict and professional technical assistant. "
            f"Answer the user's question concisely using ONLY "
            f"the information in the Context. "
            f"Do not repeat the raw context.\n\n"
            f"Context:\n{context_str}\n\n"
            f"Question:\n{query}\n\n"
            f"Answer:"
        )
        return self.generate(prompt, **kwargs)
