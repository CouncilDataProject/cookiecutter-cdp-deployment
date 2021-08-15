#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import traceback

import requests

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################


class Args(argparse.Namespace):
    def __init__(self) -> None:
        self.__parse()

    def __parse(self) -> None:
        p = argparse.ArgumentParser(
            prog="check-github-resource-exists",
            description="Check if a GitHub resource (repo, user, org) exists.",
        )
        p.add_argument(
            "resource",
            type=str,
            help=(
                "The resource target. Ex. 'repos', 'users', 'organizations'"
            )
        )
        p.add_argument(
            "name",
            type=str,
            help=(
                "The resource name. "
                "Repo Ex. 'councildataproject/cookiecutter-cdp-deployment' "
                "User Ex. 'JacksonMaxfield'"
            )
        )
        p.parse_args(namespace=self)

def check_repo_exists(resource: str, name: str) -> None:
    # Request and get response
    response = requests.get(f"https://api.github.com/{resource}/{name}")
    content = response.json()

    # Print out the boolean if the structure is consistent or not
    # name is only present if the repo exists
    # Otherwise the response looks like
    # {'message': 'Not Found', 'documentation_url': '...'}
    print("name" in content)


def main() -> None:
    try:
        args = Args()
        check_repo_exists(resource=args.resource, name=args.name)
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