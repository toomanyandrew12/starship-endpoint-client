from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import app


class ConfigTests(unittest.TestCase):
    def test_missing_endpoint_has_stable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "starship.ini"
            with self.assertRaisesRegex(
                RuntimeError, "ServiceEndpoint not configured"
            ):
                app.load_endpoint(path)


if __name__ == "__main__":
    unittest.main()
