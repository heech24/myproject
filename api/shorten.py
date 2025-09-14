import os, requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

# ====== 환경변수 (Vercel 대시보드에서 설정) ======
BULY_API_URL = os.environ.get("BULY_API_URL", "https://alie.kr/api/shoturl.siso")
CUSTOMER_ID = os.environ.get("BULY_CUSTOMER_ID", "dhgmlcks14")
PARTNER_API_ID = os.environ.get("BULY_PARTNER_API_ID", "B2B6FDCFD4AFB4D1EDFC7A47E948D450")

def _is_http_url(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

@app.post("/api/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    long_url = (data.get("url") or "").strip()
    if not _is_http_url(long_url):
        return ("invalid URL (http/https)", 400)
    if not (CUSTOMER_ID and PARTNER_API_ID):
        return ("missing API credentials", 500)

    payload = {
        "customer_id": CUSTOMER_ID,
        "partner_api_id": PARTNER_API_ID,
        "org_url": long_url
    }

    try:
        r = requests.post(BULY_API_URL, data=payload, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        return (f"upstream error: {e}", 502)

    # 예상 응답 예: {"result":"Y","url":"https://buly.kr/xxxxx","message":"..."}
    # 실제 포맷은 운영 정책에 따를 수 있으니 필요 시 key 이름을 아래에서 조정하세요.
    try:
        j = r.json()
    except ValueError:
        return ("unexpected response: " + r.text[:300], 502)

    ok_raw = str(j.get("result", "")).strip().upper()
    ok = ok_raw in ("Y", "TRUE", "1")
    if not ok:
        return (j.get("message") or "shorten failed", 400)

    short_url = j.get("url") or j.get("short_url")
    if not short_url:
        return ("missing 'url' in response", 502)

    return jsonify({"short_url": short_url, "provider": "buly"})