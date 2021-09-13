# CDP Instance Setup

This document outlines the steps necessary to finish initializing this CDP Instance.

## Initial Repository Setup

1.  Create (or sign in to) a Google Cloud Platform (GCP) account.
    ([Google Cloud Console Home](https://console.cloud.google.com/))

    Google Cloud Platform is where all data and files will be stored, and some
    processing will be done using GCP resources. More details can be found
    [here](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#google-cloud).

2.  Create (or re-use) a [billing account](https://console.cloud.google.com/billing)
    and attach it to your GCP account.

    For more details on the cost of maintaining a CDP Instance, see our [estimated cost breakdown](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#cost).

3.  Create a new [Google Cloud Project](https://console.cloud.google.com/projectcreate).

    Set the project name to: **cdp-example-IIxkylGT**.

4.  After clicking "Create", Google Cloud will take a second to prevision the project.
    Once it has, you will have access to the [project's dashboard](https://console.cloud.google.com/home/dashboard?project=cdp-example-IIxkylGT).

5.  Create a [Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts/create?project=cdp-example-IIxkylGT).

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

8.  Enable the [Cloud Resource Manager API](https://console.cloud.google.com/apis/library/cloudresourcemanager.googleapis.com?project=cdp-example-IIxkylGT).

9.  Create (or sign in to) a Pulumi account.
    ([Pulumi Account Sign-Up](https://app.pulumi.com/signup))

    Pulumi tracks and manages the state of your instance's infrastructure
    (databases, file storage servers, credentials, etc.). More details can be found
    [here](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#pulumi).

10. Create a [Pulumi Access Token](https://app.pulumi.com/account/tokens).

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

**If all steps complete successful your web application will be viewable at: https://CouncilDataProject/github.io/example**

## Data Gathering Setup

Once your repository, infrastructure, and web application have been set up, you will need to write an event data gathering function.

Navigate and follow the instructions in the the file: `python/cdp_example_backend/scraper.py`.

As soon as you push your updates to your event gather function (`get_events`) to your GitHub repository, everything will be tested and configured for the next pipeline run.

There are some optional configurations for the data gathering pipeline which can be added to `python/event-gather-config.json`. No action is needed for a barebones pipeline run, but the optional parameters can be checked in the [CDP pipeline config documentation](https://councildataproject.org/cdp-backend/cdp_backend.pipeline.html#module-cdp_backend.pipeline.pipeline_config). Note that `google_credentials_file` and `get_events_function_path` should not be modified and will populate automatically if you have followed the steps above.

Be sure to review the [CDP Ingestion Model documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html) for the object definition to return from your `get_events` function.

Once your function is complete and pushed to the `main` branch, feel free to delete this setup file.
