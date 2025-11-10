import os

def map_codebase(repo_path):
    """
    Walks the repo and maps python files and functions.
    """
    code_map = {"files": {}, "edges": []}
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r", errors="ignore") as fh:
                    lines = fh.readlines()
                funcs = [line.strip().split("(")[0].replace("def ", "") for line in lines if line.strip().startswith("def ")]
                code_map["files"][path] = {"functions": funcs}
    return code_map
