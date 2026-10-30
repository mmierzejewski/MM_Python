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

    def test_parse_schedule_time_valid(self) -> None:
        self.assertEqual(clear_caches.parse_schedule_time("03:30"), (3, 30))
        self.assertEqual(clear_caches.parse_schedule_time("00:00"), (0, 0))
        self.assertEqual(clear_caches.parse_schedule_time("23:59"), (23, 59))
        self.assertEqual(clear_caches.parse_schedule_time("9:05"), (9, 5))

    def test_parse_schedule_time_invalid(self) -> None:
        invalid_inputs = ["abc", "24:00", "12:60", "-1:30", "12", "12:34:56", "ab:cd"]
        for val in invalid_inputs:
            with self.subTest(val=val):
                with self.assertRaises(ValueError):
                    clear_caches.parse_schedule_time(val)

    def test_get_all_targets_includes_static_targets(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            targets = clear_caches.get_all_targets()
        paths = {t.path for t in targets}
        for static in clear_caches.TARGETS:
            self.assertIn(static.path, paths)

    def test_reindex_skips_sudo_tasks_when_not_root(self) -> None:
        output = io.StringIO()
        with patch("os.geteuid", return_value=1000, create=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value.returncode = 0
                with contextlib.redirect_stdout(output):
                    clear_caches.run_reindex(dry_run=False)
        stdout = output.getvalue()
        self.assertIn("Skipped (wymaga uprawnień root / sudo)", stdout)

    def test_get_protected_pids_includes_self_and_vscode_pid(self) -> None:
        with patch.dict(os.environ, {"VSCODE_PID": "99999"}):
            pids = clear_caches.get_protected_pids()
            self.assertIn(os.getpid(), pids)
            self.assertIn(os.getppid(), pids)
            self.assertIn(99999, pids)

    def test_get_running_applications_filters_protected(self) -> None:
        sample_lsappinfo = """
 1) "Finder" ASN:0x0-0x1111:
    bundleID="com.apple.finder"
    bundle path="/System/Library/CoreServices/Finder.app"
    pid = 1001 type="Foreground"
 2) "Terminal" ASN:0x0-0x2222:
    bundleID="com.apple.Terminal"
    bundle path="/System/Applications/Utilities/Terminal.app"
    pid = 1002 type="Foreground"
 3) "Google Chrome" ASN:0x0-0x3333:
    bundleID="com.google.Chrome"
    bundle path="/Applications/Google Chrome.app"
    pid = 1003 type="Foreground"
 4) "Slack" ASN:0x0-0x4444:
    bundleID="com.tinyspeck.slackmacgap"
    bundle path="/Applications/Slack.app"
    pid = 1004 type="Foreground"
 5) "RandomDaemon" ASN:0x0-0x5555:
    bundleID="com.example.daemon"
    bundle path="/Library/PrivilegedHelperTools/daemon"
    pid = 1005 type="BackgroundOnly"
"""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = sample_lsappinfo
            with patch.object(clear_caches, "get_protected_pids", return_value={9999}):
                apps = clear_caches.get_running_applications()
                app_names = [a.name for a in apps]
                self.assertIn("Google Chrome", app_names)
                self.assertIn("Slack", app_names)
                self.assertNotIn("Finder", app_names)
                self.assertNotIn("Terminal", app_names)
                self.assertNotIn("RandomDaemon", app_names)

    def test_close_running_applications_dry_run_does_not_kill(self) -> None:
        apps = [clear_caches.RunningApp(name="TestApp", pid=55555)]
        output = io.StringIO()
        with patch("os.kill") as mock_kill:
            with contextlib.redirect_stdout(output):
                lines = clear_caches.close_running_applications(apps, dry_run=True)
            mock_kill.assert_not_called()
            self.assertTrue(any("[dry-run] would force quit" in line for line in lines))

    def test_close_running_applications_kills_process(self) -> None:
        apps = [clear_caches.RunningApp(name="TestApp", pid=55555)]
        output = io.StringIO()
        with patch("os.kill") as mock_kill, patch("time.sleep"):
            # First os.kill is SIGTERM, second is os.kill(pid, 0) which raises ProcessLookupError (exited)
            mock_kill.side_effect = [None, ProcessLookupError()]
            with contextlib.redirect_stdout(output):
                lines = clear_caches.close_running_applications(apps, dry_run=False)
            self.assertTrue(mock_kill.called)
            self.assertTrue(any("Closed: TestApp" in line for line in lines))

    def test_stale_jetbrains_keeps_newest_version_per_product(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for name in ("PyCharm2025.2", "PyCharm2026.10", "PyCharm2026.2",
                         "IntelliJIdea2025.3", "Pycharm", "consentOptions"):
                (root / name).mkdir()

            stale = {p.name for p in clear_caches.stale_jetbrains_config_dirs(root)}

            self.assertEqual(stale, {"PyCharm2025.2", "PyCharm2026.2"})

    def test_broken_symlinks_and_remove_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            bin_dir = Path(temporary_directory)
            (bin_dir / "real").write_text("x")
            (bin_dir / "ok").symlink_to(bin_dir / "real")
            (bin_dir / "dead").symlink_to(bin_dir / "missing")

            found = clear_caches.broken_symlinks((bin_dir,))
            self.assertEqual(found, [bin_dir / "dead"])

            _, entries, _ = clear_caches.remove_path(found[0], dry_run=True)
            self.assertEqual(entries, 1)
            self.assertTrue((bin_dir / "dead").is_symlink())

            _, entries, _ = clear_caches.remove_path(found[0], dry_run=False)
            self.assertEqual(entries, 1)
            self.assertFalse(os.path.lexists(bin_dir / "dead"))
            self.assertTrue((bin_dir / "ok").exists())

    def test_confirm_includes_apps_warning(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", return_value="y") as mock_input, contextlib.redirect_stdout(output):
            res = clear_caches.confirm(1024, to_trash=False, apps_count=5)
            self.assertTrue(res)
            mock_input.assert_called_with("This will force-quit 5 running application(s) and permanently delete the listed items. Continue? [y/N]: ")


if __name__ == "__main__":
    unittest.main()
