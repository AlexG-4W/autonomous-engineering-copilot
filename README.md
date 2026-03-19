# Autonomous Engineering Copilot 🤖
![scr1 ver1 1](https://github.com/user-attachments/assets/6ebc3f6f-3cc4-46dd-a892-0493207206c6)


## Vision
The Autonomous Engineering Copilot is a cross-platform desktop application designed to act as an offline AI assistant. By utilizing local Large Language Models (LLMs) and embedded vector databases, it provides powerful RAG (Retrieval-Augmented Generation) capabilities entirely on the user's hardware.



## ✨ Key Features & Use Cases
- **Local Document Q&A:** Users can seamlessly query proprietary technical specifications, datasheets, and compliance documents directly on their machine, receiving accurate insights with specific page references.
- **Configurable Inference:** The application provides a GUI settings panel for dynamically adjusting LLM generation parameters (e.g., Temperature, Top-P, Model Selection).
- **Real-Time Streaming:** The AI copilot streams generation text incrementally into the chat window for immediate feedback and responsiveness.
- **Dynamic Context Retrieval:** Users can dynamically adjust the number of context chunks retrieved for RAG generation.
- **Infrastructure Independence:** The system operates without any requirement for API keys, internet connectivity, or specialized cloud infrastructure, ensuring uninterrupted access and complete data privacy.

## 🚀 Quick Start (Standalone Executable for Windows)

You don't need to install Python to use the Copilot. You can run the pre-compiled standalone executable.

1. **Download the Release:** Download the `v1.1.0` release of the `AECopilot` distribution from the Releases tab.
2. **Add a Model:** Ensure you have a quantized GGUF model (e.g., `meta-llama-3-8b-instruct.Q4_K_M.gguf`). Place it in the `model/` directory next to the `.exe`.
3. **Run:** Double-click `AECopilot.exe` to launch the application. No background console will appear, and the app will load the AI models entirely offline.

*(Note: The embedded `lancedb_data` directory is kept alongside the executable to persist your vectorized document knowledge base between sessions).*

---

## 🛠️ Building & Running from Source

If you want to modify the code, run it via Python, or build your own executable, follow these steps.

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Setup Virtual Environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## Troubleshooting

### Failed building wheel for llama-cpp-python (Windows)
This error occurs during dependency installation if your system lacks the necessary C++ compiler to build the `llama-cpp-python` package from source.

**Solution:**
1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) from Microsoft.
2. Run the installer and select the **"Desktop development with C++"** workload.
3. Finish the installation and **restart your terminal or IDE** (e.g., VS Code) to update the system paths.
4. Re-activate your virtual environment and run `pip install -r requirements.txt` again.

### ModuleNotFoundError: No module named 'PySide6'
This usually happens if the `pip install -r requirements.txt` command failed or was interrupted (often by the C++ compiler issue mentioned above). Because the process stopped early, subsequent packages like `PySide6` were not installed.

**Solution:** Resolve any build errors first, then re-run `pip install -r requirements.txt` to ensure all required packages are successfully installed into your `.venv`.
### 4. Download Model
Download a GGUF model (e.g., [Llama-3-8B-Instruct-GGUF](https://huggingface.co/NoelJacob/Meta-Llama-3-8B-Instruct-Q4_K_M-GGUF) , [Qwen2.5-7B-Instruct-Q4_K_M.gguf](https://huggingface.co/WSDW/Qwen2.5-7B-Instruct-Uncensored-Q4_K_M-GGUF) , [Mistral-Nemo-Instruct-2407-Q4_K_M.gguf](https://huggingface.co/Nehal07/Mistral-Nemo-Instruct-2407-Q4_K_M-GGUF) ) and place it in the `model/` directory.
```bash
mkdir model
# Place your .gguf file here
```

### 5. Run the Application
You can run the application by double-clicking the `run_gui.bat` script (on Windows), or by running the module from your terminal:
```bash
python -m src.gui.main_window
```

---

## 📦 Packaging the Application (PyInstaller)

This project includes a custom automated build pipeline that compiles the PySide6 app and handles heavy Machine Learning libraries (like `torch`, `sentence-transformers`, and `lancedb`) correctly.

To build the executable yourself:

```bash
python build.py
```

**What the build script does:**
- Cleans up old cache and build artifacts.
- Uses **PyInstaller** to compile the app in `--onedir` (directory bundle) and `--noconsole` mode.
- Injects necessary metadata and hidden imports for PyTorch and Hugging Face architectures.
- Automatically copies the dynamic DLLs (`llama_cpp/lib`), the `model/` directory, and the `lancedb_data/` directory to the final `dist/AECopilot/` folder.

Once finished, your fully portable application will be waiting in the `dist/AECopilot/` directory!

---

## 🧪 Running Tests
To run the automated test suite, ensure your virtual environment is active and execute:
```bash
pytest tests/
```

## 📂 Architecture & Structure
- `src/gui/`: PySide6 frontend logic, asynchronous QThread workers.
- `src/ingestion/`: Extractors for PDFs (PyMuPDF) and CSVs.
- `src/rag/`: Logic for vector embedding, database interaction (LanceDB), LLM generation, and text chunking.
- `tests/`: Comprehensive test suite using pytest and MagicMock for GUI testing.
- `build.py`: Automated compilation pipeline for PyInstaller.
