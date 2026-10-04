import contextlib
import io
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import clear_caches


class ClearCachesTests(unittest.TestCase):
    def test_age_filter_preserves_directory_with_recent_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "cache"
            nested = target / "nested"
            nested.mkdir(parents=True)
            recent_file = nested / "recent.dat"
            recent_file.write_text("recent")

            old_time = time.time() - 10 * 86400
            os.utime(nested, (old_time, old_time))
            os.utime(target, (old_time, old_time))

            lines, entries, size = clear_caches.clear_directory(
                target, dry_run=True, older_than_days=1
            )

            self.assertEqual((entries, size), (0, 0))
            self.assertTrue(any("[skipped-age]" in line for line in lines))
            self.assertFalse(any("[dry-run]" in line for line in lines))
            self.assertTrue(recent_file.exists())

    def test_age_filter_still_selects_entirely_old_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "cache"
            nested = target / "nested"
            nested.mkdir(parents=True)
            old_file = nested / "old.dat"
            old_file.write_text("old")

            old_time = time.time() - 10 * 86400
            os.utime(old_file, (old_time, old_time))
            os.utime(nested, (old_time, old_time))
            os.utime(target, (old_time, old_time))

            lines, entries, size = clear_caches.clear_directory(
                target, dry_run=True, older_than_days=1
            )

            self.assertEqual((entries, size), (1, 3))
            self.assertTrue(any("[dry-run] would remove:" in line for line in lines))

    def test_browser_profile_scan_skips_permission_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_root = Path(temporary_directory)
            output = io.StringIO()
            with patch.object(Path, "iterdir", side_effect=PermissionError("denied")):
                with contextlib.redirect_stdout(output):
                    targets = clear_caches.browser_profile_targets(cache_root, "Chrome")

            self.assertEqual(targets, [])
            self.assertIn("Could not scan browser profiles", output.getvalue())

    def test_application_support_scan_adds_known_caches_but_not_data_stores(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "Code" / "DawnGraphiteCache").mkdir(parents=True)
            (root / "Google" / "Chrome" / "Default" / "Cache").mkdir(parents=True)
            (root / "Nikon" / "NX Studio" / "Cache").mkdir(parents=True)
            (root / "Shared App" / "Shared Dictionary" / "cache").mkdir(parents=True)
            (root / "Drive" / "content_cache").mkdir(parents=True)
            (root / "Chat" / "blob_storage").mkdir(parents=True)

            targets = clear_caches.application_support_cache_targets(root)
            discovered = {target.path.relative_to(root).as_posix(): target for target in targets}

            self.assertIn("Code/DawnGraphiteCache", discovered)
            self.assertEqual(discovered["Code/DawnGraphiteCache"].category, "developer")
            self.assertEqual(discovered["Google/Chrome/Default/Cache"].category, "browsers")
            self.assertIn("Nikon/NX Studio/Cache", discovered)
            self.assertIn("Shared App/Shared Dictionary/cache", discovered)
            self.assertNotIn("Drive/content_cache", discovered)
            self.assertNotIn("Chat/blob_storage", discovered)

    def test_sandbox_scan_adds_third_party_cache_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            third_party_cache = (
                root / "com.microsoft.OneDrive-mac" / "Data" / "Library" / "Caches"
            )
            apple_cache = root / "com.apple.mail" / "Data" / "Library" / "Caches"
            third_party_cache.mkdir(parents=True)
            apple_cache.mkdir(parents=True)

            targets = clear_caches.sandboxed_app_cache_targets(root)

            self.assertEqual([target.path for target in targets], [third_party_cache])
            self.assertEqual(targets[0].category, "apps")

    def test_frozen_runtime_uses_executable_directory_and_schedule_arguments(self) -> None:
        executable = "/Applications/Clear Caches/clear_caches"
        with patch.object(clear_caches.sys, "frozen", True, create=True):
            with patch.object(clear_caches.sys, "executable", executable):
                self.assertEqual(
                    clear_caches.application_directory(),
                    Path(executable).parent,
                )
                self.assertEqual(
                    clear_caches.schedule_program_arguments(),
                    [executable, "--yes", "--no-reindex"],
                )


if __name__ == "__main__":
    unittest.main()