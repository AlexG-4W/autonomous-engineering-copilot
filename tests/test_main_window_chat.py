from unittest.mock import patch, MagicMock


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
def test_main_window_chat_interaction(
    mock_resize: MagicMock, mock_set_title: MagicMock, mock_super_init: MagicMock
) -> None:
    # Use patch context manager for the MainWindow methods to isolate test logic
    with (
        patch("src.gui.main_window.MainWindow.setup_ui"),
        patch("src.gui.main_window.MainWindow.connect_signals"),
        patch("src.gui.main_window.MainWindow.apply_dark_theme"),
        patch("src.gui.main_window.MainWindow.append_chat") as mock_append,
        patch("src.gui.main_window.Worker") as mock_worker_class,
    ):
        from src.gui.main_window import MainWindow

        mock_pipeline = MagicMock()
        window = MainWindow(pipeline=mock_pipeline)

        # Manually construct attributes needed for test since setup_ui is mocked
        window.chat_input = MagicMock()
        window.chat_input.text.return_value = "Test query"
        window.send_btn = MagicMock()

        # Mock the worker instance behavior
        mock_worker_instance = MagicMock()
        mock_worker_class.return_value = mock_worker_instance

        # Trigger handle_send
        window.handle_send()

        # Assert UI updates
        mock_append.assert_any_call("<b>You:</b> Test query")
        mock_append.assert_any_call("<b>Copilot:</b> ")
        window.chat_input.clear.assert_called_once()
        window.send_btn.setEnabled.assert_called_once_with(False)

        # Assert worker thread is created and started with the pipeline
        mock_worker_class.assert_called_once_with(
            mock_pipeline.query,
            "Test query",
            top_k=3,
            stream=True,
            temperature=0.1,
            top_p=0.90,
            max_tokens=512,
        )
        mock_worker_instance.start.assert_called_once()


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
def test_main_window_on_query_stream(
    mock_connect, mock_setup, mock_theme, mock_resize, mock_title, mock_init
) -> None:
    from src.gui.main_window import MainWindow

    window = MainWindow()
    window.chat_history = MagicMock()

    mock_cursor = MagicMock()
    window.chat_history.textCursor.return_value = mock_cursor

    mock_scrollbar = MagicMock()
    window.chat_history.verticalScrollBar.return_value = mock_scrollbar

    window.on_query_stream("Hello")

    window.chat_history.setTextCursor.assert_called_once_with(mock_cursor)
    window.chat_history.insertPlainText.assert_called_once_with("Hello")
    mock_scrollbar.setValue.assert_called_once()
