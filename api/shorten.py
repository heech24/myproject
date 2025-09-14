import os
import json
import requests
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """CORS preflight 요청 처리"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """POST 요청 처리"""
        try:
            # 요청 본문 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8')) if post_data else {}
            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON")
                return

            long_url = (data.get("url") or "").strip()

            # URL 유효성 검사
            if not self._is_http_url(long_url):
                self.send_error_response(400, "Invalid URL format")
                return

            # 환경변수 확인
            CUSTOMER_ID = os.environ.get("BULY_CUSTOMER_ID", "dhgmlcks14")
            PARTNER_API_ID = os.environ.get("BULY_PARTNER_API_ID", "B2B6FDCFD4AFB4D1EDFC7A47E948D450")
            BULY_API_URL = os.environ.get("BULY_API_URL", "https://alie.kr/api/shoturl.siso")

            if not (CUSTOMER_ID and PARTNER_API_ID):
                self.send_error_response(500, "Missing API credentials")
                return

            # buly.kr API 호출
            payload = {
                "customer_id": CUSTOMER_ID,
                "partner_api_id": PARTNER_API_ID,
                "org_url": long_url
            }

            try:
                response = requests.post(BULY_API_URL, data=payload, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                self.send_error_response(502, f"API request failed: {str(e)}")
                return

            # 응답 파싱
            try:
                result = response.json()
            except ValueError:
                self.send_error_response(502, "Invalid API response format")
                return

            # 응답 검증
            ok_raw = str(result.get("result", "")).strip().upper()
            ok = ok_raw in ("Y", "TRUE", "1")

            if not ok:
                error_msg = result.get("message", "URL shortening failed")
                self.send_error_response(400, error_msg)
                return

            short_url = result.get("url") or result.get("short_url")
            if not short_url:
                self.send_error_response(502, "No short URL in response")
                return

            # 성공 응답
            self.send_success_response({
                'short_url': short_url,
                'provider': 'buly',
                'original_url': long_url
            })

        except Exception as e:
            self.send_error_response(500, f"Internal error: {str(e)}")

    def do_GET(self):
        """GET 요청 처리 (테스트용)"""
        self.send_success_response({
            'status': 'API is running',
            'endpoint': '/api/shorten',
            'method': 'POST'
        })

    def send_success_response(self, data):
        """성공 응답 전송"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def send_error_response(self, code, message):
        """에러 응답 전송"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps({
            'error': message,
            'code': code
        }, ensure_ascii=False).encode('utf-8'))

    def _is_http_url(self, url: str) -> bool:
        """URL 유효성 검사"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ("http", "https") and bool(parsed.netloc)
        except Exception:
            return False