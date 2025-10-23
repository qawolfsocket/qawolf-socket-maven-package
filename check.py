#!/usr/bin/env python3
"""
Verify a Sonatype Central Portal *User Token* (username + password).

Usage:
  export CENTRAL_USERNAME=ut_xxxxx
  export CENTRAL_PASSWORD=pt_xxxxx
  python3 check_central_token.py
"""
import base64, os, sys, urllib.request

u = os.getenv("CENTRAL_USERNAME", "H5CCah")
p = os.getenv("CENTRAL_PASSWORD", "gC8FShAMnD0X3HrHbeEWMZpBT8kxtP8in")

def bad(msg):
    print(f"[!] {msg}")
    sys.exit(1)


# Quick whitespace sanity check (doesn't print the creds themselves)
def has_weird_ws(s: str) -> bool:
    return any(ch in s for ch in ("\r", "\n", "\t", " "))

if has_weird_ws(u) or has_weird_ws(p):
    bad("Your token values appear to contain whitespace. Re-copy them cleanly from the Portal.")
bearer = base64.b64encode(f"{u}:{p}".encode()).decode()

req = urllib.request.Request(
    "https://central.sonatype.com/api/v1/publisher/upload",
    method="POST",
    headers={"Authorization": f"Bearer {bearer}"}
)
try:
    urllib.request.urlopen(req, timeout=20)
    # If Central ever returns 2xx with empty body (unlikely), call it "OK"
    print("[+] Token accepted (unexpected 2xx)")
except urllib.error.HTTPError as e:
    if e.code in (400, 415):
        print(f"[+] Token accepted (HTTP {e.code} for bad/missing form-data)")
    elif e.code == 401:
        print("[!] Token rejected (HTTP 401) – wrong/expired user token.")
    else:
        print(f"[?] Server returned HTTP {e.code} – not conclusive.")
except Exception as e:
    print(f"[!] Request failed: {e}")