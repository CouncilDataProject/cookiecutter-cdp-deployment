# CDP Instance Setup

This document outlines the steps necessary to finish initializing this CDP Instance.

## Before You Begin

Install the command line tools that will help shorten the setup process

1. Install [gcloud](https://cloud.google.com/sdk/docs/install)
1. Install [gsutil](https://cloud.google.com/storage/docs/gsutil_install)
1. Install [firebase-tools](https://firebase.google.com/docs/cli/)
1. Install [just](https://github.com/casey/just)

## Initial Repository Setup

There are additional tasks required after generating this repository.

1.  Create the GitHub repository for this deployment to live in.

    [Create a new Repository](https://github.com/new) with the following parameters:

    -   Set the repo name to: **example**
    -   Set the repo owner to: **CouncilDataProject**
    -   Set the repo visibility to: "Public"
    -   Do not initialize with any of the extra options
    -   Click "Create repository".

1. Install `cdp-backend`.

    This step should be ran while within the `SETUP` directory (`cd SETUP`).

    ```bash
    pip install ../python/
    ```

1. Get the infrastructure files.

    This step should be ran while within the `SETUP` directory (`cd SETUP`).

    ```bash
    get_cdp_infrastructure_stack .
    ```

1.  Login to Google Cloud.

    This step should be run while within the `SETUP` directory (`cd SETUP`).

    Run:

    ```bash
    just login
    ```

1.  Initialize the basic project infrastructure.

    This step should be run while within the `SETUP` directory (`cd SETUP`)

    Run:

    ```bash
    just init cdp-example-ereuzelu
    ```

    This step will also generate a Google Service Account JSON file and store it
    in a directory called `.keys` in the root of this repository.

1.  Set or update the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the
    path to the key that was just generated.

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="INSERT/PATH/HERE"
    ```

1.  Create (or re-use) a
    [Google Cloud billing account](https://console.cloud.google.com/billing/linkedaccount?project=cdp-example-ereuzelu)
    and attach it to the newly created project (cdp-example-ereuzelu).

    For more details on the cost of maintaining a CDP Instance, see our [estimated cost breakdown](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#cost).

1.  Generate a Firebase CI token.

    ```bash
    firebase login:ci
    ```

    Save the created token for a following step!

1.  Create a GitHub Personal Access Token.

    Create a new (classic) GitHub Personal Access Token by navigating to
    [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new).

    -   Click the "Generate new token" dropdown.
    -   Select "Generate new token (classic)".
    -   Give the token a descriptive name / note. We recommend: `cdp-example-ereuzelu`
    -   Set the expiration to "No expiration"
        -   You can set a set expiration if you would like, you will simply have to update this token later.
    -   Select the `repo` checkbox to give access this token access to the repo.
    -   Click the "Generate token" button.

    Save the created token for a following step.

    For more documentation and assistance see
    [GitHub's Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic).

1.  Attach the Google Service Account JSON as GitHub Repository Secret.

    1. Create a [new secret](https://github.com/CouncilDataProject/example/settings/secrets/actions/new)

    -   Set the name to: **GOOGLE_CREDENTIALS**
    -   Set the value to: the contents of the file `.keys/cdp-example-ereuzelu.json`
    -   Click "Add secret"

    2. Create a [new secret](https://github.com/CouncilDataProject/example/settings/secrets/actions/new)

    -   Set the name to: **FIREBASE_TOKEN**
    -   Set the value to: the value of the Firebase CI token you created in a prior step.
    -   Click "Add secret"

    3. Create a [new secret](https://github.com/CouncilDataProject/example/settings/secrets/actions/new)
    
    -   Set the name to: **PERSONAL_ACCESS_TOKEN**
    -   Set the value to: the value of the GitHub Personal Access Token you created in a prior step.
    -   Click "Add secret"

1.  Build the basic project infrastructure.

    This step should be run while within the `SETUP` directory (`cd SETUP`)

    ```bash
    just setup cdp-example-ereuzelu us-central
    ```

1.  Initialize Firebase Storage.

    [Firestore Storage Page](https://console.firebase.google.com/u/0/project/cdp-example-ereuzelu/storage)

    The default settings ("Start in Production Mode" and default region) for setting up
    storage are fine.

1.  Initialize and push the local repository to GitHub.

    This step should be run while within the base directory of the repository (`cd ..`).

    To initialize the repo locally, run:

    ```bash
    git init
    git add -A
    git commit -m "Initial commit"
    git branch -M main
    ```

    To setup a connection to our GitHub repo, run either:

    ```bash
    git remote add origin https://github.com/CouncilDataProject/example.git
    ```

    Or (with SSH):

    ```bash
    git remote add origin git@github.com:CouncilDataProject/example.git
    ```

    Finally, to push this repo to GitHub, run:

    ```bash
    git push -u origin main
    ```

    Now refresh your repository's dashboard to ensure that all files were pushed.

1.  Once the
    ["Web App" GitHub Action Successfully Complete](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Web+App%22)
    configure GitHub Pages.

    Go to your repository's [GitHub Pages Configuration](https://github.com/CouncilDataProject/example/settings/pages)

    -   Set the source to: "gh-pages"
    -   Set the folder to: `/ (root)`
    -   Click "Save"

1. Once the ["Infrastructure" GitHub Action Successfully Completes](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22) request a quota increase for `compute.googleapis.com/gpus_all_regions`.

    [Direct Link to Quota](https://console.cloud.google.com/iam-admin/quotas?project=cdp-example-ereuzelu&pageState=(%22allQuotasTable%22:(%22f%22:%22%255B%257B_22k_22_3A_22Metric_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22compute.googleapis.com%252Fgpus_all_regions_5C_22_22_2C_22s_22_3Atrue_2C_22i_22_3A_22metricName_22%257D%255D%22)))

    -   Click the checkbox for the "GPUs (all regions)"
    -   Click the "EDIT QUOTAS" button
    -   In the "New limit" text field, enter a value of: `2`.
        -   You can request more or less than `2` GPUs, however we have noticed that a
            request of `2` is generally automatically accepted.
    -   In the "Request description" text field, enter a value of: speech-to-text
        model application and downstream text tasks
    -   Click the "NEXT" button
    -   Enter your name and phone number into the contact fields.
    -   Click the "SUBMIT REQUEST" button

    If the above direct link doesn't work, follow the instructions from
    [Google Documentation](https://cloud.google.com/docs/quota#requesting_higher_quota).

    You will need to wait until the quota increase has been approved before running any
    event processing. From our experience, the quota is approved within 15 minutes.

**If all steps complete successful your web application will be viewable at: https://CouncilDataProject.github.io/example**

## Data Gathering Setup

Once your repository, infrastructure, and web application have been set up, you will need to write an event data gathering function.

Navigate and follow the instructions in the the file: `python/cdp_example_backend/scraper.py`.

As soon as you push your updates to your event gather function (`get_events`) to your GitHub repository, everything will be tested and configured for the next pipeline run. Events are gathered from this function every 6 hours from the default branch via a Github Action cron job. If you'd like to manually run event gathering, you can do so from within the Actions tab of your repo -> Event Gather -> Run workflow.

It is expected that the Event Index workflow will fail to start, as your database will not yet be populated with events to index.

There are some optional configurations for the data gathering pipeline which can be added to `python/event-gather-config.json`. No action is needed for a barebones pipeline run, but the optional parameters can be checked in the [CDP pipeline config documentation](https://councildataproject.org/cdp-backend/cdp_backend.pipeline.html#module-cdp_backend.pipeline.pipeline_config). Note that `google_credentials_file` and `get_events_function_path` should not be modified and will populate automatically if you have followed the steps above.

Be sure to review the [CDP Ingestion Model documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html) for the object definition to return from your `get_events` function.

Once your function is complete and pushed to the `main` branch, feel free to delete this setup directory.

## Other Documentation

For more documentation on adding data to your new CDP instance and maintainer or customizing your instance
please see the "admin-docs" directory.
