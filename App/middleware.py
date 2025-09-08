class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        # Permissions-Policy (you already had something like this)
        resp["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=(), usb=()"

        # Cross-origin protections (optional but good)
        resp["Cross-Origin-Embedder-Policy"] = "require-corp"
        resp["Cross-Origin-Resource-Policy"] = "same-site"

        # ⭐ Content Security Policy (CSP) — allows your Bootstrap CDN + inline scripts you use
        resp["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'"
        )

        return resp
