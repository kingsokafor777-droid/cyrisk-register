"""Local CLI for deterministic Cyrisk Register signal evaluation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from cyrisk_register.engine import evaluate
from cyrisk_register.models import RegisterRequest


def main(argv: Sequence[str] | None = None) -> int:
    """Evaluate one local register request at a caller-supplied ISO date."""
    parser = argparse.ArgumentParser(prog="cyrisk-register")
    parser.add_argument("command", choices=("evaluate",))
    parser.add_argument("request", type=Path)
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    args = parser.parse_args(argv)
    try:
        request = RegisterRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
        result = evaluate(request, args.as_of)
    except (OSError, ValidationError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(result.model_dump_json())
    return 0
