# CDP - {{ cookiecutter.municipality }}

[![Infrastructure Deployment Status]({{ cookiecutter.hosting_github_url }}/workflows/Infrastructure/badge.svg)]({{ cookiecutter.hosting_github_url }}/actions?query=workflow%3A%22Infrastructure%22)
[![Event Processing Pipeline]({{ cookiecutter.hosting_github_url }}/workflows/Event%20Processing/badge.svg)]({{ cookiecutter.hosting_github_url }}/actions?query=workflow%3A%22Event+Processing%22)
[![Event Index Pipeline]({{ cookiecutter.hosting_github_url }}/workflows/Event%20Index/badge.svg)]({{ cookiecutter.hosting_github_url }}/actions?query=workflow%3A%22Event+Index%22)
[![Web Deployment Status]({{ cookiecutter.hosting_github_url }}/workflows/Web%20App/badge.svg)](https://{{ cookiecutter.hosting_github_username_or_org }}.github.io/{{ cookiecutter.hosting_github_reponame }})
[![Repo Build Status]({{ cookiecutter.hosting_github_url }}/workflows/Build%20Main/badge.svg)]({{ cookiecutter.hosting_github_url }}/actions?query=workflow%3A%22Build+Main%22)

---

## CouncilDataProject

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

For more information about CouncilDataProject, please visit
[our website](https://councildataproject.github.io/).

## Instance Information

This repo serves the municipality: **{{ cookiecutter.municipality }}**

## Contributing

If you wish to contribute to CDP please note that the best method to do so is to
contribute to the upstream libraries that compose the CDP instances themselves.
These are detailed below.

-   [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): Contains
    all the database models, data processing pipelines, and infrastructure-as-code for CDP
    deployments. Contributions here will be available to all CDP instances. Entirely
    written in Python.
-   [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): Contains all of
    the components used by the web apps to be hosted on GitHub Pages. Contributions here
    will be available to all CDP instances. Entirely written in
    TypeScript and React.
-   [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment):
    The repo used to generate new CDP Instance deployments. Like this repo!
-   [councildataproject.github.io](https://github.com/CouncilDataProject/councildataproject.github.io):
    Our landing page! Contributions here should largely be text changes and admin updates.

## Initial Repo Setup

1.  Create (or sign in to) a Google Cloud Platform (GCP) account.
    ([Google Cloud Console Home](https://console.cloud.google.com/))<br>
    Google Cloud Platform is where all data and files will be stored, and some
    processing will be done using GCP resources.
    More details available in the [Google Cloud](#google-cloud) section.
2.  Create (or re-use) a [billing account](https://console.cloud.google.com/billing)
    and attach it to your GCP account.<br>
    For more details on the cost of maintaining a CDP Instance, see [Cost](#cost).
3.  PLACEHOLDER: GET GOOGLE CLOUD CREDENTIALS<br>
    _I remember this is where things went wrong in setting things up..._
4.  Create (or sign in to) a Pulumi account.
    ([Pulumi Account Sign-Up](https://app.pulumi.com/signup))<br>
    Pulumi tracks and manages the state of your instances infrastructure
    (databases, file storage servers, credentials, etc.).
    More details available in the [Pulumi](#pulumi) section.
5.  Create a [Pulumi Access Token](https://app.pulumi.com/account/tokens).<br>
    Keep this token available. We will use it later.
6.
7.  Create the GitHub repository for this deployment to live in.
    [Create a new Repository](https://github.com/new)
    Set the repo name to what you
    Be sure to select the correct "Owner" (the organization or account to use)
    Set the repo to "Public", do not initialize with any of the extra options

---

1.  Create a [new GitHub repo](https://github.com/{{ cookiecutter.hosting_github_username_or_org}}/repositories/new).

    -   Set the "Repository name" to: **{{ cookiecutter.hosting_github_reponame }}**
    -   Select the "Public" option for repository visibility.
    -   Do not select any of the "Initialize this repository with" options.

2.  [ ] Turn on GitHub Pages for the `gh-pages` branch ([Repo Settings]({{ cookiecutter.hosting_github_url }}/settings))
3.  [ ] Write Python event gather function [`get_events`](python/cdp\_{{ cookiecutter.python_municipality_slug }}\_backend/scraper.py)
4.  [ ] Add [GitHub Actions repository secrets]({{ cookiecutter.hosting_github_url }}/settings/secrets/actions) for:

    -   [ ] Google Cloud (`GOOGLE_CREDENTIALS`)
    -   [ ] Pulumi (`PULUMI_ACCESS_TOKEN`)
