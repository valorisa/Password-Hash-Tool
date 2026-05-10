from typer.testing import CliRunner

from password_hash_tool.cli import app

runner = CliRunner()


def test_hash_command():
    result = runner.invoke(app, ["hash", "--password", "testpass", "--algorithm", "bcrypt"])
    assert result.exit_code == 0
    assert "bcrypt" in result.stdout


def test_hash_invalid_algorithm():
    result = runner.invoke(app, ["hash", "--password", "testpass", "--algorithm", "md5"])
    assert result.exit_code == 1


def test_verify_command():
    hash_result = runner.invoke(app, ["hash", "--password", "testpass", "--algorithm", "argon2id"])
    import json

    output = json.loads(hash_result.stdout)
    hash_value = output["hash"]

    result = runner.invoke(app, ["verify", "--password", "testpass", "--hash", hash_value])
    assert result.exit_code == 0
    assert '"valid": true' in result.stdout


def test_benchmark_command():
    result = runner.invoke(app, ["benchmark", "--iterations", "1"])
    assert result.exit_code == 0
    assert "results" in result.stdout
