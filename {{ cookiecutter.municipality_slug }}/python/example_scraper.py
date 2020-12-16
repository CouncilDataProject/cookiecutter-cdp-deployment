#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from datetime import datetime
from typing import List

from cdp_backend.pipeline.ingestion_models import (
    Body,
    EventIngestionModel,
    EventMinutesItem,
    Matter,
    MinutesItem,
    Person,
    Role,
    Seat,
    Session,
    SupportingFile,
    Vote,
)

###############################################################################


def get_example_events(
    n: int = 10, is_minimal: bool = False
) -> List[EventIngestionModel]:
    return [_get_example_event(is_minimal) for _ in range(n)]


###############################################################################


FAKE_COUNCIL_SEAT_NUM = 10


def _get_example_event(is_minimal: bool) -> EventIngestionModel:
    "Create a fake example event data"
    # Create a body for the event
    body = Body(
        name=f"Example Committee {random.randint(1, 100)}",
        description="Example Description",
    )
    # Create sessions for the event
    sessions = [
        Session(
            session_datetime=datetime.utcnow(),
            video_uri="https://youtu.be/UjieH-NrOe8",
        )
        for _ in range(random.randint(1, 3))
    ]
    event_minutes_items = None
    # Create event minutes items for the event
    if not is_minimal:
        # Get a number of event minutes items
        event_minutes_items_num = random.randint(5, 15)
        # Get a number of sponsors for each event minutes item
        sponsors_nums = random.choices(range(1, 4), k=event_minutes_items_num)
        # Specify the seat position for each sponsor
        sponsors_seats = [
            random.sample(range(1, FAKE_COUNCIL_SEAT_NUM + 1), sponsors_num)
            for sponsors_num in sponsors_nums
        ]
        # Create a list of event minutes item
        event_minutes_items = [
            EventMinutesItem(
                minutes_item=MinutesItem(
                    name=f"Example Minutes Item {random.randint(1, 100)}",
                    description="Example Description",
                ),
                matter=Matter(
                    name=f"Example Matter {random.randint(1, 100)}",
                    matter_type=f"Example Matter Type {random.randint(1, 5)}",
                    title="Example Matter Title",
                    sponsors=[
                        _get_example_person(seat_num) for seat_num in sponsors_seats[i]
                    ],
                ),
                supporting_files=[
                    SupportingFile(
                        name=f"Example Supporting File Name {file_num}",
                        uri="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    )
                    for file_num in range(1, random.randint(1, 5) + 1)
                ],
                decision=f"Example Decision {random.randint(1, 5)}",
                votes=[
                    Vote(
                        person=_get_example_person(seat_num),
                        decision=f"Example Decision {random.randint(1, 5)}",
                    )
                    for seat_num in range(1, FAKE_COUNCIL_SEAT_NUM + 1)
                ],
            )
            for i in range(event_minutes_items_num)
        ]
        # Insert a non-matter event minutes item
        event_minutes_items.insert(
            0,
            EventMinutesItem(
                minutes_item=MinutesItem(
                    name="Example Minutes Item", description="Example Description"
                )
            ),
        )
    return EventIngestionModel(
        body=body,
        sessions=sessions,
        event_minutes_items=event_minutes_items,
        agenda_uri="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        minutes_uri="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    )


def _get_example_person(seat_num: int) -> Person:
    "Create a fake example person"
    return Person(
        name=f"Example Person {seat_num}",
        email="person@example.com",
        phone="123-456-7890",
        website="www.example.com",
        picture_uri="https://councildataproject.github.io/imgs/public-speaker-light-purple.svg",
        seat=Seat(
            name=f"Example Seat Position {seat_num}",
            electoral_area=f"Example Electoral Area {seat_num}",
            electoral_type=f"Example Electoral Type {1 if seat_num <= FAKE_COUNCIL_SEAT_NUM / 2 else 2 }",
            image_uri="https://councildataproject.github.io/imgs/seattle.jpg",
        ),
        roles=[
            Role(title="Councilmember", body=Body(name="Example Committee")),
            Role(title="Chair", body=Body(name=f"Example Committee {seat_num}")),
        ],
    )
