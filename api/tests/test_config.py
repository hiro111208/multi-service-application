from app.config import read_secret


def test_read_secret_from_file(tmp_path, monkeypatch):
    secret_file = tmp_path / "password.txt"
    secret_file.write_text("secret-value\n", encoding="utf-8")
    monkeypatch.setenv("MONGODB_PASSWORD_FILE", str(secret_file))

    assert read_secret("MONGODB_PASSWORD") == "secret-value"


def test_read_secret_falls_back_to_env(monkeypatch):
    monkeypatch.delenv("MONGODB_PASSWORD_FILE", raising=False)
    monkeypatch.setenv("MONGODB_PASSWORD", "env-value")

    assert read_secret("MONGODB_PASSWORD") == "env-value"


def test_read_secret_returns_default_when_missing(monkeypatch):
    monkeypatch.delenv("MONGODB_PASSWORD_FILE", raising=False)
    monkeypatch.delenv("MONGODB_PASSWORD", raising=False)

    assert read_secret("MONGODB_PASSWORD", default="fallback") == "fallback"
