"""Middleware chuyển URL path về lowercase (giống routing case-insensitive của .NET)."""
from starlette.middleware.base import BaseHTTPMiddleware


class LowercasePathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        scope = request.scope
        path = scope.get("path", "")
        low = path.lower()
        if low != path:
            scope["path"] = low
            scope["raw_path"] = low.encode()
        return await call_next(request)
