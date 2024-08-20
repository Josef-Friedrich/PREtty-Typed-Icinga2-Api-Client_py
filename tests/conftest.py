# https://docs.pytest.org/en/8.0.x/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Generator

import pytest


def __chdir(dest: Path) -> Generator[Path, Any, None]:
    """https://github.com/ar90n/pytest-chdir"""
    last_cwd = os.getcwd()
    os.chdir(dest)
    try:
        yield dest
    finally:
        os.chdir(last_cwd)


@pytest.fixture
def cwd_tmpdir(tmpdir: Path) -> Generator[Path, Any, None]:
    yield from __chdir(tmpdir)


@pytest.fixture
def cwd_test_path() -> Generator[Path, Any, None]:
    yield from __chdir(Path(__file__).parent)
