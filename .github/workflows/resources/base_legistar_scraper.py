#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from cdp_backend.pipeline.ingestion_models import EventIngestionModel
from cdp_scrapers.legistar_utils import LegistarScraper

###############################################################################


def get_events(
    from_dt: datetime,
    to_dt: datetime,
    **kwargs,
) -> List[EventIngestionModel]:
    scraper = LegistarScraper(
        client="REPLACE_LEGISTAR_CLIENT",
        timezone="REPLACE_IANA_CLIENT_TZ",
    )

    return scraper.get_events(begin=from_dt, end=to_dt)
