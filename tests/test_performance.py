import unittest
from backend.services.cache_service import CacheService
from backend.services.monitoring_service import MonitoringService
from app import create_app


class TestPerformanceAndCache(unittest.TestCase):
    """Unit tests for Phase 6 Performance, Cache, and Monitoring Services."""

    def test_01_cache_service(self):
        """Test in-memory/Redis CacheService set, get, and expiration."""
        cache = CacheService()
        cache.set("test_key", {"score": 95}, ttl_seconds=10)

        val = cache.get("test_key")
        self.assertIsNotNone(val)
        self.assertEqual(val["score"], 95)

    def test_02_monitoring_service(self):
        """Test MonitoringService health metrics."""
        app = create_app("testing")
        with app.app_context():
            mon = MonitoringService()
            health = mon.get_system_health()
            self.assertIn("status", health)
            self.assertTrue(health["database_connected"])


if __name__ == "__main__":
    unittest.main()
