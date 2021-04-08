#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

deployment_dir = Path(".").resolve()

print("-" * 80)
print(f"Created new directory: {deployment_dir}")
print(
    "To finish new CDP Instance creation, move into the "
    "created directory and follow the instructions in the "
    "'Initial Repo Setup' section of the README.md file."
)
