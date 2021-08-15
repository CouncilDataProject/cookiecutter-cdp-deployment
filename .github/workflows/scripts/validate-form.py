#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import sys
import traceback
from typing import Dict, List, Optional

from cdp_backend.pipeline.event_index_pipeline import clean_text
import requests

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################

COUNCIL_DATA_PROJECT = "CouncilDataProject"

MUNICIPALITY_NAME = "municipality"
MUNICIPALITY_SLUG = "municipality_slug"
PYTHON_MUNICIPALITY_SLUG = "python_municipality_slug"
TARGET_MAINTAINER = "maintainer_or_org_full_name"
FIRESTORE_REGION = "firestore_region"

LEGISTAR_CLIENT_ID = "legistar_client_id"
LEGISTAR_CLIENT_TIMEZONE = "legistar_client_timezone"

FORM_FIELD_TO_HEADER = {
    MUNICIPALITY_NAME: "Municipality Name",
    MUNICIPALITY_SLUG: "(Optional) Municipality Slug",
    TARGET_MAINTAINER: "Maintainer GitHub Name",
    FIRESTORE_REGION: "(Optional) Firestore Region",
    LEGISTAR_CLIENT_ID: "(Optional) Legistar Client Id",
    LEGISTAR_CLIENT_TIMEZONE: "(Optional) Municipality Timezone",
}

GITHUB_USERS_RESOURCE = "users"
GITHUB_REPOSITORIES_RESOURCE = "repos"

NO_RESPONSE = "_No response_"

DEFAULT_FIRESTORE_REGION = "us-central1"

###############################################################################


class Args(argparse.Namespace):
    def __init__(self) -> None:
        self.__parse()

    def __parse(self) -> None:
        p = argparse.ArgumentParser(
            prog="validate-form",
            description="Validate the values provided in the CDP instance config form.",
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


def _check_github_resource_exists(resource: str, name: str) -> bool:
    # Request and get response
    response = requests.get(f"https://api.github.com/{resource}/{name}")
    content = response.json()

    # Return the boolean if the structure is consistent with successful query or not
    # name is only present if the resource exists
    # Otherwise the response looks like
    # {'message': 'Not Found', 'documentation_url': '...'}
    return "name" in content


def validate_form(issue_content_file: str) -> None:
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
            clean_text(form_values[MUNICIPALITY_NAME]).lower().replace(" ", "-")
        )
    else:
        municipality_slug = form_values[MUNICIPALITY_SLUG]

    # Get python municipality slug
    python_municipality_slug = municipality_slug.replace("-", "_")

    # Check planned maintainer exists
    planned_maintainer_exists = _check_github_resource_exists(
        resource=GITHUB_USERS_RESOURCE,
        name=form_values[TARGET_MAINTAINER],
    )

    # Get municipality name
    repository_path = f"{COUNCIL_DATA_PROJECT}/{municipality_slug}"
    planned_repository_exists = _check_github_resource_exists(
        resource=GITHUB_REPOSITORIES_RESOURCE, name=repository_path
    )

    # Get default firestore region
    if form_values[FIRESTORE_REGION] is None:
        firestore_region = DEFAULT_FIRESTORE_REGION
    else:
        firestore_region = form_values[FIRESTORE_REGION]

    # Dump to cookiecutter.json
    with open("planned-cookiecutter.json", "w") as open_f:
        open_f.write(
            json.dumps(
                {
                    MUNICIPALITY_NAME: form_values[MUNICIPALITY_NAME],
                    MUNICIPALITY_SLUG: municipality_slug,
                    PYTHON_MUNICIPALITY_SLUG: python_municipality_slug,
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
                indent=4,
            )
        )

    # TODO: legistar

    # Construct message content
    if planned_maintainer_exists:
        maintainer_response = (
            f":heavy_check_mark: @{form_values[TARGET_MAINTAINER]} "
            f"has been marked as the instance maintainer."
        )
    else:
        maintainer_response = (
            f":x: The planned instance maintainer: "
            f"'{form_values[TARGET_MAINTAINER]}', does not exist."
        )

    if planned_repository_exists:
        repository_response = (
            f":x: The planned repository already exists. "
            f"See: [{repository_path}](https://github.com/{repository_path})"
        )
    else:
        repository_response = f":heavy_check_mark: **{repository_path}** is available."

    # Join all together
    comment_response = "\n".join(
        [
            maintainer_response,
            repository_response,
        ]
    )

    # Dump to file
    with open("form-validation-results.md", "w") as open_f:
        open_f.write(comment_response)


def main() -> None:
    try:
        args = Args()
        validate_form(
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
