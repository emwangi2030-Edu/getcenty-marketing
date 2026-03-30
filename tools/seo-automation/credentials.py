"""Load Google service account credentials from file or JSON env (CI-friendly)."""

import json
import os
from pathlib import Path
from google.oauth2 import service_account


def load_credentials(scopes):
    """Prefer GOOGLE_APPLICATION_CREDENTIALS_JSON (raw JSON string), else file path."""
    raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if raw:
        info = json.loads(raw)
        return service_account.Credentials.from_service_account_info(info, scopes=scopes)

    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if path and Path(path).is_file():
        return service_account.Credentials.from_service_account_file(path, scopes=scopes)

    raise RuntimeError(
        "Set GOOGLE_APPLICATION_CREDENTIALS_JSON (entire JSON) or "
        "GOOGLE_APPLICATION_CREDENTIALS (path to .json file)."
    )
