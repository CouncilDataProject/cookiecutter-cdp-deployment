from diagrams import Diagram, Cluster
from diagrams.firebase.develop import Firestore, Storage
from diagrams.gcp.ml import SpeechToText
from diagrams.k8s.compute import Cronjob
from diagrams.onprem.ci import GithubActions
from diagrams.k8s.podconfig import CM
from diagrams.onprem.compute import Server as Function
from diagrams.programming.flowchart import Or
from diagrams.onprem.vcs import Github

with Diagram("CDP Core Infrastructure", show=False):
    # Storage
    with Cluster("Firebase"):
        database = Firestore("Firestore")
        storage = Storage("Storage")

    with Cluster("Event Gather Pipeline"):
        # Inputs
        with Cluster("Triggers"):
            event_cron = Cronjob("Every 6 Hours")
            custom_json = CM("JSON")
            backfill = CM("Datetime Range")

            event_gather_triggers = [event_cron, custom_json, backfill]

        # Core Job
        event_gather_job = GithubActions("Action Triggered")

        # Processing
        with Cluster("Tasks"):
            # Functions
            get_events = Function("Get Events")
            thumbnails = Function("Generate Thumbnails")
            or_op = Or("Convert or Create")
            archive_event = Function("Archive")

            convert_transcript = Function("Convert Captions")
            create_transcript = SpeechToText("Speech-to-Text")
            
            convert_or_generate = [convert_transcript, create_transcript]

        event_gather_triggers >> event_gather_job
        or_op >> convert_or_generate
        event_gather_job >> get_events >> thumbnails >> or_op
        convert_or_generate >> archive_event
        thumbnails >> archive_event
        archive_event >> database
        archive_event >> storage

    with Cluster("Event Index Pipeline"):
        # Inputs
        with Cluster("Triggers"):
            index_cron = Cronjob("Every 2 Days")
            manual_index = CM("Manual")

            event_index_triggers = [index_cron, manual_index]

        # Core Job
        event_index_job = GithubActions("Action Triggered")

        # Processing
        with Cluster("Tasks"):
            unigrams = Function("Unigrams")
            bigrams = Function("Bigrams")
            trigrams = Function("Trigrams")

            unigrams_store = Function("Upload")
            bigrams_store = Function("Upload")
            trigrams_store = Function("Upload")

            unigrams >> unigrams_store
            bigrams >> bigrams_store
            trigrams >> trigrams_store

            index = [unigrams, bigrams, trigrams]
            stores = [unigrams_store, bigrams_store, trigrams_store]

        event_index_triggers >> event_index_job
        event_index_job >> index
        stores >> database

    with Cluster("Web Application"):
        # Inputs
        with Cluster("Triggers"):
            web_app_cron = Cronjob("Once a week")
            manual_web_build = CM("Manual")

            web_app_build_triggers = [web_app_cron, manual_web_build]

        # Core Job
        web_app_build_job = GithubActions("Action Triggered")
        web_app = Github("GitHub Pages")
    
        web_app_build_triggers >> web_app_build_job >> web_app

        database >> web_app
        storage >> web_app