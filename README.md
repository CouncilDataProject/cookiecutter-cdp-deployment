# Cookiecutter CDP Deployment

[![Cookiecutter Check Status](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/workflows/Build%20Example%20Repo/badge.svg)](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/tree/example-build)

Cookiecutter template for new CDP deployments.

---

## CouncilDataProject

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

For more information about CouncilDataProject, please visit
[our website](https://councildataproject.github.io/).

## About

This repository is "cookiecutter template" for an entirely new 
CouncilDataProject (CDP) Instance. By following the steps defined in
the [Usage](#usage) section, you will be creating all the database, file storage,
processing resources, and more, that are ultimately needed to serve the
CDP web application.

See the current
[Seattle CDP Instance](https://councildataproject.github.io/seattle/#/).

### CDP Instance Features

-   Plain text search of past events and legislation<br>
    _(search for "missing middle housing" or "bike lanes")_
-   Filter and sort event and legislation search results<br>
    _(filter by date range, committee, etc.)_
-   Automatic timestamped-transcript generation<br>
    _(jump to a specific public comment or debate)_
-   Legislation and amendment tracking<br>
    _(check for amendment passage, upcoming meetings, etc.)_
-   Share event at timepoint<br>
    _(jump right to the point in the meeting you want to highlight)_
-   Full event minute details<br>
    _(view all documents and presentations related to each event)

_Note: Some features are dependent on how much data is provided during event gather.
More information available in our
[ingestion models documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html)._

## Usage

1. Create (or sign in to) a Google Cloud Platform (GCP) account.
   ([Google Cloud Console Home](https://console.cloud.google.com/))
   Google Cloud Platform is where all data and files will be stored, and some
   processing will be done using GCP resources.
   More details available in the [Google Cloud](#google-cloud) section.
2. Create (or re-use) a [billing account](https://console.cloud.google.com/billing)
   and attach it to your GCP account.
3. PLACEHOLDER: GET GOOGLE CLOUD CREDENTIALS
3. Create (or sign in to) a Pulumi account.
   ([Pulumi Account Sign-Up](https://app.pulumi.com/signup))
   Pulumi tracks and manages the state of your instances infrastructure
   (databases, file storage servers, credentials, etc.).
   More details available in the [Pulumi](#pulumi) section.
4. [Create a Pulumi Access Token](https://app.pulumi.com/account/tokens).
   Keep this token available. We will use it later.

### Cookiecutter Repo Generation

`Cookiecutter` is a Python package to generate templated projects.
This repository is a template for `cookiecutter` to generate a CDP deployment
repository which contains following:

-   A directory structure for your project
-   A directory for the web app to build and deploy from
-   A directory for infrastructure management
-   A directory for your Python event gather function and it's requirements
-   Continuous integration
    -   Preconfigured for web app to fully deploy
    -   Preconfigured to deploy all required CDP infrastructure
    -   Preconfigured to run CDP pipelines using GitHub Actions

To generate a new repository from this template, run:

```bash
pip install cookiecutter
cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment
```

_Note: This will only create the basic repository. You will still need to setup
Google Cloud and Pulumi accounts._

### Google Cloud

All of your deployments data and some data processing will be done using
Google Cloud Platform (GCP).

-   Your deployment's provided and generated data (meeting dates,
    committee names, councilmember details, etc) will live in
    [Firestore](https://cloud.google.com/firestore).
-   Your deployment's generated files (audio clips, transcripts, etc.)
    will live in [Filestore](https://cloud.google.com/filestore).
-   When provided a video without closed captions, the audio from the provided video
    will be processed using [Speech-to-Text](https://cloud.google.com/speech-to-text).

All of these resources will be set up for you using [Pulumi](#pulumi) but you will
need to make


**Free software: MIT license**
