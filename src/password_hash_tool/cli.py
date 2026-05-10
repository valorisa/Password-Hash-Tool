import json
from typing import Annotated

import typer
from rich.console import Console

from password_hash_tool.benchmark import run_benchmark
from password_hash_tool.hashers import HASHERS

app = typer.Typer(
    name="password-hash-tool",
    help="Hash, verify, and benchmark passwords using modern algorithms.",
)
console = Console()


@app.command()
def hash(
    password: Annotated[str, typer.Option("--password", "-p", prompt=True, hide_input=True)],
    algorithm: Annotated[str, typer.Option("--algorithm", "-a")] = "argon2id",
):
    """Hash a password with the specified algorithm."""
    if algorithm not in HASHERS:
        console.print(f"[red]Unknown algorithm: {algorithm}[/red]")
        console.print(f"Available: {', '.join(HASHERS.keys())}")
        raise typer.Exit(1)

    hasher = HASHERS[algorithm]()
    result = hasher.hash(password)
    console.print_json(json.dumps(result))


@app.command()
def verify(
    password: Annotated[str, typer.Option("--password", "-p", prompt=True, hide_input=True)],
    hash_str: Annotated[str, typer.Option("--hash", "-H")],
):
    """Verify a password against an existing hash."""
    detected = None
    if hash_str.startswith("$2b$") or hash_str.startswith("$2a$"):
        detected = "bcrypt"
    elif hash_str.startswith("$argon2"):
        detected = "argon2id"
    elif hash_str.startswith("$scrypt$"):
        detected = "scrypt"

    if detected is None:
        console.print("[red]Could not detect algorithm from hash format.[/red]")
        raise typer.Exit(1)

    hasher = HASHERS[detected]()
    result = hasher.verify(password, hash_str)
    console.print_json(json.dumps(result))


@app.command()
def benchmark(
    iterations: Annotated[int, typer.Option("--iterations", "-n")] = 10,
):
    """Benchmark all supported hashing algorithms."""
    console.print(f"[bold]Running benchmark ({iterations} iterations per algorithm)...[/bold]")
    results = run_benchmark(iterations=iterations)
    console.print_json(json.dumps({"results": results}))


@app.command()
def serve(
    host: Annotated[str, typer.Option("--host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port")] = 8000,
):
    """Start the FastAPI server."""
    import uvicorn

    console.print(f"[bold green]Starting server at http://{host}:{port}[/bold green]")
    console.print("Documentation: http://{host}:{port}/docs")
    uvicorn.run("password_hash_tool.api:app", host=host, port=port)


if __name__ == "__main__":
    app()
