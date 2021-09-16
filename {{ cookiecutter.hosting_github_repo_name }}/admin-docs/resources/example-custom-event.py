from datetime import datetime

from cdp_backend.pipeline import ingestion_models

# Define your event
event = ingestion_models.EventIngestionModel(
    body=ingestion_models.Body(name="2021 Mayoral Debates"),
    sessions=[
        ingestion_models.Session(
            video_uri="https://video.seattle.gov/media/council/brief_091321_2012171V.mp4",
            session_datetime=datetime(2021, 9, 13),
            session_index=0,
        ),
    ],
)

# Print out the JSON string in it's full form
print(repr(event.to_json()))
