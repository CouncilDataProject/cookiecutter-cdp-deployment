# cookiecutter-cdp-deployment

[![Cookiecutter Check Status](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/workflows/Build%20Example%20Repo/badge.svg)](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/tree/example-build)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.03904/status.svg)](https://doi.org/10.21105/joss.03904)

Cookiecutter template for creating new Council Data Project deployments.

---

## Council Data Project

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools
they need to stay informed and hold their Council Members accountable.

For more information about Council Data Project, please visit
[our website](https://councildataproject.org/).

## About

This repository is a "cookiecutter template" for an entirely new
Council Data Project (CDP) Instance. By following the steps defined in
the [Usage](#usage) section, our tools will create and manage all the database,
file storage, and processing infrastructure needed to serve the CDP web application.

While our tools will setup and manage all processing and storage infrastructure, you
(or your team) must provide and maintain the custom Python code to gather event
information and handle billing for the costs of the deployment.

For more information about costs and billing, see [Cost](#cost).

### CDP Instance Features

-   Plain text search of past events and meeting items<br>
    _(search for "missing middle housing" or "bike lanes")_
-   Filter and sort event and meeting item search results<br>
    _(filter by date range, committee, etc.)_
-   Automatic timestamped-transcript generation<br>
    _(jump right to a specific public comment or debate)_
-   Meeting item and amendment tracking<br>
    _(check for amendment passage, upcoming meetings, etc.)_
-   Share event at timepoint<br>
    _(jump right to the point in the meeting you want to share)_
-   Full event minutes details<br>
    _(view all documents and presentations related to each event)_

See the current [Seattle CDP Instance](https://councildataproject.org/seattle/#/) for a live example.

_Note: Some features are dependent on how much data is provided during event gather._
_More information see our [ingestion models documentation](https://councildataproject.org/cdp-backend/ingestion_models.html)._

## Usage

Regardless of your deployment strategy, you may find reading the
[Things to Know](#things-to-know) section helpful prior to deployment.

_Note: while this cookiecutter will help you setup a repository and CDP infrastructure,_
_you will still need to write your own custom data ingestion function._
_Writing a basic data ingestion function ranges from taking a couple of hours_
_to a couple of days depending on how much data you want to provide to our system._

### Deploying Under the councildataproject.org Domain

If you want your deployment under the councildataproject.org domain (i.e. https://councildataproject.org/seattle),
you will need to fill out the
["New Instance Deployment" Issue Form](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/issues/new/choose).

The Council Data Project team will help you along in the process on the
issue from there.

### Deploying Under Your Own Domain

If you want to host your deployment under a different domain
(i.e. Your-Org-Name.github.io/your-municipality),
you will need to install `cookiecutter` and use this template.

[**Follow along with the video walkthrough**](https://youtu.be/xdRhh-ocSfc)

Before you begin, please note that you will need to install or have available the following:

-   [gcloud](https://cloud.google.com/sdk/docs/install)
-   [gsutil](https://cloud.google.com/storage/docs/gsutil_install)
-   [Python 3.6+](https://www.python.org/downloads/) (Any Python version greater than or equal to 3.6)

Once all tools are installed, the rest of the infrastructure setup process
should take an hour or two.

In a terminal with Python 3.6+ installed:

```bash
pip install cookiecutter
cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment
```

Follow the prompts in your terminal and fill in the details for the instance deployment.
At the end of the process a new directory will have been created with all required
files and further instructions to set up your new deployment.

For more details and examples on each parameter of this cookiecutter template,
see [Cookiecutter Parameters](#cookiecutter-parameters).

Follow the steps in the "Initial Repository Setup" section of the
`README.md` file within the generated `SETUP` directory.

For more details on what is created from using this cookiecutter template,
see [Cookiecutter Repo Generation](#cookiecutter-repo-generation).

The short summary of setup tasks remaining are:

-   The creation of a new GitHub repository for the instance.
-   Logging in or creating an account for Google Cloud.
-   Initialize the basic infrastructure.
-   Assign a billing account to the created Google Cloud project.
-   Generate credentials for the Google Project for use in automated scripts.
-   Attach credentials as secrets to the GitHub repository.
-   Push the cookiecutter generated files to the GitHub repository.
-   Setup web hosting through GitHub Pages.
-   Enable open access for data stored by Google Cloud and Firebase.
-   Write a data ingestion function for your municipality (it may be useful to
    build off of [cdp-scrapers](https://github.com/CouncilDataProject/cdp-scrapers)).

You can also see an example generated repository and the full steps listed
[here](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/tree/example-build/SETUP).

### Cookiecutter Parameters

| Parameter                      | Description                                                                                                                                 | Example 1                                      | Example 2                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| municipality                   | The name of the municipality (town, city, county, etc.) that this CDP Instance will store data for.                                         | Seattle                                        | King County                                       |
| iana_timezone                  | The [IANA Timezone string](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) of the municipality that this CDP instance is for. | America/Los_Angeles                            | America/Chicago                                   |
| governing_body_type            | What type of governing body this instance is for.                                                                                           | city council                                   | county council                                    |
| municipality_slug              | The name of the municipality cleaned for use in the web application and parts of repository naming.                                         | seattle                                        | king-county                                       |
| python_municipality_slug       | The name of the municipality cleaned for use in specifically Python parts of the application.                                               | seattle                                        | king_county                                       |
| infrastructure_slug            | The name of the municipality cleaned for use in specifically application infrastructure. Must be globally unique to GCP.                    | cdp-seattle-abasjkqy                           | cdp-king-county-uiqmsbaw                          |
| maintainer_or_org_full_name    | The full name of the primary maintainer or organization that will be managing this instance deployment.                                     | Eva Maxfield Brown                         | Council Data Project                              |
| hosting_github_username_or_org | The GitHub username or organization that will host this instance's repository. (Used in the web application's domain name)                  | evamaxfield                                | CouncilDataProject                                |
| hosting_github_repo_name       | A specific name to give to the repository. (Used in the web application's full address)                                                     | cdp-seattle                                    | king-county                                       |
| hosting_github_url             | From the provided information, the expected URL of the GitHub repository.                                                                   | https://github.com/evamaxfield/cdp-seattle | https://github.com/CouncilDataProject/king-county |
| hosting_web_app_address        | From the provided information, the expected URL of the web application.                                                                     | https://evamaxfield.github.io/cdp-seattle  | https://councildataproject.org/king-county        |
| firestore_region               | The desired region to host the firestore instance. ([Firestore docs](https://firebase.google.com/docs/firestore/locations))                 | us-west1                                       | europe-central2                                   |
| default_event_gather_timedelta_lookback_days               | The number of days to look back from the current date every time the event scraper runs.                  | 2                                       | 6                                   |
| default_event_gather_cron               | The event gather CRON configuration. ([GitHub Actions CRON Details](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule))                 | 26 0,6,12,18 * * *                                       | 17 3,9,15,21 * * *                                   |

### Things to Know

Much of Council Data Project processing and resource management can be handled for free
and purely on GitHub. However we do rely on a select few resources outside of GitHub
to manage all services and applications.

The only service that will require a billing account to manage payment for resources
used, is [Google Cloud](#google-cloud). Google Cloud will manage all databases,
file storage, and (if needed) [speech-to-text](#speech-to-text) for transcription.
You can see more about the average monthly cost of running a
CDP Instance in [Cost](#cost).

For more details see [Cookiecutter Repo Generation](#cookiecutter-repo-generation).
_After creating the repo, the following steps will have instructions and links specific_
_to your deployment in the generated repository's README._

### Cookiecutter Repo Generation

`Cookiecutter` is a Python package to generate templated projects. This repository is
a template for `cookiecutter` to generate a CDP deployment repository which contains
following:

-   A directory structure for your project
-   A directory for your web application to build and deploy from
-   A directory for infrastructure management
-   A directory for your Python event gather function and it's requirements
-   Continuous integration
    -   Preconfigured for your web application to fully deploy
    -   Preconfigured to deploy all required CDP infrastructure
    -   Preconfigured to run CDP pipelines using GitHub Actions

To generate a new repository from this template, in a terminal with Python 3.5+
installed, run:

```bash
pip install cookiecutter
cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment
```

_Note: This will only create the basic repository._
_You will still need to set up a Google Cloud account._

### Google Cloud

All of your deployments data and some data processing will be done using
Google Cloud Platform (GCP).

-   Your deployment's provided and generated data (meeting dates, committee names, councilmember details, etc) will live in [Firestore](https://cloud.google.com/firestore).
-   Your deployment's generated files (audio clips, transcripts, etc.) will live in [Filestore](https://cloud.google.com/filestore).
-   When provided a video without closed captions, the audio from the provided video will be processed using [Speech-to-Text](https://cloud.google.com/speech-to-text).

## Cost

CDP was created and maintained by a group of people working on it in their free time.
We didn't want to pay extreme amounts of money so why should you?

To that end, we try to make CDP as low cost as possible. Many of the current features
are entirely free as long as the repo is open source:

Free Resources and Infrastructure:

-   Event Processing (GitHub Actions)
-   Event and Legislation Indexing (GitHub Actions)
-   Web Hosting (GitHub Pages)

The backend resources and processing are the only real costs and depend on usage.
The more users that use your web application, the more the database and
file storage cost. The CDP-Seattle monthly averages below are for the most utilized
months of its existence so take these as close to upper-bounds.

Billed Resources and Infrastructure:

-   [Cloud Firestore Pricing](https://firebase.google.com/pricing/)
    _CDP-Seattle monthly average: ~$19.00_
-   [Google Storage Pricing](https://cloud.google.com/storage/pricing#price-tables)
    _CDP-Seattle monthly average: ~$1.00_
-   [Google Speech-to-Text Pricing](https://cloud.google.com/speech-to-text/pricing)
    _CDP-Seattle monthly average: ~$40.00_

**Total Average Monthly Cost**: $60.00

This is the ongoing cost of storing new meetings as they occur once your instance is deployed.
You may have an additonal upfront cost if you are seeding your database with older videos and
using speech-to-text to transcribe them. At the time of this writing, it cost around $1.25 per
2 hours of video to transcribe and store.

### Speech-to-Text

You may not need to use speech-to-text! In the case your municipality provides closed
caption files in a format we support parsing and cleaning, we can use those files
instead of using speech-to-text. When using closed caption files for transcription
generation, CDP-Seattle speech-to-text costs dropped to ~$2.00 / month.

To use closed captions files instead of generating a transcript from audio,
your event gather function can attach a
[`closed_caption_uri`](https://councildataproject.org/cdp-backend/cdp_backend.pipeline.html#cdp_backend.pipeline.ingestion_models.Session)
to the `Session` object.

With speech-to-text cost removed, total average monthly cost for CDP-Seattle is ~$22.00.

### Future Processing Features

As we add more features to CDP that require additional processing or resources we
will continue to try to minimize their costs wherever possible.
Further, if a feature is optional, we will create a flag that maintainers can set
to include or exclude the additional processing or resource usage.
See [Upgrades and New Features](#upgrades-and-new-features) for more information.

## Upgrades and New Features

In general, all upgrades, bugfixes, new features, and more will be delivered to your
CDP repository via [Dependabot](https://github.com/dependabot).

After releasing a new version of `cdp-backend` or `cdp-frontend`, GitHub and Dependabot
will automatically create a pull request to your instance repository which updates
the version requirements of the pipelines, infrastructure, and/or web application.

These pull requests will contain the release notes for the each version that it upgrades
through, i.e. if it upgrades from 3.0.7 to 3.0.9, it will contain the release notes
for both 3.0.8 and 3.0.9. This should help you as a maintainer understand
what each upgrade is fixing or adding.

An example of such an automated pull request can be seen
[here](https://github.com/CouncilDataProject/seattle/pull/5).

Finally, in the case that an upgrade requires some additional work for the maintainer,
i.e. "regenerate the latest cookiecutter," or "run this script" -- we will explicitly
say so in our release notes. Those additional tasks are usually quite simple we just
haven't fully automated them yet.

An example of why we may ask for the maintainer to run a script after merging,
would be to backfill the data needed for a new feature. For example, if we update our
data model to allow for some new feature, data moving forward may be fine but data
from the past will be missing values and it may be optional but recommended to run the
backfill script to have the new feature available for all historical data.

## Citation

If you have found CDP software, data, or ideas useful in your own work,
please consider citing us:

Brown et al., (2021). Council Data Project: Software for Municipal Data Collection, Analysis, and Publication. Journal of Open Source Software, 6(68), 3904, https://doi.org/10.21105/joss.03904

```bibtex
@article{Brown2021,
  doi = {10.21105/joss.03904},
  url = {https://doi.org/10.21105/joss.03904},
  year = {2021},
  publisher = {The Open Journal},
  volume = {6},
  number = {68},
  pages = {3904},
  author = {Eva Maxfield Brown and To Huynh and Isaac Na and Brian Ledbetter and Hawk Ticehurst and Sarah Liu and Emily Gilles and Katlyn M. f. Greene and Sung Cho and Shak Ragoler and Nicholas Weber},
  title = {{Council Data Project: Software for Municipal Data Collection, Analysis, and Publication}},
  journal = {Journal of Open Source Software}
}
```

## License

[MIT](./LICENSE)
