import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_pipeline():
    return MagicMock()


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
def test_settings_initialization(
    mock_connect,
    mock_setup,
    mock_theme,
    mock_resize,
    mock_title,
    mock_init,
    mock_pipeline,
):
    from src.gui.main_window import MainWindow

    window = MainWindow(pipeline=mock_pipeline)

    assert window.settings.model_path == "./model/meta-llama-3-8b-instruct.Q4_K_M.gguf"
    assert window.settings.temperature == 0.7
    assert window.settings.top_p == 0.95
    assert window.settings.max_tokens == 512


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
@patch(
    "src.gui.main_window.QFileDialog.getOpenFileName",
    return_value=("/some/path/model.gguf", ""),
)
def test_handle_browse_model(
    mock_file_dialog,
    mock_connect,
    mock_setup,
    mock_theme,
    mock_resize,
    mock_title,
    mock_init,
    mock_pipeline,
):
    from src.gui.main_window import MainWindow

    window = MainWindow(pipeline=mock_pipeline)

    window.model_path_input = MagicMock()

    window.handle_browse_model()

    mock_file_dialog.assert_called_once_with(
        window, "Select Model", "", "GGUF Models (*.gguf)"
    )
    window.model_path_input.setText.assert_called_once_with("/some/path/model.gguf")


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
@patch("src.gui.main_window.Worker")
def test_handle_apply_settings_new_model(
    mock_worker,
    mock_connect,
    mock_setup,
    mock_theme,
    mock_resize,
    mock_title,
    mock_init,
    mock_pipeline,
):
    from src.gui.main_window import MainWindow

    window = MainWindow(pipeline=mock_pipeline)

    window.model_path_input = MagicMock()
    window.model_path_input.text.return_value = "/a/new/path.gguf"

    window.temp_input = MagicMock()
    window.temp_input.value.return_value = 0.8
    window.top_p_input = MagicMock()
    window.top_p_input.value.return_value = 0.9
    window.max_tokens_input = MagicMock()
    window.max_tokens_input.value.return_value = 1024

    window.status_label = MagicMock()
    window.apply_settings_btn = MagicMock()
    window.send_btn = MagicMock()
    window.upload_btn = MagicMock()

    mock_worker_instance = MagicMock()
    mock_worker.return_value = mock_worker_instance

    window.handle_apply_settings()

    assert window.settings.model_path == "/a/new/path.gguf"
    window.status_label.setText.assert_called_once_with("Loading model...")
    window.apply_settings_btn.setEnabled.assert_called_once_with(False)

    mock_worker.assert_called_once()
    mock_worker_instance.start.assert_called_once()


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
def test_on_model_load_slots(
    mock_connect,
    mock_setup,
    mock_theme,
    mock_resize,
    mock_title,
    mock_init,
):
    from src.gui.main_window import MainWindow

    window = MainWindow()
    window.status_label = MagicMock()
    window.apply_settings_btn = MagicMock()
    window.send_btn = MagicMock()
    window.upload_btn = MagicMock()

    new_pipeline = MagicMock()
    window.on_model_load_success(new_pipeline)
    assert window.pipeline == new_pipeline
    window.status_label.setText.assert_called_with("Model loaded successfully")

    with patch("src.gui.main_window.QMessageBox.critical") as mock_box:
        window.on_model_load_error("Failed to load")
        assert window.pipeline is None
        window.status_label.setText.assert_called_with("Error loading model")
        mock_box.assert_called_once()

    window.on_model_load_finished()
    window.apply_settings_btn.setEnabled.assert_called_with(True)
    window.send_btn.setEnabled.assert_called_with(True)
    window.upload_btn.setEnabled.assert_called_with(True)


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
@patch("src.gui.main_window.MainWindow.apply_dark_theme")
@patch("src.gui.main_window.MainWindow.setup_ui")
@patch("src.gui.main_window.MainWindow.connect_signals")
def test_handle_apply_settings_same_model(
    mock_connect,
    mock_setup,
    mock_theme,
    mock_resize,
    mock_title,
    mock_init,
    mock_pipeline,
):
    from src.gui.main_window import MainWindow

    window = MainWindow(pipeline=mock_pipeline)

    window.model_path_input = MagicMock()
    # Return the exact same path to trigger the 'else' block
    window.model_path_input.text.return_value = (
        "./model/meta-llama-3-8b-instruct.Q4_K_M.gguf"
    )

    window.temp_input = MagicMock()
    window.temp_input.value.return_value = 0.8
    window.top_p_input = MagicMock()
    window.top_p_input.value.return_value = 0.9
    window.max_tokens_input = MagicMock()
    window.max_tokens_input.value.return_value = 1024
    window.status_label = MagicMock()

    window.handle_apply_settings()

    assert window.settings.temperature == 0.8
    assert window.settings.top_p == 0.9
    assert window.settings.max_tokens == 1024
    window.status_label.setText.assert_called_once_with("Settings Applied")
