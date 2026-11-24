from __future__ import annotations

import tomllib
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

SECRETS_PATH = Path(__file__).resolve().parents[2] / ".streamlit" / "secrets.toml"


class FirebaseConfigError(Exception):
    pass


def _streamlit_secrets() -> dict | None:
    try:
        import streamlit as st

        if "firebase" in st.secrets:
            return dict(st.secrets["firebase"])
    except Exception:
        pass
    return None


def _load_firebase_secrets() -> dict:
    from_streamlit = _streamlit_secrets()
    if from_streamlit is not None:
        return from_streamlit

    if not SECRETS_PATH.exists():
        raise FirebaseConfigError(
            ".streamlit/secrets.toml 파일이 없습니다. "
            "secrets.toml.example을 복사해서 값을 채워 주세요."
        )
    with SECRETS_PATH.open("rb") as f:
        data = tomllib.load(f)
    if "firebase" not in data:
        raise FirebaseConfigError("secrets.toml에 [firebase] 섹션이 없습니다.")
    return data["firebase"]


def get_api_key() -> str:
    api_key = _load_firebase_secrets().get("api_key", "")
    if not api_key:
        raise FirebaseConfigError("secrets.toml의 [firebase] api_key가 비어 있습니다.")
    return api_key


def init_firebase() -> firebase_admin.App:
    try:
        return firebase_admin.get_app()
    except ValueError:
        pass

    service_account = _load_firebase_secrets().get("service_account")
    if not service_account or not service_account.get("private_key"):
        raise FirebaseConfigError(
            "secrets.toml의 [firebase.service_account]가 비어 있습니다."
        )
    cred = credentials.Certificate(dict(service_account))
    return firebase_admin.initialize_app(cred)


def get_db():
    init_firebase()
    return firestore.client()
