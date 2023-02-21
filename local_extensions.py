#!/usr/bin/env python

import random

from jinja2.ext import Extension

###############################################################################


class RandomIntegerExtension(Extension):
    """
    Enables the `random_integer` function for use in jinja injection.

    Example
    -------
    Creating a CRON string which runs at a random time each day.

    {
        "cron": "{{ random_integer(0, 59) }} {{ random_integer(0, 23) }} * * *"
    } 
    """
    def __init__(self, environment):
        super().__init__(environment)

        def random_integer(min: int, max: int) -> int:
            return random.randint(min, max)

        environment.globals.update(random_integer=random_integer)