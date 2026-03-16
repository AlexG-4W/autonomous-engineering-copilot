from typing import List, Any
from src.gui.threads import Worker


def dummy_function(x: int, y: int) -> int:
    return x + y


def dummy_function_error() -> None:
    raise ValueError("Test error")


def dummy_function_stream() -> Any:
    yield "Hello"
    yield " "
    yield "World"


def test_worker_success() -> None:
    worker = Worker(dummy_function, 2, 3)

    results: List[Any] = []
    finished_called = []
    errors: List[str] = []

    worker.signals.result.connect(lambda r: results.append(r))
    worker.signals.finished.connect(lambda: finished_called.append(True))
    worker.signals.error.connect(lambda e: errors.append(e))

    worker.run()

    assert results == [5]
    assert len(finished_called) == 1
    assert len(errors) == 0


def test_worker_error() -> None:
    worker = Worker(dummy_function_error)

    results: List[Any] = []
    finished_called = []
    errors: List[str] = []

    worker.signals.result.connect(lambda r: results.append(r))
    worker.signals.finished.connect(lambda: finished_called.append(True))
    worker.signals.error.connect(lambda e: errors.append(e))

    worker.run()

    assert len(results) == 0
    assert errors == ["Test error"]
    assert len(finished_called) == 1


def test_worker_stream() -> None:
    worker = Worker(dummy_function_stream)

    results: List[Any] = []
    streams: List[str] = []
    finished_called = []
    errors: List[str] = []

    worker.signals.result.connect(lambda r: results.append(r))
    worker.signals.stream.connect(lambda s: streams.append(s))
    worker.signals.finished.connect(lambda: finished_called.append(True))
    worker.signals.error.connect(lambda e: errors.append(e))

    worker.run()

    assert streams == ["Hello", " ", "World"]
    assert results == ["Hello World"]
    assert len(finished_called) == 1
    assert len(errors) == 0
