# CDP - Example

[![Infrastructure Deployment Status](https://github.com/CouncilDataProject/example/workflows/Infrastructure/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
[![Event Processing Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Processing/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Processing%22)
[![Event Index Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Index/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Index%22)
[![Web Deployment Status](https://github.com/CouncilDataProject/example/workflows/Web%20App/badge.svg)](https://CouncilDataProject/github.io/example)
[![Repo Build Status](https://github.com/CouncilDataProject/example/workflows/Build%20Main/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Build+Main%22)

---

## CouncilDataProject

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

For more information about CouncilDataProject, please visit
[our website](https://councildataproject.github.io/).

## Instance Information

This repo serves the municipality: **Example**

## Contributing

If you wish to contribute to CDP please note that the best method to do so is to
contribute to the upstream libraries that compose the CDP Instances themselves.
These are detailed below.

-   [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): Contains
    all the database models, data processing pipelines, and infrastructure-as-code for CDP
    deployments. Contributions here will be available to all CDP Instances. Entirely
    written in Python.
-   [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): Contains all of
    the components used by the web apps to be hosted on GitHub Pages. Contributions here
    will be available to all CDP Instances. Entirely written in
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
    More details available in the
    [Cookiecutter Google Cloud](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#google-cloud)
    section.
2.  Create (or re-use) a [billing account](https://console.cloud.google.com/billing)
    and attach it to your GCP account.<br>
    For more details on the cost of maintaining a CDP Instance, see [Cost](#cost).
3.  Create a new [Google Cloud Project](https://console.cloud.google.com/projectcreate).
    -   Set the project name to: **cdp-example**.
4.  After clicking "Create", Google Cloud will take a second to prevision the project.
    Once it has, you will have access to the
    [project's dashboard](https://console.cloud.google.com/home/dashboard?project=cdp-example).
5.  Create a [Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts/create?project=cdp-example).
    -   Set the Service Acount Name to: "GitHub Actions Runner".
    -   Click "Create".
    -   Grant the access to the project for the service account:
        -   Select the "Editor" (Edit access to all resources) role.
    -   Do not grant users access to this service account.
    -   Click "Done".
6.  On the "Service Accounts" dashboard, select the newly created service acount.
7.  Generate a new JSON Key for the Service Account.
    -   Navigate to the "Keys" tab.
    -   Click "Add Key" and "Create new key".
    -   Select JSON.
    -   Click "Create".
    -   Save the file somewhere safe. We will use it later.
        _Do not save this file to the this repository's directory._
8.  Enable the [Cloud Resource Manager API](https://console.cloud.google.com/apis/library/cloudresourcemanager.googleapis.com?project=cdp-example).
9.  Create (or sign in to) a Pulumi account.
    ([Pulumi Account Sign-Up](https://app.pulumi.com/signup))<br>
    Pulumi tracks and manages the state of your instance's infrastructure
    (databases, file storage servers, credentials, etc.).
    More details available in the
    [Cookiecutter Pulumi](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#pulumi)
    section.
10. Create a [Pulumi Access Token](https://app.pulumi.com/account/tokens).<br>
    -   Click "Create token".
    -   Set the description to: "example-github-actions-runner".
    -   Click "Create token".
    -   Copy and save the token somewhere safe. We will use it later.
        _Do not save this token as a file in this repository's directory._
11. Create the GitHub repository for this deployment to live in.
    [Create a new Repository](https://github.com/new)
    -   Set the repo name to: **example**
    -   Set the repo owner to: **CouncilDataProject**
    -   Set the repo visibility to: "Public"
    -   Do not initialize with any of the extra options
    -   Click "Create repository".
12. Initialize and push the local repository to GitHub.
    -   In a terminal, while in this repository's directory, run:
        ```bash
        git init
        git add -A
        git commit -m "Initial commit"
        git branch -M main
        git remote add origin https://github.com/CouncilDataProject/example.git
        git push -u origin main
        ```
    -   Refresh your repository's dashboard to ensure that all files were pushed.
13. Configure [repository settings](https://github.com/CouncilDataProject/example/settings).
    -   In the "Options" tab, configure "GitHub Pages"
        -   Select "gh-pages" from the "Source" dropdown.
        -   Click "Save".
    -   In the "Secrets" tab, configure two "Actions secrets"
        -   Click "New repository secret".
        -   Set "Name" to: **GOOGLE_CREDENTIALS**
        -   Open up the file downloaded from Google Cloud (the Service Account JSON),
            copy all text in the file, paste the text into the "Value" field.
        -   Click "Add secret".
        -   Click "New repository secret".
        -   Set "Name" to: **PULUMI_ACCESS_TOKEN**
        -   Open up the file or browser tab where you saved your Pulumi token,
            copy the token, past the token into the "Value" field.
        -   Click "Add secret".
14. Navigate to [GitHub Actions History](https://github.com/CouncilDataProject/example/actions).

    -   Click on the "workflow run" tagged with "Initial commit" and "Infrastructure".
    -   Click the "Re-run jobs" dropdown.
    -   Click "Re-run all jobs".

**If all steps complete successful your web application will be viewable at:
https://CouncilDataProject/github.io/example**

Once all of these steps are done, feel free to delete this section of the README.

## Data Gathering Setup

Once your repository, infrastructure, and web application have been set up,
you will need to write an event data gathering function.

Navigate and follow the instructions in the the file:
`python/cdp_example_backend/scraper.py`.

As soon as you push your updates to your event gather function (`get_events`)
to your GitHub repository, everything will be tested and configured for the
next pipeline run.

Be sure to review the
[CDP Ingestion Model documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html)
for the object definition to return from your `get_events` function.

Once your function is complete and pushed to the `main` branch,
feel free to delete this section of the README.
