# src/features/extract_features.py
# Given one function (as an AST node), calculates its risk-related metrics:
# lines of code, cyclomatic complexity, max nesting depth, branch count,
# variable count, and argument count.
# This is the same logic from V1, now as a reusable, importable module.

import ast

def get_function_features(node):
    """
    Takes one function's AST node and returns a dictionary of
    measured features describing that function's structure.
    """
    # Work out how many lines this function spans
    start = node.lineno
    end = max(child.lineno for child in ast.walk(node) if hasattr(child, "lineno"))
    loc = end - start + 1

    # Start complexity at 1 (one path through the function by default)
    complexity = 1
    max_nesting = 0
    branches = 0
    variables = set()

    # Recursively track how deep if/for/while/try/with blocks are nested
    def walk_nesting(n, depth):
        nonlocal max_nesting
        max_nesting = max(max_nesting, depth)
        for child in ast.iter_child_nodes(n):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                walk_nesting(child, depth + 1)
            else:
                walk_nesting(child, depth)

    walk_nesting(node, 0)

    # Walk every node inside the function once, counting decision points
    # (adds to complexity/branches) and collecting unique variable names
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp, ast.ExceptHandler)):
            complexity += 1
            branches += 1
        if isinstance(child, ast.Name):
            variables.add(child.id)

    # Return everything as a dictionary — one row of our future dataset
    return {
        "function_name": node.name,
        "loc": loc,
        "complexity": complexity,
        "max_nesting": max_nesting,
        "branches": branches,
        "num_variables": len(variables),
        "num_args": len(node.args.args)
    }


def get_functions_from_file(filepath):
    """
    Opens one Python file, parses it, and returns a list of every
    function definition found inside it (as AST nodes).
    Returns an empty list if the file can't be parsed (e.g. syntax error).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception:
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
    return functions
