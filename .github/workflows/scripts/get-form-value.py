#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import traceback

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
            prog="get-form-value",
            description="Get a GitHub CDP New Instance form value.",
        )
        p.add_argument(
            "issue_content_file",
            type=str,
            help="The path to the issue / form content file."
        )
        p.add_argument(
            "form_target_header",
            type=str,
            help="Which header to get",
        )
        p.parse_args(namespace=self)

def get_form_value(issue_content_file: str, form_target_header: str) -> None:
    # Open the content file, read, strip, and clean
    with open(issue_content_file, "r") as open_f:
        lines = open_f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]

    # Get index of target then + 1 for the value
    header_index = lines.index(form_target_header)

    # The print is picked up by the GitHub Action runner
    print(lines[header_index + 1])


def main() -> None:
    try:
        args = Args()
        get_form_value(
            issue_content_file=args.issue_content_file,
            form_target_header=args.form_target_header,
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