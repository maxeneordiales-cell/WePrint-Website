from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse


HOST = "127.0.0.1"
PORT = 8000
SHOP_EMAIL = "weprintgraphixsolutions@gmail.com"
SITE_ROOT = Path(__file__).parent


def quote_details(service):
    subject = "Quote request" if not service else f"Quote request: {service}"
    lines = [
        "Hi WePrint Graphix Solutions,",
        "",
        f"I'd like a quote for: {service or '(describe the job)'}",
        "",
        "Size / dimensions:",
        "Quantity:",
        "Material or finish:",
        "Installation needed? (yes / no):",
        "Date needed:",
        "Artwork ready? (yes / no — we can lay it out for you):",
        "",
        "Name:",
        "Contact number:",
        "",
        "Thank you.",
    ]
    return subject, "\n".join(lines)


class WebsiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)

        if request.path == "/quote":
            service = parse_qs(request.query).get("service", [""])[0].strip()
            subject, body = quote_details(service)
            gmail_url = "https://mail.google.com/mail/?" + urlencode(
                {"view": "cm", "fs": "1", "to": SHOP_EMAIL, "su": subject, "body": body}
            )
            self.send_response(302)
            self.send_header("Location", gmail_url)
            self.end_headers()
            return

        if request.path in ("/", "/index.html"):
            content = (SITE_ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_error(404, "Not found")

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), WebsiteHandler)
    print(f"WePrint website running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()