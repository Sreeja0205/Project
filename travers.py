import os
import pandas as pd

# 1. Set this to your main project folder where your Bronze/Silver/Gold code & Streamlit app live
project_dir = "."  # Or replace "." with r"C:\Users\Vijay Meher\path\to\your\project"

print("=== 1. PROJECT FILES & FOLDERS ===")
for root, dirs, files in os.walk(project_dir):
    # Skip hidden git/venv/cache folders and raw csv dump
    dirs[:] = [d for d in dirs if d not in {'.git', 'venv', '.venv', '__pycache__', 'node_modules', 'jsonl'}]
    level = root.replace(project_dir, '').count(os.sep)
    indent = '  ' * level
    print(f"{indent}[{os.path.basename(root) or root}]/")
    for f in files:
        if f.endswith(('.py', '.ipynb', '.sql', '.parquet', '.csv', '.db', '.duckdb')):
            print(f"{indent}  - {f}")

print("\n=== 2. PYTHON / SQL CODE FILES ===")
for root, dirs, files in os.walk(project_dir):
    dirs[:] = [d for d in dirs if d not in {'.git', 'venv', '.venv', '__pycache__'}]
    for f in files:
        if f.endswith(('.py', '.sql')):
            filepath = os.path.join(root, f)
            print(f"\n--- FILE: {filepath} ---")
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    print(file.read())
            except Exception as e:
                print(f"Could not read: {e}")
