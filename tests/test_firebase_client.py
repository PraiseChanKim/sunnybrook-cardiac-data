import pytest

from src.backend import firebase_client
from src.backend.firebase_client import FirebaseConfigError


def test_missing_secrets_file_raises_korean_message(monkeypatch, tmp_path):
    monkeypatch.setattr(firebase_client, "SECRETS_PATH", tmp_path / "none.toml")
    monkeypatch.setattr(firebase_client, "_streamlit_secrets", lambda: None)
    with pytest.raises(FirebaseConfigError, match="secrets.toml"):
        firebase_client.get_api_key()


def test_empty_api_key_raises(monkeypatch, tmp_path):
    path = tmp_path / "secrets.toml"
    path.write_text('[firebase]\napi_key = ""\n', encoding="utf-8")
    monkeypatch.setattr(firebase_client, "SECRETS_PATH", path)
    monkeypatch.setattr(firebase_client, "_streamlit_secrets", lambda: None)
    with pytest.raises(FirebaseConfigError, match="api_key"):
        firebase_client.get_api_key()


@pytest.mark.skipif(
    not firebase_client.SECRETS_PATH.exists(), reason="secrets.toml 없음"
)
def test_firestore_write_read_delete():
    db = firebase_client.get_db()
    ref = db.collection("_healthcheck").document("pytest_connection")
    ref.set({"ok": True})
    try:
        assert ref.get().to_dict() == {"ok": True}
    finally:
        ref.delete()
    assert not ref.get().exists
