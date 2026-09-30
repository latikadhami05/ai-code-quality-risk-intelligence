# src/ingestion/find_files.py
# Finds every Python (.py) file inside a given folder, including subfolders.
# This is the same logic from V1, now as a reusable module instead of a notebook cell.

import os

def find_python_files(folder):
    """
    Walks through 'folder' and every subfolder inside it,
    collecting the full path of every file that ends in .py
    """
    py_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files
