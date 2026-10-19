import os, glob, pandas as pd

# 1. Print only your Python/Notebook file names
for f in glob.glob("**/*", recursive=True):
    if f.endswith(('.py', '.ipynb', '.sql')) and 'venv' not in f:
        print("CODE:", f)

# 2. Print only Gold/Silver table names and their columns
for f in glob.glob("**/*", recursive=True):
    if any(k in f.lower() for k in ['gold', 'silver', 'kpi', 'segment', 'customer']) and f.endswith(('.csv', '.parquet')):
        df = pd.read_csv(f, nrows=1) if f.endswith('.csv') else pd.read_parquet(f)
        print(f"\nTABLE: {f} -> COLS: {list(df.columns)}")
