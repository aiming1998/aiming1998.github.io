#!/usr/bin/env python3
"""Notify IndexNow after deployment; the ownership key is intentionally public.

--dry-run validates local configuration without making any network requests.
HTTP 200/202 are notification responses, never evidence of search indexing.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ENDPOINT = "https://api.indexnow.org/indexnow"
TIMEOUT = 15


def load_plan(root=ROOT):
    data = json.loads((root / "content.json").read_text(encoding="utf-8"))
    if data.get("publish_ready") is not True:
        raise ValueError("The site is not marked ready for publication.")
    site_url = data.get("site_url", "")
    parsed = urlsplit(site_url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or not site_url.isascii()
        or any(character.isspace() for character in site_url)
    ):
        raise ValueError("site_url must be an HTTPS site root without credentials, port, query, or fragment.")
    key = (root / "indexnow-key.txt").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9a-f]{32}", key):
        raise ValueError("indexnow-key.txt must contain the fixed 32-character lowercase hexadecimal key.")
    base = site_url.rstrip("/") + "/"
    return {
        "host": parsed.hostname,
        "key": key,
        "keyLocation": base + key + ".txt",
        "urlList": [base, base + "zh.html"],
    }


def warning(message):
    if os.environ.get("GITHUB_ACTIONS") == "true":
        escaped = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print("::warning title=IndexNow::" + escaped, file=sys.stderr)
    else:
        print("WARNING: " + message, file=sys.stderr)


def submit(plan):
    # A notification must not be sent until the deployed ownership file matches.
    verification = Request(plan["keyLocation"], headers={"Accept": "text/plain"})
    with urlopen(verification, timeout=TIMEOUT) as response:
        if response.status != 200 or response.geturl() != plan["keyLocation"]:
            raise ValueError("The deployed key URL did not return HTTP 200 at its exact location; no notification sent.")
        online_key = response.read(1024).decode("utf-8-sig").strip()
        if online_key != plan["key"]:
            raise ValueError("The deployed key text does not match indexnow-key.txt; no notification sent.")

    request = Request(
        ENDPOINT,
        data=json.dumps(plan).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urlopen(request, timeout=TIMEOUT) as response:
        if response.geturl() != ENDPOINT:
            raise ValueError("IndexNow redirected the notification; receipt is not confirmed.")
        status = response.status
    if status == 200:
        print("IndexNow HTTP 200: URL notification received. This does not confirm crawling or indexing.")
    elif status == 202:
        warning("IndexNow HTTP 202: notification accepted, key validation pending. This does not confirm crawling or indexing.")
    else:
        raise ValueError(f"Unexpected IndexNow HTTP {status}; receipt is not confirmed.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Validate local host, URLs, and key; perform no requests")
    args = parser.parse_args(argv)
    try:
        plan = load_plan()
        if args.dry_run:
            print(json.dumps({
                "host": plan["host"],
                "urls": plan["urlList"],
                "validation": {
                    "https_root_and_matching_host": all(urlsplit(url).hostname == plan["host"] for url in plan["urlList"]),
                    "public_key_format": "valid: 32 lowercase hexadecimal characters",
                    "online_key": "not checked; dry-run makes no requests",
                },
            }, indent=2))
        else:
            submit(plan)
    except (OSError, ValueError, KeyError) as error:
        warning(f"IndexNow notification incomplete: {error}. Site deployment is unaffected.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
