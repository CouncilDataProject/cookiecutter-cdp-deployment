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
            prog="check-repo-exists",
            description="Check if a GitHub repository exists.",
        )
        p.add_argument(
            "repo",
            type=str,
            help="The repo name. Ex. 'councildataproject/cookiecutter-cdp-deployment'"
        )
        p.parse_args(namespace=self)

def check_repo_exists(repo: str) -> None:
    # Request and get response
    response = requests.get(f"https://api.github.com/repos/{repo}")
    content = response.json()

    # Print out the boolean if the structure is consistent or not
    # name is only present if the repo exists
    # Otherwise the response looks like
    # {'message': 'Not Found', 'documentation_url': '...'}
    print("name" in content)


def main() -> None:
    try:
        args = Args()
        check_repo_exists(repo=args.repo)
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