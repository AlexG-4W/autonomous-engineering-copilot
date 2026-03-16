import sys
import os
from dataclasses import dataclass

# Add project root to sys.path to allow direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from typing import Optional, Any  # noqa: E402
from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
    QDoubleSpinBox,
    QSpinBox,
    QFormLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt  # noqa: E402
from src.gui.threads import Worker  # noqa: E402

# We'll import RAGPipeline lazily or mock it for tests,
# but define it here for real usage.
# from src.rag.pipeline import RAGPipeline


@dataclass
class AppSettings:
    model_path: str = "./model/meta-llama-3-8b-instruct.Q4_K_M.gguf"
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 512


class MainWindow(QMainWindow):
    def __init__(self, pipeline: Optional[Any] = None) -> None:
        super().__init__()
        self.pipeline = pipeline
        self.settings = AppSettings()
        self.setWindowTitle("Autonomous Engineering Copilot")
        self.resize(1024, 768)

        self.apply_dark_theme()
        self.setup_ui()
        self.connect_signals()

    def apply_dark_theme(self) -> None:
        dark_stylesheet = """
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QPushButton {
                background-color: #0e639c;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #094771;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                padding: 8px;
                border-radius: 4px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def setup_ui(self) -> None:
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(sidebar)

        self.upload_btn = QPushButton("Upload Document")

        # Settings UI
        settings_group = QGroupBox("Settings")
        settings_layout = QFormLayout(settings_group)

        self.model_path_input = QLineEdit(self.settings.model_path)
        self.browse_model_btn = QPushButton("Browse...")

        model_path_layout = QHBoxLayout()
        model_path_layout.addWidget(self.model_path_input)
        model_path_layout.addWidget(self.browse_model_btn)

        self.temp_input = QDoubleSpinBox()
        self.temp_input.setRange(0.0, 2.0)
        self.temp_input.setSingleStep(0.1)
        self.temp_input.setValue(self.settings.temperature)

        self.top_p_input = QDoubleSpinBox()
        self.top_p_input.setRange(0.0, 1.0)
        self.top_p_input.setSingleStep(0.05)
        self.top_p_input.setValue(self.settings.top_p)

        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(1, 4096)
        self.max_tokens_input.setValue(self.settings.max_tokens)

        self.apply_settings_btn = QPushButton("Apply Settings")

        settings_layout.addRow("Model Path:", model_path_layout)
        settings_layout.addRow("Temperature:", self.temp_input)
        settings_layout.addRow("Top-P:", self.top_p_input)
        settings_layout.addRow("Max Tokens:", self.max_tokens_input)
        settings_layout.addWidget(self.apply_settings_btn)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(self.upload_btn)
        sidebar_layout.addWidget(settings_group)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.status_label)

        # Chat Area
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask a question about your documents...")
        self.send_btn = QPushButton("Send")

        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_btn)

        chat_layout.addWidget(self.chat_history)
        chat_layout.addWidget(input_container)

        # Assemble Main Layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(chat_container)

        self.setCentralWidget(main_widget)

    def connect_signals(self) -> None:
        self.upload_btn.clicked.connect(self.handle_upload)
        self.send_btn.clicked.connect(self.handle_send)
        self.chat_input.returnPressed.connect(self.handle_send)
        self.apply_settings_btn.clicked.connect(self.handle_apply_settings)
        self.browse_model_btn.clicked.connect(self.handle_browse_model)

    def handle_apply_settings(self) -> None:
        new_model_path = self.model_path_input.text()

        # Check if the model path has changed
        if new_model_path != self.settings.model_path:
            self.settings.model_path = new_model_path
            self.settings.temperature = self.temp_input.value()
            self.settings.top_p = self.top_p_input.value()
            self.settings.max_tokens = self.max_tokens_input.value()

            self.status_label.setText("Loading model...")
            self.apply_settings_btn.setEnabled(False)
            self.send_btn.setEnabled(False)
            self.upload_btn.setEnabled(False)

            # Re-initialize the pipeline in a background thread
            from src.rag.pipeline import RAGPipeline

            self.model_worker = Worker(
                RAGPipeline, db_uri="./lancedb_data", model_path=new_model_path
            )
            self.model_worker.signals.result.connect(self.on_model_load_success)
            self.model_worker.signals.error.connect(self.on_model_load_error)
            self.model_worker.signals.finished.connect(self.on_model_load_finished)
            self.model_worker.start()
        else:
            # If path hasn't changed, just update other settings instantly
            self.settings.temperature = self.temp_input.value()
            self.settings.top_p = self.top_p_input.value()
            self.settings.max_tokens = self.max_tokens_input.value()
            self.status_label.setText("Settings Applied")

    def on_model_load_success(self, pipeline: Any) -> None:
        self.pipeline = pipeline
        self.status_label.setText("Model loaded successfully")

    def on_model_load_error(self, error_msg: str) -> None:
        self.status_label.setText("Error loading model")
        QMessageBox.critical(
            self, "Model Error", f"Failed to load the new model:\n{error_msg}"
        )
        self.pipeline = None

    def on_model_load_finished(self) -> None:
        self.apply_settings_btn.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.upload_btn.setEnabled(True)

    def handle_browse_model(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Model", "", "GGUF Models (*.gguf)"
        )
        if file_path:
            self.model_path_input.setText(file_path)

    def handle_upload(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Document", "", "Documents (*.pdf *.csv)"
        )
        if not file_path:
            return

        if not self.pipeline:
            QMessageBox.warning(self, "Error", "RAG Pipeline is not initialized.")
            return

        self.status_label.setText("Ingesting...")
        self.upload_btn.setEnabled(False)

        # Start ingestion in a background thread
        self.worker = Worker(self.pipeline.ingest_document, file_path)
        self.worker.signals.result.connect(self.on_ingest_success)
        self.worker.signals.error.connect(self.on_ingest_error)
        self.worker.signals.finished.connect(self.on_ingest_finished)
        self.worker.start()

    def on_ingest_success(self, result: Any) -> None:
        self.status_label.setText("Ingestion Complete")

    def on_ingest_error(self, error_msg: str) -> None:
        self.status_label.setText("Error")
        QMessageBox.critical(
            self, "Ingestion Error", f"Failed to ingest document:\n{error_msg}"
        )

    def on_ingest_finished(self) -> None:
        self.upload_btn.setEnabled(True)

    def handle_send(self) -> None:
        query = self.chat_input.text().strip()
        if not query:
            return

        self.append_chat(f"<b>You:</b> {query}")
        self.append_chat("<b>Copilot:</b> ")
        self.chat_input.clear()

        if not self.pipeline:
            self.append_chat("<b>System:</b> Error: RAG Pipeline is not initialized.")
            return

        self.send_btn.setEnabled(False)
        self.chat_input.setEnabled(False)

        # Uses the inference parameters from self.settings
        self.chat_worker = Worker(
            self.pipeline.query,
            query,
            stream=True,
            temperature=self.settings.temperature,
            top_p=self.settings.top_p,
            max_tokens=self.settings.max_tokens,
        )
        self.chat_worker.signals.stream.connect(self.on_query_stream)
        self.chat_worker.signals.result.connect(self.on_query_success)
        self.chat_worker.signals.error.connect(self.on_query_error)
        self.chat_worker.signals.finished.connect(self.on_query_finished)
        self.chat_worker.start()

    def append_chat(self, message: str) -> None:
        self.chat_history.append(message)
        # Scroll to bottom
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_query_stream(self, chunk: str) -> None:
        cursor = self.chat_history.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.chat_history.setTextCursor(cursor)
        self.chat_history.insertPlainText(chunk)
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_query_success(self, result: Any) -> None:
        self.append_chat("\n")

    def on_query_error(self, error_msg: str) -> None:
        self.append_chat(f"<b>System:</b> Error during generation: {error_msg}")

    def on_query_finished(self) -> None:
        self.send_btn.setEnabled(True)
        self.chat_input.setEnabled(True)
        self.chat_input.setFocus()


if __name__ == "__main__":
    from src.rag.pipeline import RAGPipeline

    app = QApplication(sys.argv)

    # 1. Загружаем нашу модель до открытия окна
    print("Инициализация ИИ-модели. Пожалуйста, подождите...")
    model_path = os.path.join(".", "model", "meta-llama-3-8b-instruct.Q4_K_M.gguf")

    try:
        my_pipeline = RAGPipeline(db_uri="./lancedb_data", model_path=model_path)
        print("Модель успешно загружена!")
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        my_pipeline = None  # type: ignore

    # 2. Передаем готовую модель внутрь интерфейса
    window = MainWindow(pipeline=my_pipeline)
    window.show()
    sys.exit(app.exec())
