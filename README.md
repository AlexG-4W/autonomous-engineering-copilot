# Autonomous Engineering Copilot

## Vision
The Autonomous Engineering Copilot is a cross-platform Python desktop application designed to act as an offline AI assistant. By utilizing local Large Language Models (LLMs) and embedded vector databases, it provides powerful RAG (Retrieval-Augmented Generation) capabilities entirely on the user's hardware.

![s1](https://github.com/AlexG-4W/autonomous-engineering-copilot/blob/main/s1.jpg)
![s1](https://github.com/AlexG-4W/autonomous-engineering-copilot/blob/main/s2.jpg)


## Key Features & Use Cases
- **Local Document Q&A:** Users can seamlessly query proprietary technical specifications, datasheets, and compliance documents directly on their machine, receiving accurate insights with specific page references.
- **Configurable Inference:** The application provides a GUI settings panel for dynamically adjusting LLM generation parameters (e.g., Temperature, Top-P, Model Selection).
- **Real-Time Streaming:** The AI copilot streams generation text incrementally into the chat window for immediate feedback and responsiveness.
- **Infrastructure Independence:** The system operates without any requirement for API keys, internet connectivity, or specialized cloud infrastructure, ensuring uninterrupted access and complete data privacy.

## Technology Stack
- **Programming Language:** Python 3.11+
- **Frontend Framework:** PySide6 (Qt for Python). Selected for its enterprise-grade cross-platform capabilities and robust multithreading support (QThread). It ensures the UI remains fully responsive and non-blocking during intensive local LLM inference.
- **Backend Core & AI Pipeline:** 
  - **Local LLM Engine:** llama-cpp-python for local CPU inference using quantized GGUF models.
  - **Embedding Model:** sentence-transformers (`all-MiniLM-L6-v2`) for rapid CPU-bound vector generation.
  - **Data Ingestion (Parsing):** PyMuPDF for PDF parsing, and standard CSV modules for structured data extraction.
- **Database:** LanceDB. An embedded-first (in-process) vector database running directly within the Python process using memory-mapped files.

## Getting Started

### 1. Prerequisites
- Python 3.11 or higher
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

### 4. Download Model
Download a GGUF model (e.g., [Llama-3-8B-Instruct-GGUF](https://huggingface.co/NoelJacob/Meta-Llama-3-8B-Instruct-Q4_K_M-GGUF) and place it in the `model/` directory.


```bash
mkdir model
# Download your chosen .gguf file into the model/ directory
```

### 5. Run the Application
You can run the application by double-clicking the `run_gui.bat` script (on Windows), or by running the module from your terminal:

```bash
python -m src.gui.main_window
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

## Running Tests
To run the automated test suite, ensure your virtual environment is active and execute:
```bash
pytest tests/
```

## Structure
- `src/gui/`: PySide6 frontend logic, asynchronous QThread workers.
- `src/ingestion/`: Extractors for PDFs, CSVs.
- `src/rag/`: Logic for vector embedding, database interaction (LanceDB), LLM generation, and text chunking.
- `tests/`: Comprehensive test suite using pytest and MagicMock for GUI testing.

- ## License
This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE
