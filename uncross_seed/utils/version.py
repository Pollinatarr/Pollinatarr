#!/usr/bin/python3

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def get_version() -> str:
    version = "Unknown"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")) as handle:
        for line in handle.readlines():
            line = line.strip()
            if len(line) > 0:
                version = line
                break
    return version
