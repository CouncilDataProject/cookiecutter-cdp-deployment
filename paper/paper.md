---
title: "Council Data Project: A Platform for Municipal Event Processing, Archival, and Discovery"
tags:
    - Python
    - JavaScript
    - open government
    - open data
    - open infrastructure
    - municipal governance
    - data archival
    - civic technology
    - natural language processing
authors:
    - name: Jackson Maxfield Brown
      orcid: 0000-0003-2564-0373
      affiliation: 1
    - name: To Huynh
      orcid: 0000-0002-9664-3662
      affiliation: 2
    - name: Isaac Na
      orcid: 0000-0002-0182-1615
      affiliation: 3
    - name: Brian Ledbetter
      affiliation: 1
    - name: Hawk Ticehurst
      affiliation: 1
    - name: Sara Liu
      affiliation: 4
    - name: Emily Giles
      affiliation: 4
    - name: Katlyn Greene
      affiliation: 4
    - name: Sung Cho
      affiliation: 4
    - name: Shak Ragoler
      affiliation: 4
    - name: Dhanya Pisharasyar
      affiliation: 4
    - name: Nicholas Weber
      orcid: 0000-0002-6008-3763
      affiliation: 1

affiliations:
    - name: University of Washington iSchool, University of Washington, Seattle
      index: 1
    - name: University of Washington, Seattle
      index: 2
    - name: McKelvey School of Engineering, Washington University, St. Louis
      index: 3
    - name: Independent Researcher
      index: 4

date: 26 September 2021
bibliography: paper.bib
---

# Summary

Council Data Project is a collection of tools for automated (or manual) processing, archival, and interactive discovery of municipal event data. It is designed to be an easily deployable infrastructure to allow for wide-spread dissemination and collective data generation. The data produced, archived, and made available through either web application or API, has wide ranging application from research on public policy, natural language processing and machine learning, information retrieval and discovery, and more. It is released under MIT license.

Council Data Project (CDP) tooling was originally designed for processing and archiving meetings of the Seattle City Council. Recent additions, have made it possible to archive, process, and compile data for any number of recorded events, either manually or in an automated fashion.

CDP tools are meant to act as a platform for research. As more CDP instances are deployed, the larger the pool of standardize event data there is to study. Specifically in cross-municipality studies for public policy, sociology, and more.

# Architecture

Council Data Project consists of three primary tools:

1. [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment): a Python [cookiecutter](https://cookiecutter.readthedocs.io/) template to assist users in fully deploying a new CDP instance.

2. [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): a Python package containing the database schema definition, transcript file format, our infrastructure definition, and our pipeline definitions.

3. [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): a TypeScript library containing all frontend components and our web application.

## Cookiecutter and the Produced Repository

`cookiecutter-cdp-deployment` will generate all necessary files for an entirely new CDP deployment as well as generate additional setup documentation for the user to follow to complete the instance deployment process.

Utilizing [GitHub Actions](https://github.com/features/actions) and [GitHub Pages](https://pages.github.com/), data processing and web hosting is entirely free. While the limited primary costs of CDP tools, are:

1. [Google Speech-to-Text](https://cloud.google.com/speech-to-text/) for transcript generation.
2. [Firebase Cloud Firestore](https://firebase.google.com/docs/firestore/) for feature and meta event data storage and access.
3. [Firebase Storage](https://firebase.google.com/docs/storage) for file storage and access.

CDP tools create an extremely cost effective solution while providing decentralized control over each deployment to the deployment maintainer(s) because each deployment is contained and managed with a unique GitHub repository.

![CDP Core Infrastructure Figure. Event Gather Pipeline: inputs, GitHub Action, Python Pipeline tasks, and storage. Event Index Pipeline: inputs, GitHub Action, Python n-gram generation, and storage. Web Application Building: inputs, GitHub Action, and GitHub Pages.\label{fig:core-infra}](./assets/cdp_core_infrastructure.png)

Additionally, because the CDP deployment repository is separate from the `cdp-backend` and `cdp-frontend` libraries, any time a data processing pipeline or the web application build jobs are initiated (any of the "Action Triggered" tasks in \autoref{fig:core-infra}), both libraries are updated with non-breaking changes prior to processing or build and deployment.

This allows for new additions and features to be automatically added to each deployment independent of updating all deployments. For example, we are currently developing a feature for automatic "meeting chapter" generation that would generate and attach timestamps to the meeting transcripts that correspond to the different portions of the meeting. When this feature is released to `cdp-backend`, it will become available to all CDP deployments during the next run of their event processing pipeline run (unless the maintainer has changed their repository from the default deployment configuration).

All combined, CDP tools allow for decentralized control over the management and deployment of each CDP instance while producing a standardized dataset.

## Data Access

Once data is processed, it is available through our interactive web application with plain text search for event discovery.

![CDP Web Application. Screenshot of a single events page, with navigation tabs for basic event details such as the minutes items, the entire transcript, and voting information. Additionally both the transcript search and the full transcript have links to jump to a specific sentence in the meeting](./assets/event-page-screenshot.png)

Additionally, as all of our database models are documented in the `cdp-backend` [library documentation](https://councildataproject.org/cdp-backend/database_schema.html), our backend tooling additionally allows for easy Python API access:

```python
from cdp_backend.database import models as db_models
from cdp_backend.pipeline.transcript_model import Transcript
import fireo
from gcsfs import GCSFileSystem
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client

# Connect to the database
fireo.connection(client=Client(
    project="cdp-test-deployment-435b5309",
    credentials=AnonymousCredentials()
))

# Read from the database
five_people = list(db_models.Person.collection.fetch(5))

# Connect to the file store
fs = GCSFileSystem(project="cdp-test-deployment-435b5309", token="anon")

# Read a transcript's details from the database
transcript_model = list(db_models.Transcript.collection.fetch(1))[0]

# Read the transcript directly from the file store
with fs.open(transcript_model.file_ref.uri, "r") as open_resource:
    transcript = Transcript.from_json(open_resource.read())

# OR download and store the transcript locally with `get`
fs.get(transcript_model.file_ref.uri, "local-transcript.json")
# Then read the transcript from your local machine
with open("local-transcript.json", "r") as open_resource:
    transcript = Transcript.from_json(open_resource.read())
```

## Future

# Acknowledgements

We wish to thank all DemocracyLab volunteers for the many hours of work and input on the many versions of CDP that have existed. From DemocracyLab, we would like to specifically thank Mark Frischmuth for the continued support and helpful discussions.

# References
