# Autonomous Engineering Copilot 🤖

![scr v2a](https://github.com/user-attachments/assets/fadbd47b-fe95-4659-b6c8-f7da21678126)



## Vision
The Autonomous Engineering Copilot is a cross-platform desktop application designed to act as an offline AI assistant. By utilizing local Large Language Models (LLMs) and embedded vector databases, it provides powerful RAG (Retrieval-Augmented Generation) capabilities entirely on the user's hardware.




## ✨ Key Features & Use Cases
- **Local Document Q&A:** Users can seamlessly query proprietary technical specifications, datasheets, and compliance documents directly on their machine, receiving accurate insights with specific page references.
- **Multiple File Formats:** Support for `.pdf`, `.csv`, `.docx`, `.xlsx`, `.txt`, and `.md` file ingestion.
- **Multi-Table Vector Search:** Dynamically isolates each uploaded document into its own LanceDB table, allowing users to query "All" documents via Reciprocal Rank Fusion, or filter the search to a specific document collection via the UI sidebar.
- **Source Citations:** Automatically appends document sources and metadata to the end of the AI's response so users can verify facts.
- **Modern UI & Configurable Inference:** A sleek dark theme (Fusion) with a GUI settings panel for dynamically adjusting LLM generation parameters (e.g., Temperature, Top-P, Model Selection, Context Chunks).
- **Real-Time Streaming:** The AI copilot streams generation text incrementally into the chat window for immediate feedback and responsiveness.
- **Infrastructure Independence:** The system operates without any requirement for API keys, internet connectivity, or specialized cloud infrastructure, ensuring uninterrupted access and complete data privacy.

# 🚀 Release v2.1-alpha: Gemma 4 Support

## 🔥 Highlight: Full Gemma 4 Compatibility
The core inference engine has been upgraded to support the newly released **Gemma 4** architecture. The application now seamlessly handles the advanced tokenization and multi-layered embeddings of the latest GGUF models.
* **Recommended Model:** This release is optimized and tested with the `Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf` model for precise, unfiltered technical generation.
* **Download the Model:** [Download Gemma-4-E4B here](https://huggingface.co/HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive#aggressive-variant)


## 🛠️ Quick Start Instructions
1. Download the `AECopilot2.1-alpha.zip` archive from the assets below and extract it to a folder on your PC.
2. Download your preferred `.gguf` model (like the recommended Gemma 4 model above).
3. Place the downloaded `.gguf` file inside the `AECopilot/model/` directory.
4. Run `AECopilot.exe` and start querying your local documents entirely offline!

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

* **Note:**  also tested and verified 4-bit support for the advanced reasoning model: [Qwen3.6-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled-GGUF](https://huggingface.co/hesamation/Qwen3.6-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled-GGUF).
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
