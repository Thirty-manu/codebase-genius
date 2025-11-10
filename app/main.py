from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from git import Repo
import os, shutil, tempfile
from app import mapper, analyzer, docgen

app = FastAPI()

class RepoRequest(BaseModel):
    repo_url: str  # can be a GitHub URL OR a local path


@app.on_event("startup")
def startup_message():
    """Print a friendly message when the server starts."""
    import socket
    host = "127.0.0.1"
    port = os.environ.get("PORT", "8000")
    try:
        # Detect port from uvicorn command if passed via --port
        port_env = [arg for arg in os.sys.argv if "--port" in arg]
        if port_env:
            idx = os.sys.argv.index("--port")
            port = os.sys.argv[idx + 1]
    except Exception:
        pass
    print(f"\n🚀 Server running! Open your docs at: http://{host}:{port}/docs\n")


@app.post("/generate")
def generate_docs(data: RepoRequest):
    repo_url = data.repo_url.strip()

    # Detect if it's a local path or remote URL
    is_local = os.path.exists(repo_url)
    tempdir = tempfile.mkdtemp()
    repo_name = os.path.basename(repo_url.rstrip('/')).replace(".git", "")
    repo_path = os.path.join(tempdir, repo_name)

    try:
        if is_local:
            print(f"📂 Analyzing local folder: {repo_url}")
            shutil.copytree(repo_url, repo_path, dirs_exist_ok=True)
        else:
            print(f"🌍 Cloning remote repo: {repo_url}")
            Repo.clone_from(repo_url, repo_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not load repo: {e}")

    # Analyze repo
    ccg = mapper.map_codebase(repo_path)
    summary = analyzer.analyze_codebase(ccg)

    # Output folder
    outdir = os.path.join("outputs", repo_name)
    os.makedirs(outdir, exist_ok=True)
    docgen.generate_docs(repo_name, summary, outdir)

    # Clean up temp files
    shutil.rmtree(tempdir, ignore_errors=True)

    return {
        "status": "done",
        "output": outdir,
        "files": summary["total_files"],
        "functions": summary["total_functions"]
    }
