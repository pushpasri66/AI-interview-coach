import os
import unittest
from config import config_by_name


class TestDeploymentConfigurations(unittest.TestCase):
    """Unit tests for Phase 6 Deployment Configurations & Files."""

    def test_01_environment_configs(self):
        """Test Development, Production, and Testing configuration objects."""
        dev_cfg = config_by_name["development"]
        prod_cfg = config_by_name["production"]
        test_cfg = config_by_name["testing"]

        self.assertTrue(dev_cfg.DEBUG)
        self.assertFalse(prod_cfg.DEBUG)
        self.assertTrue(test_cfg.TESTING)

    def test_02_deployment_files_exist(self):
        """Test that Dockerfile, docker-compose.yml, nginx.conf, and gunicorn.conf.py exist."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "deployment", "Dockerfile")))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "deployment", "docker-compose.yml")))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "deployment", "nginx.conf")))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "deployment", "gunicorn.conf.py")))


if __name__ == "__main__":
    unittest.main()
