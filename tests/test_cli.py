from __future__ import annotations

import json
from pathlib import Path

import pytest

from cyrisk_register.cli import main

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_register_request.json"


def test_cli_emits_signal_report(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["evaluate", str(FIXTURE), "--as-of", "2099-01-01"]) == 0
    assert json.loads(capsys.readouterr().out)["central_above_tolerance"] is True


def test_cli_rejects_invalid_request(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text("not-json", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["evaluate", str(invalid), "--as-of", "2099-01-01"])
