#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, timedelta
import json
import logging
import sys
import traceback

from cdp_backend.infrastructure.cdp_stack import GoverningBody
from cdp_scrapers.legistar_utils import LegistarScraper
from cdp_scrapers import instances
import requests

from parse_form import (
    COOKIECUTTER_OPTIONS,
    FORM_VALUES,
    MUNICIPALITY_SLUG,
    GOVERNING_BODY_TYPE,
    MUNICIPALITY_NAME,
    LEGISTAR_CLIENT_ID,
    LEGISTAR_CLIENT_TIMEZONE,
    PYTHON_MUNICIPALITY_SLUG,
    TARGET_MAINTAINER,
    COUNCIL_DATA_PROJECT,
    parse_form,
)

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################

GITHUB_USERS_RESOURCE = "users"
GITHUB_REPOSITORIES_RESOURCE = "repos"

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
    # Parse and get cookiecutter options
    form_values_and_cookiecutter_options = parse_form(
        issue_content_file=issue_content_file,
    )

    # Unpack form values
    form_values = form_values_and_cookiecutter_options[FORM_VALUES]

    # Unpack certain values
    municipality_slug = form_values_and_cookiecutter_options[COOKIECUTTER_OPTIONS][
        MUNICIPALITY_SLUG
    ]
    python_municipality_slug = form_values_and_cookiecutter_options[
        COOKIECUTTER_OPTIONS
    ][PYTHON_MUNICIPALITY_SLUG]

    # Governing body type in allowed
    governing_body_allowed_strings = [
        getattr(GoverningBody, attr) for attr in dir(GoverningBody) if "__" not in attr
    ]
    governing_body_type_allowed = (
        form_values[GOVERNING_BODY_TYPE] in governing_body_allowed_strings
    )

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

    # Test Legistar / existing scraper
    scraper_response = None
    scraper_options = None
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
        scraper_options = f"USE_FOUND_SCRAPER%{func_name}"
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
                for days_prior in [3, 7, 14, 28]:
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
                        scraper_options = (
                            f"USE_BASE_LEGISTAR"
                            f"%{form_values[LEGISTAR_CLIENT_ID]}"
                            f"%{form_values[LEGISTAR_CLIENT_TIMEZONE]}"
                        )
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

            except Exception as e:
                scraper_response = (
                    f"❌ Something went wrong during Legistar client data validation. "
                    f"A [cdp-scrapers]"
                    f"(https://github.com/"
                    f"{COUNCIL_DATA_PROJECT}/cdp-scrapers) maintainer "
                    f"will look into the logs for this bug. Sorry about this!"
                )
                log.error(e)
                log.error(traceback.format_exc())
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
    if governing_body_type_allowed:
        governing_body_response = "✅ Governing body type is an accepted value."
    else:
        governing_body_response = (
            f"❌ The provided governing body type is not an allowed value "
            f"({form_values[GOVERNING_BODY_TYPE]}). "
            f"Allowed values are: {governing_body_allowed_strings}."
        )
    maintainer_name = None
    if planned_maintainer_exists:
        maintainer_name = form_values[TARGET_MAINTAINER]
        maintainer_response = (
            f"✅ @{maintainer_name} " f"has been marked as the instance maintainer."
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
        repository_path = None
    else:
        repository_response = f"✅ **{repository_path}** is available."
        repository_ready = True

    # Construct "ready"
    if all(
        [
            scraper_ready,
            maintainer_ready,
            repository_ready,
            governing_body_type_allowed,
        ]
    ):
        ready_response = "#### ✅ All checks successful :tada:"
    else:
        ready_response = "#### ❌ Some checks failing"

    # Join all together
    comment_response = "\n".join(
        [
            governing_body_response,
            maintainer_response,
            repository_response,
            scraper_response,
            ready_response,
        ]
    )

    # Dump to file
    with open("form-validation-results.md", "w") as open_f:
        open_f.write(comment_response)

    # Save shorthand repo generation options to file
    # If any check failed, the value will be None / null
    with open("generation-options.json", "w") as open_f:
        json.dump(
            {
                "scraper_options": scraper_options,
                "maintainer_name": maintainer_name,
                "repository_path": repository_path,
            },
            open_f,
        )


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
