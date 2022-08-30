#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import sys
import traceback
from typing import Dict, List, Optional
from uuid import uuid4
from random import randint

from cdp_backend.utils.string_utils import clean_text

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)


###############################################################################

COUNCIL_DATA_PROJECT = "CouncilDataProject"

FORM_VALUES = "form_values"
COOKIECUTTER_OPTIONS = "cookiecutter_options"

MUNICIPALITY_NAME = "municipality"
GOVERNING_BODY_TYPE = "governing_body_type"
MUNICIPALITY_SLUG = "municipality_slug"
PYTHON_MUNICIPALITY_SLUG = "python_municipality_slug"
TARGET_MAINTAINER = "maintainer_or_org_full_name"
FIRESTORE_REGION = "firestore_region"

LEGISTAR_CLIENT_ID = "legistar_client_id"
IANA_CLIENT_TIMEZONE = "iana_timezone"
EVENT_GATHER_TIMEDELTA = "event_gather_timedelta_lookback_days"
EVENT_GATHER_CRON = "event_gather_cron"

FORM_FIELD_TO_HEADER = {
    MUNICIPALITY_NAME: "Municipality Name",
    GOVERNING_BODY_TYPE: "Governing Body Type",
    MUNICIPALITY_SLUG: "Municipality Slug",
    TARGET_MAINTAINER: "Maintainer GitHub Name",
    FIRESTORE_REGION: "Firestore Region",
    LEGISTAR_CLIENT_ID: "Legistar Client Id",
    IANA_CLIENT_TIMEZONE: "Municipality Timezone",
    EVENT_GATHER_TIMEDELTA: "Event Gather Timedelta Lookback Days",
    EVENT_GATHER_CRON: "Event Gather CRON",
}

NO_RESPONSE = "_No response_"

DEFAULT_FIRESTORE_REGION = "us-central"
DEFAULT_EVENT_GATHER_TIMEDELTA = 2

RANDOM_MINUTE = randint(0, 59)  # inclusive
RANDOM_HOUR = randint(0, 23)  # inclusive
OFFSET_HOUR = (RANDOM_HOUR + 12) % 24
DEFAULT_EVENT_GATHER_CRON = f"{RANDOM_MINUTE} {RANDOM_HOUR},{OFFSET_HOUR} * * *"

###############################################################################


class Args(argparse.Namespace):
    def __init__(self) -> None:
        self.__parse()

    def __parse(self) -> None:
        p = argparse.ArgumentParser(
            prog="parse-form",
            description="Parse the form values and generate cookiecutter options.",
        )
        p.add_argument(
            "issue_content_file",
            type=str,
            help="The path to the issue / form content file.",
        )
        p.parse_args(namespace=self)


def _get_field_value(lines: List[str], field_header: str) -> Optional[str]:
    # Get index of target then + 1 for the value
    header_index = lines.index(f"### {field_header}")
    value = lines[header_index + 1]
    return value if value != NO_RESPONSE else None


def parse_form(issue_content_file: str) -> Dict[str, Dict[str, str]]:
    # Open the content file, read, strip, and clean
    with open(issue_content_file, "r") as open_f:
        lines = open_f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]

    # Get all form values
    form_values: Dict[str, Optional[str]] = {}
    for field_name, form_header_string in FORM_FIELD_TO_HEADER.items():
        form_values[field_name] = _get_field_value(
            lines=lines,
            field_header=form_header_string,
        )
    log.info(form_values)

    # Get municipality slug
    if form_values[MUNICIPALITY_SLUG] is None:
        municipality_slug = (
            clean_text(form_values[MUNICIPALITY_NAME])
            .lower()
            .replace(
                " ",
                "-",
            )
        )
    else:
        municipality_slug = form_values[MUNICIPALITY_SLUG]

    # Get python municipality slug
    python_municipality_slug = municipality_slug.replace("-", "_")

    # Get default firestore region
    if form_values[FIRESTORE_REGION] is None:
        firestore_region = DEFAULT_FIRESTORE_REGION
    else:
        firestore_region = form_values[FIRESTORE_REGION]

    # Get event gather timedelta
    if form_values[EVENT_GATHER_TIMEDELTA] is None:
        event_gather_timedelta = DEFAULT_EVENT_GATHER_TIMEDELTA
    else:
        event_gather_timedelta = int(form_values[EVENT_GATHER_TIMEDELTA])

    # Get event gather cron
    if form_values[EVENT_GATHER_CRON] is None:
        event_gather_cron = DEFAULT_EVENT_GATHER_CRON
    else:
        event_gather_cron = form_values[EVENT_GATHER_CRON]

    all_options = {
        FORM_VALUES: form_values,
        COOKIECUTTER_OPTIONS: {
            MUNICIPALITY_NAME: form_values[MUNICIPALITY_NAME],
            IANA_CLIENT_TIMEZONE: form_values[IANA_CLIENT_TIMEZONE],
            GOVERNING_BODY_TYPE: form_values[GOVERNING_BODY_TYPE],
            MUNICIPALITY_SLUG: municipality_slug,
            PYTHON_MUNICIPALITY_SLUG: python_municipality_slug,
            "infrastructure_slug": f"cdp-{municipality_slug}-{str(uuid4())[:8]}",
            TARGET_MAINTAINER: form_values[TARGET_MAINTAINER],
            "hosting_github_username_or_org": COUNCIL_DATA_PROJECT,
            "hosting_github_repo_name": municipality_slug,
            "hosting_github_url": (
                f"https://github.com/{COUNCIL_DATA_PROJECT}/{municipality_slug}"
            ),
            "hosting_web_app_address": (
                f"https://councildataproject.github.io/{municipality_slug}"
            ),
            FIRESTORE_REGION: firestore_region,
            EVENT_GATHER_TIMEDELTA: event_gather_timedelta,
            EVENT_GATHER_CRON: event_gather_cron,
        },
    }

    # Dump to cookiecutter.json
    with open("planned-cookiecutter.json", "w") as open_f:
        open_f.write(json.dumps(all_options[COOKIECUTTER_OPTIONS], indent=4))

    return all_options


def main() -> None:
    try:
        args = Args()
        parse_form(
            issue_content_file=args.issue_content_file,
        )
    except Exception as e:
        log.error("=============================================")
        log.error("\n\n" + traceback.format_exc())
        log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
