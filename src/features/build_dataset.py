# src/features/build_dataset.py
# Combines file-finding and feature-extraction into one pipeline:
# given a list of files, returns a list of feature dictionaries,
# one per function found across all those files.

from src.features.extract_features import get_functions_from_file, get_function_features

def build_dataset(file_list, repo_name):
    """
    Takes a list of file paths and a label for where they came from
    (e.g. 'requests', 'flask'), and returns a list of rows — one per
    function found, each with its measured features plus identifiers.
    """
    rows = []
    for filepath in file_list:
        functions = get_functions_from_file(filepath)
        for fn in functions:
            try:
                features = get_function_features(fn)
                # Add identifiers separately from the ML features themselves,
                # so file/repo names never leak into what the model learns from
                features["file"] = filepath
                features["repo"] = repo_name
                rows.append(features)
            except Exception:
                # If one function fails to measure, skip it — don't crash
                # the whole repository scan over a single bad case
                continue
    return rows
