import contextlib
import io
import json
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

    def test_load_external_targets_validates_entries_and_rejects_home_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            app_dir = root / "app"
            home = root / "home"
            target = home / "Library" / "Caches" / "Example"
            app_dir.mkdir()
            target.mkdir(parents=True)
            config = [
                {"path": str(target), "label": "Example Cache", "category": "apps"},
                {"path": "~", "label": "Home", "category": "apps"},
                {"path": "/", "label": "Filesystem", "category": "apps"},
                {"path": str(target), "label": "Unknown", "category": "unknown"},
                {"path": str(target), "category": "apps"},
                "not an object",
            ]
            (app_dir / "targets.json").write_text(json.dumps(config))
            output = io.StringIO()

            with patch.object(clear_caches, "application_directory", return_value=app_dir):
                with patch.dict(os.environ, {"HOME": str(home)}):
                    with contextlib.redirect_stdout(output):
                        targets = clear_caches.load_external_targets()

            self.assertEqual(
                targets,
                [clear_caches.Target(target.resolve(), "Example Cache", "apps")],
            )
            self.assertIn("home directory or one of its parents", output.getvalue())
            self.assertIn("invalid category", output.getvalue())

    def test_load_external_targets_skips_non_list_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            app_dir = Path(temporary_directory)
            (app_dir / "targets.json").write_text('{"path": "/tmp/cache"}')
            output = io.StringIO()

            with patch.object(clear_caches, "application_directory", return_value=app_dir):
                with contextlib.redirect_stdout(output):
                    targets = clear_caches.load_external_targets()

            self.assertEqual(targets, [])
            self.assertIn("expected a JSON list", output.getvalue())

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
                    [executable, "--yes", "--no-reindex", "--no-kill-apps"],
                )

    def test_scan_tree_counts_unreadable_entries_without_raising(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "file.dat").write_text("abc")
            with patch.object(Path, "lstat", side_effect=PermissionError("denied")):
                scan = clear_caches.scan_tree(root)

        self.assertEqual((scan.size, scan.is_old, scan.errors), (0, False, 1))

    def test_cleaning_reuses_planned_sizes_without_rescanning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target_dir = Path(temporary_directory) / "cache"
            target_dir.mkdir()
            (target_dir / "a.dat").write_text("12345")
            plan = clear_caches.plan_target(clear_caches.Target(target_dir, "Cache", "apps"), None)

            with patch.object(clear_caches, "scan_tree", side_effect=AssertionError("rescanned")):
                clear_caches.refresh_plan(plan, None)
                lines, entries, size = clear_caches.execute_plan(plan, dry_run=False)

            self.assertEqual((entries, size), (1, 5))
            self.assertEqual(list(target_dir.iterdir()), [])

    def test_refresh_plan_adds_children_created_after_planning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target_dir = Path(temporary_directory)
            plan = clear_caches.plan_target(clear_caches.Target(target_dir, "Cache", "apps"), None)
            (target_dir / "late.dat").write_text("late")

            clear_caches.refresh_plan(plan, None)

            self.assertEqual([item.path.name for item in plan.items], ["late.dat"])

    def test_move_to_trash_keeps_same_named_items_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = root / "first" / "cache"
            second = root / "second" / "cache"
            first.parent.mkdir()
            second.parent.mkdir()
            first.write_text("first")
            second.write_text("second")

            with patch.object(Path, "home", return_value=root):
                with patch.object(clear_caches.time, "time_ns", return_value=123):
                    clear_caches.move_to_trash(first)
                    clear_caches.move_to_trash(second)

            trashed_items = sorted((root / ".Trash").iterdir())
            self.assertEqual(len(trashed_items), 2)
            self.assertEqual({item.read_text() for item in trashed_items}, {"first", "second"})

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

    def test_cleanup_targets_skip_shared_tmp_and_the_run_log_directory(self) -> None:
        self.assertNotIn("tmp", clear_caches.ALL_CATEGORIES)
        self.assertFalse(any(target.path == Path("/private/tmp") for target in clear_caches.TARGETS))

        log_targets = [target for target in clear_caches.TARGETS if target.category == "logs"]
        self.assertTrue(log_targets)
        self.assertFalse(any(clear_caches.LOG_DIR.is_relative_to(t.path) for t in log_targets))

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
 5) "TextEdit" ASN:0x0-0x5555:
    bundleID="com.apple.TextEdit"
    bundle path="/Applications/TextEdit.app"
    pid = 1005 type="Foreground"
 6) "RandomDaemon" ASN:0x0-0x6666:
    bundleID="com.example.daemon"
    bundle path="/Library/PrivilegedHelperTools/daemon"
    pid = 1006 type="BackgroundOnly"
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
                self.assertNotIn("TextEdit", app_names)
                self.assertNotIn("RandomDaemon", app_names)

    def test_still_running_apps_drops_reused_pids(self) -> None:
        chrome = clear_caches.RunningApp("Google Chrome", 1003, "com.google.Chrome")
        slack = clear_caches.RunningApp("Slack", 1004, "com.tinyspeck.slackmacgap")
        reused = clear_caches.RunningApp("Spotify", 1004, "com.spotify.client")
        with patch.object(clear_caches, "get_running_applications", return_value=[chrome, reused]):
            self.assertEqual(clear_caches.still_running_apps([chrome, slack]), [chrome])

    def test_application_support_scan_skips_private_roots_and_service_workers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "MobileSync" / "Backup" / "Cache").mkdir(parents=True)
            (root / "PWA" / "Service Worker" / "CacheStorage").mkdir(parents=True)
            (root / "PWA" / "Service Worker" / "Cache").mkdir(parents=True)

            targets = clear_caches.application_support_cache_targets(root, known_paths=set())

            self.assertEqual(targets, [])

    def test_install_schedule_reloads_agent_and_fails_on_bootstrap_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            plist_path = root / "agent.plist"
            calls: list[tuple[str, ...]] = []

            def fake_launchctl(*arguments: str):
                calls.append(arguments)
                code = 5 if arguments[0] == "bootstrap" else 0
                return clear_caches.subprocess.CompletedProcess(arguments, code, "", "boom")

            with patch.object(clear_caches, "LAUNCH_AGENT_PATH", plist_path), \
                    patch.object(clear_caches, "LOG_DIR", root / "logs"), \
                    patch.object(clear_caches, "run_launchctl", side_effect=fake_launchctl), \
                    contextlib.redirect_stderr(io.StringIO()) as error_output:
                with self.assertRaises(SystemExit) as raised:
                    clear_caches.install_schedule("03:00")

            self.assertEqual(raised.exception.code, 1)
            self.assertEqual([call[0] for call in calls], ["bootout", "bootstrap"])
            self.assertIn("boom", error_output.getvalue())

    def test_main_rejects_negative_older_than(self) -> None:
        with patch("sys.argv", ["clear_caches.py", "--older-than", "-1"]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    clear_caches.main()
        self.assertEqual(raised.exception.code, 2)

    def test_format_signed_size_handles_negative_delta(self) -> None:
        self.assertEqual(clear_caches.format_signed_size(-2048), "-2.0KB")
        self.assertEqual(clear_caches.format_signed_size(512), "+512B")

    def test_send_notification_escapes_applescript_strings(self) -> None:
        with patch("subprocess.run") as mock_run:
            clear_caches.send_notification('Title "x"', 'a\\b "c"')
        script = mock_run.call_args[0][0][2]
        self.assertEqual(
            script, 'display notification "a\\\\b \\"c\\"" with title "Title \\"x\\""'
        )

    def test_main_exclusions_do_not_mutate_category_constants(self) -> None:
        all_categories = set(clear_caches.ALL_CATEGORIES)
        default_categories = set(clear_caches.DEFAULT_CATEGORIES)
        invocations = (
            ["--exclude", "system"],
            ["--all", "--exclude", "system"],
        )

        for arguments in invocations:
            with self.subTest(arguments=arguments):
                with patch("sys.argv", ["clear_caches.py", *arguments, "--dry-run", "--no-log"]):
                    with patch.object(clear_caches, "get_all_targets", return_value=[]):
                        with patch.object(clear_caches, "get_running_applications", return_value=[]):
                            with patch.object(clear_caches, "maintenance_tasks", return_value=[]):
                                with patch.object(clear_caches, "run_maintenance"):
                                    clear_caches.main()

        self.assertEqual(clear_caches.ALL_CATEGORIES, all_categories)
        self.assertEqual(clear_caches.DEFAULT_CATEGORIES, default_categories)

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

    def test_is_root_user(self) -> None:
        with patch("os.geteuid", return_value=0):
            self.assertTrue(clear_caches.is_root_user())
        with patch("os.geteuid", return_value=501):
            self.assertFalse(clear_caches.is_root_user())

    def test_main_rejects_running_as_root(self) -> None:
        for arguments in (["--dry-run"], ["--install-schedule", "03:00"]):
            with self.subTest(arguments=arguments):
                with patch("sys.argv", ["clear_caches.py", *arguments]):
                    with patch.object(clear_caches, "is_root_user", return_value=True):
                        with patch.object(clear_caches, "get_all_targets") as mock_targets:
                            with contextlib.redirect_stderr(io.StringIO()):
                                with self.assertRaises(SystemExit) as raised:
                                    clear_caches.main()

                self.assertEqual(raised.exception.code, 2)
                mock_targets.assert_not_called()


if __name__ == "__main__":
    unittest.main()
