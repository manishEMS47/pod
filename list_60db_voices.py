import os
import sys
import requests

SIXTYDB_API_KEY = os.getenv("SIXTYDB_API_KEY")


def list_voices():
    if not SIXTYDB_API_KEY:
        print("SIXTYDB_API_KEY is not set. Export it first, e.g. export SIXTYDB_API_KEY=sk_live_...")
        sys.exit(1)

    url = "https://api.60db.ai/myvoices"
    headers = {"Authorization": f"Bearer {SIXTYDB_API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"60db API error: {response.status_code} - {response.text}")
        sys.exit(1)

    payload = response.json()
    voices = payload.get("data", [])
    if not voices:
        print("No voices found on this account.")
        return

    # Column widths
    header = f"{'voice_id':<38}  {'gender':<7}  {'language':<8}  {'model':<12}  name"
    print(header)
    print("-" * len(header))
    for v in voices:
        labels = v.get("labels") or {}
        print(
            f"{v.get('voice_id', ''):<38}  "
            f"{labels.get('gender', ''):<7}  "
            f"{labels.get('language', ''):<8}  "
            f"{v.get('model', ''):<12}  "
            f"{v.get('name', '')}"
        )

    print(f"\n{len(voices)} voice(s). Copy a voice_id into main.py -> voice_sarah_id.")


if __name__ == "__main__":
    list_voices()
