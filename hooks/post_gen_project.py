#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


class AnsiColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


deployment_dir = Path(".").resolve()

print()
print(
    f"🎊 Success! Generated CDP Instance repo at {AnsiColors.OKGREEN}{deployment_dir}{AnsiColors.ENDC}."
)
print()
print(
    "To finish CDP Instance initialization, follow the instructions in SETUP/README.md."
)
print()
