import time


class CacheService:
    """Caching service supporting Redis or in-memory dictionary fallback for caching dashboard stats & recommendations."""

    def __init__(self):
        self._memory_cache = {}

    def get(self, key: str):
        """Retrieves cached value if not expired."""
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if time.time() < entry["expires_at"]:
                return entry["value"]
            else:
                del self._memory_cache[key]
        return None

    def set(self, key: str, value, ttl_seconds: int = 300) -> None:
        """Stores value in cache with time-to-live in seconds."""
        self._memory_cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds
        }

    def delete(self, key: str) -> None:
        """Deletes key from cache."""
        self._memory_cache.pop(key, None)

    def clear(self) -> None:
        """Clears all cached items."""
        self._memory_cache.clear()
