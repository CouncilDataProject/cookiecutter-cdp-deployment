#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Validate the specified Google Cloud Project name is <= 30 chars
infrastructure_slug = '{{ cookiecutter.infrastructure_slug }}'

if len(infrastructure_slug) > 30:
    print(f"ERROR: {infrastructure_slug} is not a valid Google Cloud Project name! (>30 characters)")
    sys.exit(1)
