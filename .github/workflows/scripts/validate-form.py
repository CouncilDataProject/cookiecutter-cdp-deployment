#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, timedelta
import json
import logging
import sys
import traceback
from typing import Dict, List, Optional

from cdp_backend.pipeline.event_index_pipeline import clean_text
from cdp_scrapers.legistar_utils import LegistarScraper
from cdp_scrapers import instances
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
    MUNICIPALITY_SLUG: "Municipality Slug",
    TARGET_MAINTAINER: "Maintainer GitHub Name",
    FIRESTORE_REGION: "Firestore Region",
    LEGISTAR_CLIENT_ID: "Legistar Client Id",
    LEGISTAR_CLIENT_TIMEZONE: "Municipality Timezone",
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
            description=(
                "Validate the values provided in the CDP instance configuration form."
            ),
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

    # Return the boolean if the structure is consistent with successful query
    # or not name is only present if the resource exists
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
                        f"https://github.com/"
                        f"{COUNCIL_DATA_PROJECT}/{municipality_slug}"
                    ),
                    "hosting_web_app_address": (
                        f"https://councildataproject.org/{municipality_slug}"
                    ),
                    FIRESTORE_REGION: firestore_region,
                },
                indent=4,
            )
        )

    # Test Legistar / existing scraper
    scraper_response = None
    try:
        func_name = f"get_{python_municipality_slug}_events"
        getattr(instances, func_name)

        scraper_response = (
            f"✅ An existing scraper for '{form_values[MUNICIPALITY_NAME]}' was found "
            f"in `cdp-scrapers` (`cdp_scrapers.instances.{func_name}`). "
            f"If this scraper was selected incorrectly, please update the "
            f"Municipality Slug field with more specificity "
            f"(i.e. 'seattle-wa' instead of 'seattle')."
        )
        scraper_ready = True
    except AttributeError:
        if (
            form_values[LEGISTAR_CLIENT_ID] is not None
            and form_values[LEGISTAR_CLIENT_TIMEZONE] is not None
        ):
            log.info("Attempting Legistar data retrieval")

            # Init temp scraper and run
            scraper = LegistarScraper(
                client=form_values[LEGISTAR_CLIENT_ID],
                timezone=form_values[LEGISTAR_CLIENT_TIMEZONE],
            )
            try:
                # Check that the provided client information
                # is even a Legistar municipality
                if not scraper.is_legistar_compatible:
                    scraper_response = (
                        f"❌ No public Legistar instance found for "
                        f"the provided client ({form_values[LEGISTAR_CLIENT_ID]}). "
                        f"If your municipality uses Legistar but you received this "
                        f"error, we recommended contacting your municipality clerk and "
                        f"asking about public Legistar API access, "
                        f"they may direct you to the IT department as well. "
                        f"If they do not respond to your requests, you will need to "
                        f"write a custom scraper to deploy your CDP instance."
                    )
                    scraper_ready = False
                log.info("Legistar client available")

                # If everything runs correctly, log success and show event
                # model in comment
                for days_prior in [7, 14, 28]:
                    log.info(f"Attempting minimum CDP data for {days_prior} days")
                    if scraper.check_for_cdp_min_ingestion(check_days=days_prior):
                        log.info("Legistar client has minimum data")
                        events = scraper.get_events(
                            begin=datetime.utcnow() - timedelta(days=days_prior),
                        )
                        single_event = events[0].to_dict()
                        event_as_json_str = json.dumps(single_event, indent=4)

                        scraper_response = (
                            f"✅ The municipality's Legistar instance "
                            f"contains the minimum required CDP event ingestion data.\n"
                            f"<summary>Retrieved Data</summary>\n"
                            f"<details>\n\n"  # Extra new line for proper rendering
                            f"```json\n"
                            f"{event_as_json_str}\n"
                            f"```"
                            f"</details>"
                        )
                        scraper_ready = True
                        break

                if scraper_response is None:
                    log.info(
                        "Legistar client missing minimum data, "
                        "attempting to simply pull data for logging."
                    )
                    # Check if _any_ data was returned
                    for days_prior in [7, 14, 28]:
                        log.info(
                            f"Attempting to pull Legistar data for "
                            f"previous {days_prior} days."
                        )
                        events = scraper.get_events(
                            begin=datetime.utcnow() - timedelta(days=days_prior),
                        )
                        if len(events) > 0:
                            log.info(
                                f"Received Legistar data for "
                                f"previous {days_prior} days."
                            )
                            single_event = events[0].to_dict()
                            event_as_json_str = json.dumps(single_event, indent=4)
                            scraper_response = (
                                f"❌ Your municipality uses Legistar but the minimum "
                                f"required data for CDP event ingestion wasn't found. "
                                f"A "
                                f"[cdp-scrapers]"
                                f"(https://github.com/"
                                f"{COUNCIL_DATA_PROJECT}/cdp-scrapers) "
                                f"maintainer will look into this issue however it is "
                                f"likely that you (@{form_values[TARGET_MAINTAINER]}) "
                                f"will need to write a custom scraper.\n"
                                f"<summary>Retrieved Data</summary>\n"
                                f"<details>\n\n"  # Extra new line for proper rendering
                                f"```json\n"
                                f"{event_as_json_str}\n"
                                f"```"
                                f"</details>"
                            )
                            scraper_ready = False
                            break

            # Catch no video path available
            # User will need to write a custom Legistar scraper
            except NotImplementedError:
                scraper_response = (
                    f":warning: Your municipality uses Legistar but is "
                    f"missing the video URLs for event recordings. "
                    f"We recommended writing a custom Legistar Scraper that inherits "
                    f"from our own [LegistarScraper]"
                    f"(https://councildataproject.org/cdp-scrapers/"
                    f"cdp_scrapers.html#cdp_scrapers.legistar_utils.LegistarScraper) "
                    f"to resolve the issue. "
                    f"Please see the "
                    f"[cdp-scrapers]"
                    f"(https://github.com/"
                    f"{COUNCIL_DATA_PROJECT}/cdp-scrapers) repository "
                    f"for more details. And please refer to the "
                    f"[SeattleScraper]"
                    f"(https://github.com/{COUNCIL_DATA_PROJECT}/cdp-scrapers"
                    f"/blob/main/cdp_scrapers/instances/seattle.py) "
                    f"for an example of a scraper that inherits from our "
                    f"base `LegistarScraper` to resolve this issue."
                )
                scraper_ready = False

            except Exception:
                scraper_response = (
                    f"❌ Something went wrong during Legistar client data validation. "
                    f"A [cdp-scrapers]"
                    f"(https://github.com/"
                    f"{COUNCIL_DATA_PROJECT}/cdp-scrapers) maintainer "
                    f"will look into the logs for this bug. Sorry about this!"
                )
                scraper_ready = False

    # Handle bad / mis-parametrized legistar info
    if scraper_response is None:
        if (
            form_values[LEGISTAR_CLIENT_ID] is not None
            and form_values[LEGISTAR_CLIENT_TIMEZONE] is None
        ):
            scraper_response = (
                "❌ You provided a Legistar Client Id but no Timezone. "
                "**Timezone is required** for Legistar scraping. "
                "Please edit your original submission to include this information."
            )
            scraper_ready = False
        else:
            scraper_response = (
                f"❌ **You didn't provide Legistar Client "
                f"information and no existing scraper was found in `cdp-scrapers`**. "
                f"Please either provide Legistar Client information and / or add a "
                f"custom scraper to "
                f"[cdp-scrapers]"
                f"(https://github.com/"
                f"{COUNCIL_DATA_PROJECT}/cdp-scrapers). "
                f"Please refer to our "
                f"[documentation for writing custom scrapers](TODO) "
                f"for more information. "
                f"Note, either a successful basic Legistar scraper run or the "
                f"addition of a custom scraper to `cdp-scrapers` is required before "
                f"moving on in the deployment process."
            )
            scraper_ready = False

    # Construct message content
    if planned_maintainer_exists:
        maintainer_response = (
            f"✅ @{form_values[TARGET_MAINTAINER]} "
            f"has been marked as the instance maintainer."
        )
        maintainer_ready = True
    else:
        maintainer_response = (
            f"❌ The planned instance maintainer: "
            f"'{form_values[TARGET_MAINTAINER]}', does not exist."
        )
        maintainer_ready = False

    if planned_repository_exists:
        repository_response = (
            f"❌ The planned repository already exists. "
            f"See: [{repository_path}](https://github.com/{repository_path})"
        )
        repository_ready = False
    else:
        repository_response = f"✅ **{repository_path}** is available."
        repository_ready = True

    # Construct "ready"
    if all([scraper_ready, maintainer_ready, repository_ready]):
        ready_response = "#### ✅ All checks successful :tada:"
    else:
        ready_response = "#### ❌ Some checks failing"

    # Join all together
    comment_response = "\n".join(
        [
            maintainer_response,
            repository_response,
            scraper_response,
            ready_response,
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
