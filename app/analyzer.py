def analyze_codebase(ccg):
    """
    Returns summary analysis for documentation.
    """
    total_files = len(ccg["files"])
    total_functions = sum(len(v["functions"]) for v in ccg["files"].values())
    return {
        "total_files": total_files,
        "total_functions": total_functions,
        "details": ccg["files"]
    }
