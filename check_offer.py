"""Public-only check: no credentials, wallet storage, signatures, or payments."""
import base64
import json
import sys
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    payload = json.dumps({"input": "First example line\nSecond example line", "options": {"minChars": 3}}).encode()
    request = urllib.request.Request("https://route-a-worker.frostskynet-api.workers.dev/clean", data=payload,
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        response = urllib.request.build_opener(NoRedirect).open(request, timeout=15)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        header = response.headers.get("payment-required", "")
        required = json.loads(base64.b64decode(header, validate=True)) if 0 < len(header) <= 200000 else {}
        accepts = required.get("accepts", [])
        matches = response.code == 402 and required.get("x402Version") == 2 and len(accepts) == 1 and all(
            a.get("scheme") == "exact" and a.get("network") == "eip155:8453" and a.get("amount") == "5000"
            and a.get("asset", "").lower() == "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
            and a.get("payTo", "").lower() == "0x3a1121e787586a504ff74fc53e3acee19fade698" for a in accepts)
        print("HTTP status:", response.code)
        print("Expected payment terms:", bool(matches))
        return 0 if matches else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("Unpaid offer check failed; raw diagnostics suppressed. No payment was sent.")
        sys.exit(1)
