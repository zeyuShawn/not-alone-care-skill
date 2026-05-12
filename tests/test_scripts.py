from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_command(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


def run_script(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_command([PYTHON, *args], check=check)


class ScriptSafetyTests(unittest.TestCase):
    def test_event_requires_consent_and_valid_scores(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            no_consent = run_script(
                ["scripts/append_event_log.py", "--data-dir", data_dir, "--field", "mood_score=4"],
                check=False,
            )
            self.assertNotEqual(no_consent.returncode, 0)
            self.assertIn("save_consent=true", no_consent.stderr)

            bad_score = run_script(
                [
                    "scripts/append_event_log.py",
                    "--data-dir",
                    data_dir,
                    "--field",
                    "save_consent=true",
                    "--field",
                    "mood_score=11",
                ],
                check=False,
            )
            self.assertNotEqual(bad_score.returncode, 0)
            self.assertIn("mood_score", bad_score.stderr)

    def test_support_contact_method_requires_second_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            run_script(
                [
                    "scripts/manage_support_contacts.py",
                    "--data-dir",
                    data_dir,
                    "add",
                    "--field",
                    "name_or_alias=friend",
                    "--field",
                    "contact_method=555-0100",
                    "--field",
                    "consent_to_use=true",
                ]
            )
            hidden = run_script(["scripts/manage_support_contacts.py", "--data-dir", data_dir, "show", "--name", "friend"])
            self.assertNotIn("contact_method", hidden.stdout)
            refused = run_script(
                [
                    "scripts/manage_support_contacts.py",
                    "--data-dir",
                    data_dir,
                    "show",
                    "--name",
                    "friend",
                    "--include-contact-method",
                ],
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0)
            revealed = run_script(
                [
                    "scripts/manage_support_contacts.py",
                    "--data-dir",
                    data_dir,
                    "show",
                    "--name",
                    "friend",
                    "--include-contact-method",
                    "--confirm-user-consent",
                    "YES",
                ]
            )
            self.assertIn("555-0100", revealed.stdout)

    def test_job_cache_save_requires_consent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "jobs.json"
            input_path.write_text(json.dumps([{"title": "Frontend", "skills": ["React"]}]), encoding="utf-8")
            data_dir = tmp_path / "data"

            refused = run_script(
                [
                    "scripts/collect_job_posts_browser.py",
                    "--data-dir",
                    str(data_dir),
                    "--input",
                    str(input_path),
                    "--consent",
                    "false",
                ],
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0)

            ok = run_script(
                [
                    "scripts/collect_job_posts_browser.py",
                    "--data-dir",
                    str(data_dir),
                    "--input",
                    str(input_path),
                    "--consent",
                    "true",
                ]
            )
            self.assertIn('"status": "ok"', ok.stdout)

    def test_delete_dry_run_and_confirm(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            run_script(
                [
                    "scripts/append_event_log.py",
                    "--data-dir",
                    data_dir,
                    "--field",
                    "save_consent=true",
                    "--field",
                    "date=2026-05-06",
                    "--field",
                    "time=10:00:00",
                    "--field",
                    "mood_score=4",
                ]
            )
            dry = run_script(
                ["scripts/delete_log_entries.py", "--data-dir", data_dir, "--target", "event", "--date", "2026-05-06", "--dry-run"]
            )
            self.assertIn('"matched": 1', dry.stdout)
            with (Path(data_dir) / "event_log.csv").open(encoding="utf-8-sig") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 1)

            refused = run_script(
                ["scripts/delete_log_entries.py", "--data-dir", data_dir, "--target", "event", "--date", "2026-05-06"],
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0)

            run_script(
                [
                    "scripts/delete_log_entries.py",
                    "--data-dir",
                    data_dir,
                    "--target",
                    "event",
                    "--date",
                    "2026-05-06",
                    "--confirm",
                    "YES",
                ]
            )
            with (Path(data_dir) / "event_log.csv").open(encoding="utf-8-sig") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 0)

    def test_itinerary_scrubs_sensitive_terms_and_validator_uses_shared_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            itinerary = tmp_path / "itinerary.json"
            itinerary.write_text(
                json.dumps(
                    {
                        "route_name": "calm",
                        "city_area": "x",
                        "pois": [
                            {"name": "A", "type": "park", "stay": "10", "purpose": "焦虑 pause", "required": True},
                            {"name": "B", "type": "cafe", "stay": "10", "purpose": "call 13800138000", "required": False},
                        ],
                        "minimum_version": "one stop",
                        "retreat_point": "return",
                    }
                ),
                encoding="utf-8",
            )
            out_dir = tmp_path / "out"
            run_script(["scripts/export_roundtrip_itinerary.py", "--itinerary", str(itinerary), "--output-dir", str(out_dir)])
            copy_text = (out_dir / "copy.txt").read_text(encoding="utf-8")
            self.assertIn("[敏感信息已移除]", copy_text)
            self.assertIn("[敏感定位已移除]", copy_text)
            self.assertNotIn("13800138000", copy_text)

    def test_code_profile_hides_absolute_path_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            project = tmp_path / "project"
            project.mkdir()
            (project / "app.py").write_text("print('hi')\n", encoding="utf-8")
            data_dir = tmp_path / "data"
            run_script(
                [
                    "scripts/analyze_local_code_profile.py",
                    "--data-dir",
                    str(data_dir),
                    "--consent",
                    "true",
                    "--project",
                    f"demo={project}",
                ]
            )
            profile = json.loads((data_dir / "career_profile.json").read_text(encoding="utf-8"))
            evidence = profile["project_evidence"][0]
            self.assertEqual(evidence["alias"], "demo")
            self.assertNotIn("path", evidence)

    def test_csv_formula_values_are_escaped(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            run_script(
                [
                    "scripts/append_event_log.py",
                    "--data-dir",
                    data_dir,
                    "--field",
                    "save_consent=true",
                    "--field",
                    "main_trigger==HYPERLINK(\"https://example.invalid\")",
                ]
            )
            with (Path(data_dir) / "event_log.csv").open(encoding="utf-8-sig") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["main_trigger"], "'=HYPERLINK(\"https://example.invalid\")")

    def test_profile_store_writes_require_consent(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            refused = run_script(
                [
                    "scripts/manage_profile_data.py",
                    "--data-dir",
                    data_dir,
                    "--store",
                    "career",
                    "update",
                    "--set",
                    "current_role=Developer",
                ],
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("--consent true", refused.stderr)

            ok = run_script(
                [
                    "scripts/manage_profile_data.py",
                    "--data-dir",
                    data_dir,
                    "--store",
                    "career",
                    "update",
                    "--set",
                    "current_role=Developer",
                    "--consent",
                    "true",
                ]
            )
            self.assertIn('"status": "ok"', ok.stdout)

    def test_delete_rejects_invalid_date_range(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            invalid_date = run_script(
                [
                    "scripts/delete_log_entries.py",
                    "--data-dir",
                    data_dir,
                    "--target",
                    "event",
                    "--date",
                    "2026-99-99",
                    "--dry-run",
                ],
                check=False,
            )
            self.assertNotEqual(invalid_date.returncode, 0)

            inverted = run_script(
                [
                    "scripts/delete_log_entries.py",
                    "--data-dir",
                    data_dir,
                    "--target",
                    "event",
                    "--from-date",
                    "2026-05-10",
                    "--to-date",
                    "2026-05-09",
                    "--dry-run",
                ],
                check=False,
            )
            self.assertNotEqual(inverted.returncode, 0)


    def test_openclaw_local_store_and_designated_bot_require_consent(self) -> None:
        with tempfile.TemporaryDirectory() as data_dir:
            run_script(["scripts/init_local_data.py", "--data-dir", data_dir])
            openclaw_store = Path(data_dir) / "openclaw_dedicated_bots.json"
            self.assertTrue(openclaw_store.exists())

            refused = run_script(
                [
                    "scripts/configure_openclaw_bot.py",
                    "--data-dir",
                    data_dir,
                    "set",
                    "--bot-id",
                    "care-telegram",
                    "--channel",
                    "telegram",
                ],
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("--consent true", refused.stderr)

            ok = run_script(
                [
                    "scripts/configure_openclaw_bot.py",
                    "--data-dir",
                    data_dir,
                    "set",
                    "--bot-id",
                    "care-telegram",
                    "--channel",
                    "telegram",
                    "--display-name",
                    "Mental Care",
                    "--allowed-user-ids",
                    '["u123"]',
                    "--consent",
                    "true",
                ]
            )
            self.assertIn('"active_bot_id": "care-telegram"', ok.stdout)
            payload = json.loads(openclaw_store.read_text(encoding="utf-8"))
            self.assertEqual(payload["active_bot_id"], "care-telegram")
            self.assertTrue(payload["routing_policy"]["keep_records_local"])
            self.assertEqual(payload["bots"][0]["allowed_user_ids"], ["u123"])

    def test_openclaw_installer_creates_bridge_without_gateway_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            openclaw_home = tmp_path / "openclaw"
            data_dir = tmp_path / "data"
            run_command(
                [
                    "bash",
                    "scripts/install_openclaw.sh",
                    "--source-dir",
                    str(ROOT),
                    "--openclaw-home",
                    str(openclaw_home),
                    "--data-dir",
                    str(data_dir),
                    "--channel",
                    "discord",
                    "--bot-id",
                    "care-discord",
                    "--consent",
                    "true",
                ]
            )
            self.assertTrue((openclaw_home / "skills" / "mental-care-skill" / "SKILL.md").exists())
            self.assertTrue((openclaw_home / "agents" / "mental-care-skill.agent.md").exists())
            payload = json.loads((data_dir / "openclaw_dedicated_bots.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["active_bot_id"], "care-discord")

    def test_installer_creates_ide_bridge_files(self) -> None:
        with tempfile.TemporaryDirectory() as target:
            run_command(
                [
                    "bash",
                    "scripts/install.sh",
                    "--source-dir",
                    str(ROOT),
                    "--target",
                    target,
                    "--skip-codex",
                    "--ide",
                    "agents,vscode,cursor,trae",
                ]
            )
            target_path = Path(target)
            agents = target_path / "AGENTS.md"
            copilot = target_path / ".github" / "copilot-instructions.md"
            cursor = target_path / ".cursor" / "rules" / "mental-care-skill.mdc"
            trae = target_path / ".trae" / "rules" / "project_rules.md"

            for path in [agents, copilot, cursor, trae]:
                self.assertTrue(path.exists(), f"missing {path}")
                self.assertIn("mental-care-skill", path.read_text(encoding="utf-8"))

            self.assertIn("alwaysApply: false", cursor.read_text(encoding="utf-8"))

    def test_installer_is_idempotent_for_append_files(self) -> None:
        with tempfile.TemporaryDirectory() as target:
            args = [
                "bash",
                "scripts/install.sh",
                "--source-dir",
                str(ROOT),
                "--target",
                target,
                "--skip-codex",
                "--ide",
                "agents,vscode,trae",
            ]
            run_command(args)
            run_command(args)

            agents_text = (Path(target) / "AGENTS.md").read_text(encoding="utf-8")
            copilot_text = (Path(target) / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
            trae_text = (Path(target) / ".trae" / "rules" / "project_rules.md").read_text(encoding="utf-8")
            self.assertEqual(agents_text.count("mental-care-skill:start"), 1)
            self.assertEqual(copilot_text.count("mental-care-skill:start"), 1)
            self.assertEqual(trae_text.count("mental-care-skill:start"), 1)


if __name__ == "__main__":
    unittest.main()
