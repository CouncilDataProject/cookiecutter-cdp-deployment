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
    - name: Independent Contributor
      index: 4

date: 26 September 2021
bibliography: paper.bib
---

# Summary

Council Data Project is a collection of tools for automated (or manual) processing and archival, and interactive discovery, of municipal event data. It is designed to be an easily deployable infrastructure to allow for wide-spread dissemination and collective data generation. The data produced, archived, and made available through either web application or API, has wide ranging applications reaching from research on public policy, natural language processing and machine learning, information retrieval and discovery, and more. All libraries developed as a part of Council Data Project are released under MIT license.

Council Data Project (CDP) tooling was originally designed for processing and archiving meetings of the Seattle City Council. Recent additions however have made it possible to archive, process, and compile data for any number of recorded events, either manually or in an automated fashion.

CDP tools are meant to act both as a platform for accessible information but additionally as a platform for research. As more CDP instances are deployed, the larger the pool of standardized event data there is to study. Specifically, in scaling CDP instances to many deployments, scientists can test their models against multiple municipalities to see how well their model generalizes or study how different municipalities react to similar policy discussions.

# Architecture

Council Data Project consists of three primary tools:

1. [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment): a Python [cookiecutter](https://cookiecutter.readthedocs.io/) template to assist users in fully deploying a new CDP instance.

2. [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): a Python package containing the database schema definition, the transcript file format, our infrastructure specification, and our processing pipeline implementations.

3. [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): a TypeScript library containing all frontend components and our compiled web application.

## Cookiecutter and the Produced Repository

`cookiecutter-cdp-deployment` will generate all necessary files for an entirely new CDP deployment as well as additional setup documentation for the user to follow to fully complete the instance deployment process.

Utilizing [GitHub Actions](https://github.com/features/actions) and [GitHub Pages](https://pages.github.com/), data processing and web hosting are entirely free as long as the user sets their instances GitHub repository visibility to public. While the limited primary costs of CDP tools are:

1. [Google Speech-to-Text](https://cloud.google.com/speech-to-text/) for transcript generation.
2. [Firebase Cloud Firestore](https://firebase.google.com/docs/firestore/) for event metadata storage and access.
3. [Firebase Storage](https://firebase.google.com/docs/storage) for file storage and access.

Because each CDP deployment is contained and managed as a unique GitHub repository, CDP tools create an extremely cost effective solution while providing decentralized control over each deployment to the deployment maintainer(s).

![CDP Core Infrastructure Figure. Event Gather Pipeline: inputs, GitHub Action, Python Pipeline tasks, and storage. Event Index Pipeline: inputs, GitHub Action, Python n-gram generation, and storage. Web Application Building: inputs, GitHub Action, and GitHub Pages.\label{fig:core-infra}](./assets/cdp_core_infrastructure.png)

Additionally, because the produced CDP deployment repository is separate from the `cdp-backend` and `cdp-frontend` libraries, any time the data processing pipeline or the web application build jobs are initiated (any of the "Action Triggered" tasks in \autoref{fig:core-infra}), both libraries are updated with non-breaking changes prior to processing or build and deployment.

This allows for new additions and features to be automatically added to each deployment independent of updating all deployments. For example, we are currently developing a feature for automatic topic segmentation of meetings which, when implemented, will attach timestamps to the meeting transcripts that correspond to the different agenda items of the meeting. When this feature is released to `cdp-backend`, it will become available to all CDP deployments during the next run of their event processing pipeline (unless the maintainer has changed their repository from the default deployment configuration).

Further, because our core tooling libraries (`cdp-backend` and `cdp-frontend`) are open-source and separate from any individual deployment, any time an individual contributes a new feature or fixes a bug, they are inherently adding that feature or fixing that bug for all CDP instances.

All combined, CDP tools allow for decentralized control over the management and deployment of each CDP instance while producing a standardized open-access dataset for both research and for municipal transparency and accessiblity.

## Data Access

Once data is processed by a CDP instance, it is available through that instance's interactive web application.

![CDP Web Application. Screenshot of a single event's page. Navigation tabs for basic event details such as the minutes items, the entire transcript, and voting information. Additionally both the transcript search and the full transcript have links to jump to a specific sentence in the meeting.](./assets/event-page-screenshot.png)
This example event page can be found on our integration test instance: https://councildataproject.org/test-deployment/#/events/2b8d08eeea1a

For users who want programmatic access, each instance's repository README includes a programmatic quickstart guide and our database schema is autogenerated and stored in our `cdp-backend` [documentation](https://councildataproject.org/cdp-backend/database_schema.html).

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

## Research Use Cases

The following sections detail a few use cases for CDP in various research areas.

### Data Archival

**TODO: nic section**

### Misinformation

While there has been incredible growth in the study of misinformation, many studies primarily build their work off of social media datasets (Twitter, Facebook, etc.).
What we don't yet know is how misinformation, public discourse, and public sentiment shared on social media is later brought into council meetings in which there is active policy deliberation. In studying the dynamics of misinformation in policy deliberation and enactment, we can begin to understand how much of policy is decided upon using misinformation as the policy basis, how that policy is supported or not from the public, and how similar policy proposals in different municipalities (or levels of government) are discussed and either enacted or rejected.

We believe this is a crucial next step in misinformation research. Not only studying the spread of misinformation but additionally studying where, when, and how misinformation is used in policy creation. Both, how misinformation influences policy makers, and, how policy makers cite misinformation as fact to further their policy goals.

### Human-Computer Interaction

At the date of writing, we are currently still living with the COVID-19 pandemic. As we have all had to shift how and where we work, so have municipal governments. And in this shift of the municipal council, a shift was required of the public, from providing public testimony in-person to (in many cases - depending on the municipal council) completely remote. To handle this shift, many municipal councils began using information and communication technologies (ICTs) to conduct both their own deliberation and additionally their public comment periods.

While many councils are actively reverting back to in-person, or switching to hybrid models of deliberation and public comment, CDP tooling provides a unique affordance to study the effects that the deployment and utilization that these ICTs had, and continue to have, on the policy making process. In studying how the usage of information technology affected and still affects council meetings, we aim to provide insight and advice to councils on their deployment of ICTs in the future.

A specific example of a research question that we wish to pursue and answer utilizing CDP tooling is: "How does ICT utilization in the municipal council meeting process affect the composition of public commenter distribution in regards to age, gender, race, political ideology, and more? How do the various configurations of ICT utilization (fully in-person, fully remote, hybrid, etc.) affect these distributions? What methods and tools can municipalities use to ensure their council meetings are accessibile and inclusive to all who wish to participate and what methods and tools can municipalities use to actively seek out input from historically marginalized populations?"

### Catch-All

As a final note, we would like to point out that while we heavily focus on political information and data, CDP tooling can reasonably be used for any sort of "structured meeting" content. The team behind CDP for example, uses our own tools as a method for archiving our team meetings. In this way, while many of the above research use cases focus on political data as the primary point of research, CDP as a whole can be applied to many different research areas.

CDP, in a general sense, can be utilized as a method for producing a standardized dataset for any "structured meeting" content. And because of this general purpose nature, while we tend to focus on municipal information accessibility questions, these aren't the only research areas that data processed and archived by CDP can be utilized under.

## Future Work

While we have deployed CDP instances for Seattle City Council and King County Council, and we plan on deploying more instances of CDP, we recognize, that as we believe in the [Right to Replicate](https://2i2c.org/right-to-replicate/) and we have actively taken steps to make the deployment process as easy as possible with or without our support, other individuals, labs, and organizations may deploy new CDP instances completely on their own.

To make multi-municipality / multi-deployment comparitive research as easy as possible, we plan on developing a multi-instance API for search and analysis. For example, a researcher could use the planned API to construct a dataset of all transcripts from CDP instances that contain a query they are interested in and additionally provide parameters for what is returned as a result (programmatic return, downloadable archive format, etc.). This specific feature has already started to be planned out and discussion can be found here: https://github.com/CouncilDataProject/cdp-roadmap/issues/3

For a full list of potential future work specifically relating to our infrastructure and tool, please see our [public roadmap](https://github.com/CouncilDataProject/cdp-roadmap/issues).

# Acknowledgements

We wish to thank all DemocracyLab volunteers for the many hours of work and input on the many versions of CDP that have existed. From DemocracyLab, we would like to specifically thank Mark Frischmuth for the continued support and helpful discussions.

# References
