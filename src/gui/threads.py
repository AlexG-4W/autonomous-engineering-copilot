from PySide6.QtCore import QThread, QObject, Signal, Slot
from typing import Callable, Any
import types


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = Signal()
    error = Signal(str)
    result = Signal(object)
    stream = Signal(str)


class Worker(QThread):
    """
    A generic worker thread to offload blocking tasks from the main GUI thread.
    """

    def __init__(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        """
        Executes the function in the thread. Emits signals based on the outcome.
        Supports streaming generation if the function returns a generator.
        """
        try:
            result = self.fn(*self.args, **self.kwargs)

            # Check if the result is a generator (streaming response)
            if isinstance(result, types.GeneratorType):
                final_text = ""
                for chunk in result:
                    if isinstance(chunk, dict) and "choices" in chunk:
                        text = chunk["choices"][0].get("text", "")
                        self.signals.stream.emit(text)
                        final_text += text
                    elif isinstance(chunk, str):
                        self.signals.stream.emit(chunk)
                        final_text += chunk
                self.signals.result.emit(final_text.strip())
            else:
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()
