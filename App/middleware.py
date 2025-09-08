class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        # Block browser features you don't need
        resp["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
        )

        # Cross-origin isolation helpers (tighten if you use WebAssembly/SharedArrayBuffer)
        resp["Cross-Origin-Embedder-Policy"] = "require-corp"   # or "credentialless"
        resp["Cross-Origin-Resource-Policy"] = "same-site"      # or "same-origin"

        return resp
