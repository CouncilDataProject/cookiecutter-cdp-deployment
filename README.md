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
    _(view all documents and presentations related to each event)_

See the current
[Seattle CDP Instance](https://councildataproject.github.io/seattle/#/)
for a live example.

_Note: Some features are dependent on how much data is provided during event gather.
More information available in our
[ingestion models documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html)._

## Usage

Install `cookiecutter` and use this template.<br>
In a terminal with Python 3.5+ installed:

```bash
pip install cookiecutter
cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment
```

Following the prompts in the terminal and fill in the details of the repository.
At the end of the process a new directory will have been created with
further instructions and all required files to set up your new deployment.

Follow the next steps in the generated repository's "Initial Repo Setup" section
of the created README.md file.

For more details and examples on each parameter of the cookiecutter, see
[Cookiecutter Parameters](#cookiecutter-parameters)

For more details on what is created from using this template, see
[Cookiecutter Repo Generation](#cookiecutter-repo-generation)

### Cookiecutter Parameters

| Parameter                      | Description                                                                                                                | Example 1                             | Example 2                                |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ---------------------------------------- |
| municipality                   | The name of the municipality (town, city, county, etc.) that this CDP Instance will store data for.                        | Seattle                               | King County                              |
| municipality_slug              | The name of the municipality cleaned for use in infrastructure and certain parts of repository naming.                     | seattle                               | king-county                              |
| python_municipality_slug       | The name of the municipality cleaned for use in specifically Python parts of the application.                              | seattle                               | king_county                              |
| maintainer_or_org_full_name    | The full name of the primary maintainer or organization that will be managing this instance deployment.                    | Jackson Maxfield Brown                | CouncilDataProject                       |
| hosting_github_username_or_org | The GitHub username or organization that will host this instance's repository. (Used in the web application's domain name) | JacksonMaxfield                       | CouncilDataProject                       |
| hosting_github_reponame        | A specific name to give to the repository. (Used in the web application's full address)                                    | cdp-seattle                           | king-county                              |
| hosting_github_url             | From the provided information, the expected URL of the web application.                                                    | jacksonmaxfield.github.io/cdp-seattle | councildataproject.github.io/king-county |

### Things to Know

Much of CouncilDataProject processing and resource management can be handled for
free and purely on GitHub. However we do rely on a select few of resources outside
of GitHub.

The only service that will require a billing account to management payment for
resources used, is [Google Cloud](#google-cloud).
Google Cloud will manage all databases, file storage, and (if needed)
[speech-to-text](#speech-to-text) for transcription. You can see more about the
average monthly of running a CDP instance in our [cost](#cost) section.

[Pulumi](#pulumi) is a service to management and track infrastructure deployment state.
For those familiar with [Terraform](https://www.terraform.io/), the two are quite
similar. Pulumi's purpose is to ensure that we can move from infrastructure
upgrade to infrastructure upgrade without breaking anything (and skipping things
that don't need to be done).

For more details see [Cookiecutter Repo Creation](#cookiecutter-repo-generation).
_After creating the repo, the following steps will have_
_instructions and links specific to your deployment in the generated README._

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

To generate a new repository from this template,
in a terminal with Python 3.5+ installed, run:

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

## Cost

CDP was created and maintained by a group of people working on it in their free time.
We didn't want to pay extreme amounts of money so why should you?

So to that end, we try to make CDP as low cost as possible.
Many of the current features are entirely free as long as the repo is open source:

-   Event Processing (GitHub Actions)
-   Event and Legislation Indexing (GitHub Actions)
-   Web Hosting (GitHub Pages)
-   Infrastructure State Management (Pulumi)

The backend resources and processing are the only real costs and depend on usage.
The more users that use your web application, the more the database and file storage
costs. The CDP-Seattle monthly averages below are the averages for the most utilized
months of it's existance so take these as close to upper-bounds.

-   [Cloud Firestore Pricing](https://firebase.google.com/pricing/)
    _CDP-Seattle monthly average: ~$8.00_
-   [Google Storage Pricing](https://cloud.google.com/storage/pricing#price-tables)
    _CDP-Seattle monthly average: ~$3.00_
-   [Google Speech-to-Text Pricing](https://cloud.google.com/speech-to-text/pricing)
    _CDP-Seattle monthly average: ~$22.00_

**Total Average Monthly Cost**: $33.00

### Speech-to-Text

You may not need to use speech-to-text! In the case your municipalicity provides closed
caption files in a format we support parsing and cleaning, we can use those files
instead of using speech-to-text. When using closed caption files for transcription
generation. CDP-Seattle speech-to-text costs dropped to ~$2.00 / month because an
occasional meeting didn't have closed captions. You can attach a
[`closed_caption_uri`](https://councildataproject.github.io/cdp-backend/cdp_backend.pipeline.html#cdp_backend.pipeline.ingestion_models.Session)
to the `Session` object during event ingestion.

With speech-to-text cost removed, total average monthly cost for CDP-Seattle is ~$11.00.

### Future Processing Features

As we add more features to CDP that require additional processing or resources we will
continue to try to minimize their costs wherever possible. Further, if a feature is
optional, we will create a flag that maintainers can set to include or exclude the
additional processing or resource usage.

**Free software: MIT license**
