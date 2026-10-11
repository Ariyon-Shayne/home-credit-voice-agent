"""Retrieve metadata for an existing Retell call; does not place calls."""
import json
import os
import sys

try:
    from retell import Retell
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)


def main():
    api_key = os.getenv("RETELL_API_KEY")
    call_id = os.getenv("RETELL_CALL_ID")
    if not api_key or not call_id:
        raise SystemExit(
            "Set RETELL_API_KEY and RETELL_CALL_ID environment variables."
        )

    client = Retell(api_key=api_key)
    call = client.call.retrieve(call_id)

    # SDK models may expose attributes or model_dump depending on version.
    if hasattr(call, "model_dump"):
        data = call.model_dump()
    elif hasattr(call, "dict"):
        data = call.dict()
    else:
        data = {
            "call_id": getattr(call, "call_id", None),
            "transcript": getattr(call, "transcript", None),
            "recording_url": getattr(call, "recording_url", None),
            "public_log_url": getattr(call, "public_log_url", None),
        }

    wanted = {
        key: data.get(key)
        for key in ("call_id", "transcript", "recording_url", "public_log_url")
        if isinstance(data, dict) and data.get(key) is not None
    }
    print(json.dumps(wanted, indent=2, ensure_ascii=False))
    print("\nCheck access and expiry of returned URLs before submitting.")


if __name__ == "__main__":
    main()
