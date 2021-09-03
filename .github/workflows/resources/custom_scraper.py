#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from cdp_backend.pipeline.ingestion_models import EventIngestionModel
from cdp_scrapers.instances import REPLACE_CUSTOM_SCRAPER

###############################################################################


def get_events(
    from_dt: datetime,
    to_dt: datetime,
    **kwargs,
) -> List[EventIngestionModel]:
    return REPLACE_CUSTOM_SCRAPER(from_dt=from_dt, to_dt=to_dt, **kwargs)
