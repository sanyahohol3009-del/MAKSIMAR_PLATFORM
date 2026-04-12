from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_render_artifact import (
    build_operator_dashboard_first_render_artifact,
)


HOST = "127.0.0.1"
PORT = 8765


class OperatorDashboardLiveHandler(BaseHTTPRequestHandler):
    """Serve live truthful operator dashboard HTML."""

    def do_GET(self) -> None:
        """Serve the current truthful operator dashboard artifact."""
        artifact = build_operator_dashboard_first_render_artifact()
        html = artifact.html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, format: str, *args: object) -> None:
        """Reduce console noise from default HTTP logging."""
        return


def main() -> None:
    """Run local live operator dashboard server."""
    server = HTTPServer((HOST, PORT), OperatorDashboardLiveHandler)
    print(f"Operator dashboard live server running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
