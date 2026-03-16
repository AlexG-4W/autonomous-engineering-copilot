from unittest.mock import patch, MagicMock


@patch("src.gui.main_window.QMainWindow.__init__", return_value=None)
@patch("src.gui.main_window.QMainWindow.setWindowTitle")
@patch("src.gui.main_window.QMainWindow.resize")
def test_main_window_initialization(
    mock_resize: MagicMock, mock_set_title: MagicMock, mock_super_init: MagicMock
) -> None:
    # We mock out the base class init and Qt methods to bypass actual GUI context
    with (
        patch("src.gui.main_window.MainWindow.setup_ui") as mock_setup,
        patch("src.gui.main_window.MainWindow.connect_signals") as mock_connect,
        patch("src.gui.main_window.MainWindow.apply_dark_theme") as mock_theme,
    ):
        from src.gui.main_window import MainWindow

        MainWindow()

        mock_set_title.assert_called_once_with("Autonomous Engineering Copilot")
        mock_theme.assert_called_once()
        mock_setup.assert_called_once()
        mock_connect.assert_called_once()
