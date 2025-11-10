import os
from graphviz import Digraph
import shutil

def generate_docs(repo_name, summary, outdir):
    md_path = os.path.join(outdir, "docs.md")
    with open(md_path, "w") as f:
        f.write(f"# Documentation for {repo_name}\n\n")
        f.write(f"**Total files:** {summary['total_files']}\n\n")
        f.write(f"**Total functions:** {summary['total_functions']}\n\n")
        for file, data in summary["details"].items():
            f.write(f"### {file}\n")
            for func in data["functions"]:
                f.write(f"- {func}\n")
            f.write("\n")
    render_graph(summary, outdir, repo_name)

def render_graph(summary, outdir, repo_name):
    dot = Digraph(comment=repo_name, format="png")
    for file in summary["details"].keys():
        dot.node(file, os.path.basename(file))
    if shutil.which("dot"):
        dot.render(os.path.join(outdir, "structure"), cleanup=True)
    else:
        print("⚠️ Graphviz not installed — skipping PNG rendering.")
