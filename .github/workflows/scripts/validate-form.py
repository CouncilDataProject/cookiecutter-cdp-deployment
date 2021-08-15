#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import traceback
from typing import Dict, List, Optional

import requests

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################

TARGET_MAINTAINER = "target_maintainer"
TARGET_REPOSITORY = "target_respository"
LEGISTAR_CLIENT_ID = "legistar_client_id"
LEGISTAR_CLIENT_TIMEZONE = "legistar_client_timezone"

FORM_FIELD_TO_HEADER = {
    TARGET_MAINTAINER: "Maintainer GitHub Name",
    TARGET_REPOSITORY: "Repository Name",
    LEGISTAR_CLIENT_ID: "Legistar Client Id",
    LEGISTAR_CLIENT_TIMEZONE: "Municipality Timezone",
}

GITHUB_USERS_RESOURCE = "users"
GITHUB_REPOSITORIES_RESOURCE = "repos"

###############################################################################

TARGET_MAINTAINER_EXISTS_MESSAGE = """
- [x] ✅ @{maintainer_name} has been marked as the planned instance maintainer.
""".strip()

TARGET_MAINTAINER_DOES_NOT_EXIST_MESSAGE = """
- [ ] ❌ The planned instance maintainer: '{maintainer_name}', does not exist.
""".strip()

TARGET_REPOSITORY_EXISTS_MESSAGE = """
- [ ] ❌ The planned repository already exists. See: [{repository_name}](https://github.com/{repository_name})
""".strip()

TARGET_REPOSITORY_DOES_NOT_EXIST_MESSAGE = """
- [x] ✅ **{repository_name}** is available.
""".strip()

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
            help="The path to the issue / form content file."
        )
        p.parse_args(namespace=self)


def _get_field_value(lines: List[str], field_header: str) -> Optional[str]:
    # Get index of target then + 1 for the value
    header_index = lines.index(f"### {field_header}")
    value = lines[header_index + 1]
    return value if value is not "_No Response_" else None


def _check_github_resource_exists(resource: str, name: str) -> bool:
    # Request and get response
    response = requests.get(f"https://api.github.com/{resource}/{name}")
    content = response.json()
    log.info(content)

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

    # Check planned maintainer exists
    planned_maintainer_exists = _check_github_resource_exists(
        resource=GITHUB_USERS_RESOURCE,
        name=form_values[TARGET_MAINTAINER],
    )

    # Check planned repository exists
    repository_name = f"councildataproject/{form_values[TARGET_REPOSITORY]}"
    planned_repository_exists = _check_github_resource_exists(
        resource=GITHUB_REPOSITORIES_RESOURCE,
        name=repository_name
    )

    # TODO: legistar

    # Construct message content
    if planned_maintainer_exists:
        maintainer_response += TARGET_MAINTAINER_EXISTS_MESSAGE.format(
            maintainer_name=form_values[TARGET_MAINTAINER],
        )
    else:
        maintainer_response += TARGET_MAINTAINER_DOES_NOT_EXIST_MESSAGE.format(
            maintainer_name=form_values[TARGET_MAINTAINER],
        )
    
    if planned_repository_exists:
        repository_response += TARGET_REPOSITORY_EXISTS_MESSAGE.format(
            repository_name=repository_name,
        )
    else:
        repository_response += TARGET_MAINTAINER_DOES_NOT_EXIST_MESSAGE.format(
            repository_name=repository_name,
        )

    # Join all together
    comment_response = "\n".join([
        maintainer_response,
        repository_response,
    ])

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