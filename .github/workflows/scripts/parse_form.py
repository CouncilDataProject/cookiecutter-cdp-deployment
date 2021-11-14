#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import sys
import traceback
from typing import Dict, List, Optional
from uuid import uuid4

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
LEGISTAR_CLIENT_TIMEZONE = "legistar_client_timezone"

FORM_FIELD_TO_HEADER = {
    MUNICIPALITY_NAME: "Municipality Name",
    MUNICIPALITY_SLUG: "Municipality Slug",
    TARGET_MAINTAINER: "Maintainer GitHub Name",
    FIRESTORE_REGION: "Firestore Region",
    LEGISTAR_CLIENT_ID: "Legistar Client Id",
    LEGISTAR_CLIENT_TIMEZONE: "Municipality Timezone",
}

NO_RESPONSE = "_No response_"

DEFAULT_FIRESTORE_REGION = "us-central"

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

    all_options = {
        FORM_VALUES: form_values,
        COOKIECUTTER_OPTIONS: {
            MUNICIPALITY_NAME: form_values[MUNICIPALITY_NAME],
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
                f"https://councildataproject.org/{municipality_slug}"
            ),
            FIRESTORE_REGION: firestore_region,
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
