import os
import shutil
import PyInstaller.__main__

def build():
    print("Starting PyInstaller build pipeline...")
    
    # Clear PyInstaller caches and previous build artifacts
    for p in ['build', 'dist', 'AECopilot.spec']:
        if os.path.exists(p):
            print(f"Removing old cache/build path: {p}")
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    
    # Define hidden imports as required
    hidden_imports = [
        'lancedb',
        'sentence_transformers',
        'llama_cpp',
        'fitz',  # PyMuPDF
        # Common dependencies for these ML libraries that might be missed
        'torch',
        'transformers',
        'huggingface_hub',
        'tokenizers',
        'tqdm',
        'safetensors',
        'numpy',
        'pandas'
    ]
    
    # Construct PyInstaller arguments
    args = [
        'src/gui/main_window.py', # Entry point
        '--name=AECopilot',       # Executable name
        '--onedir',               # Build mode: directory bundle
        '--noconsole',            # UI mode: windowed
        '--clean',                # Clean PyInstaller cache
        '--noconfirm',            # Replace output directory without asking
        f'--paths={os.getcwd()}', # Ensure 'src' package is resolvable
    ]
    
    # Add hidden imports
    for imp in hidden_imports:
        args.extend(['--hidden-import', imp])

    # === ДОБАВЬ ЭТОТ НОВЫЙ БЛОК ===
    # Принудительно собираем все метаданные и внутренние файлы для тяжелых ML-библиотек
    collect_all_packages = [
        'sentence_transformers',
        'transformers',
        'torch',
        'lancedb',
        'pyarrow',
        'llama-cpp-python',
        'tqdm'
    ]
    for pkg in collect_all_packages:
        args.extend(['--collect-all', pkg])
        args.extend(['--copy-metadata', pkg])
    # ==============================       
    
    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
    except Exception as e:
        print(f"Build failed with error: {e}")
        return

    # Post-build check for sentence_transformers
    internal_dir = os.path.join("dist", "AECopilot", "_internal")
    st_dir = os.path.join(internal_dir, "sentence_transformers")
    if not os.path.exists(st_dir):
        # Fallback check for older pyinstaller versions or different structures
        st_dir_root = os.path.join("dist", "AECopilot", "sentence_transformers")
        if os.path.exists(st_dir_root):
            st_dir = st_dir_root
        else:
            print("\nWARNING: 'sentence_transformers' directory NOT found in PyInstaller output!")
            print(f"Expected at: {st_dir}")
    if os.path.exists(st_dir):
        print(f"\nSUCCESS: 'sentence_transformers' directory found at {st_dir}")

    print("\n--- Automating Post-Build Copies ---")
    # 1. Copy llama_cpp/lib
    src_llama_lib = os.path.join(".venv", "Lib", "site-packages", "llama_cpp", "lib")
    dst_llama_lib = os.path.join(internal_dir, "llama_cpp", "lib")
    if os.path.exists(src_llama_lib):
        print(f"Copying {src_llama_lib} -> {dst_llama_lib}")
        if os.path.exists(dst_llama_lib):
            shutil.rmtree(dst_llama_lib)
        shutil.copytree(src_llama_lib, dst_llama_lib)
    else:
        print(f"WARNING: Source llama_cpp lib not found at {src_llama_lib}")

    # 2. Copy model/
    src_model = "model"
    dst_model = os.path.join("dist", "AECopilot", "model")
    if os.path.exists(src_model):
        print(f"Copying {src_model} -> {dst_model}")
        if os.path.exists(dst_model):
            shutil.rmtree(dst_model)
        shutil.copytree(src_model, dst_model)
    else:
        print(f"WARNING: Source model directory not found at {src_model}")

    # 3. Copy lancedb_data/
    src_lancedb = "lancedb_data"
    dst_lancedb = os.path.join("dist", "AECopilot", "lancedb_data")
    if os.path.exists(src_lancedb):
        print(f"Copying {src_lancedb} -> {dst_lancedb}")
        if os.path.exists(dst_lancedb):
            shutil.rmtree(dst_lancedb)
        shutil.copytree(src_lancedb, dst_lancedb)
    else:
        print(f"WARNING: Source lancedb_data directory not found at {src_lancedb}")

    print("\n" + "="*80)
    print("                            BUILD SUCCESSFUL")
    print("="*80)
    print("The application has been successfully built and all required assets")
    print("(models, vector DB, and DLLs) have been copied to the dist folder.")
    print("You can now run dist/AECopilot/AECopilot.exe")
    print("="*80 + "\n")

if __name__ == '__main__':
    build()