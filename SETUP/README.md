# CDP Instance Setup

This document outlines the steps necessary to finish initializing this CDP Instance.

## Before You Begin

Install the command line tools that will help shorten the setup process

1. Install [gcloud](https://cloud.google.com/sdk/docs/install)
2. Install [pulumi](https://www.pulumi.com/docs/get-started/install/)
3. Install [gsutil](https://cloud.google.com/storage/docs/gsutil_install)

## Initial Repository Setup

There are additional tasks required after generating this repository.

1.  Create the GitHub repository for this deployment to live in.

    [Create a new Repository](https://github.com/new) with the following parameters:

    -   Set the repo name to: **example**
    -   Set the repo owner to: **CouncilDataProject**
    -   Set the repo visibility to: "Public"
    -   Do not initialize with any of the extra options
    -   Click "Create repository".

1.  Login to both Google Cloud and Pulumi.

    During this process Pulumi will provide a token to use for authentication.
    Keep this token available for use in a later step.

    This step should be run while within the `SETUP` directory (`cd SETUP`).

    Run:

    ```bash
    make login
    ```

1.  Initialize the basic project infrastructure.

    This step should be run while within the `SETUP` directory (`cd SETUP`)

    Run:

    ```bash
    make init
    ```

1.  Create (or re-use) a
    [Google Cloud billing account](https://console.cloud.google.com/billing/linkedaccount?project=cdp-example-xhxljvjs)
    and attach it to the newly created project (cdp-example-xhxljvjs).

    For more details on the cost of maintaining a CDP Instance, see our [estimated cost breakdown](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#cost).

1.  Generate a Google Service Account JSON Key for your Google Cloud Project.

    This will create a directory called `.keys` within this `SETUP` directory and
    add a file called `cdp-example-xhxljvjs.json` to it
    (i.e. `.keys/cdp-example-xhxljvjs)`. This file will be used later on.

    Run:

    ```bash
    make gen-key
    ```

1.  Attach the Pulumi Access Token and the
    Google Service Account JSON as GitHub Repository Secrets.

    1. Pulumi Access Token -- Create a [new secret](https://github.com/CouncilDataProject/example/settings/secrets/actions/new)

    -   Set the name to: **PULUMI_ACCESS_TOKEN**
    -   Set the value to: The token you kept from step #2
    -   Click "Add secret"

    2. Google Service Account JSON -- Create a [new secret](https://github.com/CouncilDataProject/example/settings/secrets/actions/new)

    -   Set the name to: **GOOGLE_CREDENTIALS**
    -   Set the value to: the contents of the file `.keys/cdp-example-xhxljvjs.json`
    -   Click "Add secret"

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

1.  Once the
    ["Infrastructure" GitHub Action Successfully Completes](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
    set the CORS policy for your Storage Bucket.

    This step should be run while within the `SETUP` directory (`cd SETUP`)

    Run:

    ```bash
    make set-cors
    ```

1.  Once the
    ["Infrastructure" GitHub Action Successfully Completes](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
    configure Firebase Security Rules.

    -   Navigate to [Firebase Console](https://console.firebase.google.com),
        login to the Google Account you used during step #2, select the `cdp-example-xhxljvjs` Firebase project
        -   Navigate to "Firestore Database", select the "Rules" tab, paste the following in:
            ```
            rules_version = '2';
            service cloud.firestore {
                match /databases/{database}/documents {
                    match /{document=**} {
                        allow read;
                    }
                }
            }
            ```
        -   Click "Publish"
        -   Navigate to "Storage", select the "Rules" tab, paste the following in:
            ```
            rules_version = '2';
            service firebase.storage {
                match /b/{bucket}/o {
                    match /{allPaths=**} {
                        allow read;
                    }
                }
            }
            ```
        -   Click "Publish"

**If all steps complete successful your web application will be viewable at: https://CouncilDataProject.github.io/example**

## Data Gathering Setup

Once your repository, infrastructure, and web application have been set up, you will need to write an event data gathering function.

Navigate and follow the instructions in the the file: `python/cdp_example_backend/scraper.py`.

As soon as you push your updates to your event gather function (`get_events`) to your GitHub repository, everything will be tested and configured for the next pipeline run.

There are some optional configurations for the data gathering pipeline which can be added to `python/event-gather-config.json`. No action is needed for a barebones pipeline run, but the optional parameters can be checked in the [CDP pipeline config documentation](https://councildataproject.org/cdp-backend/cdp_backend.pipeline.html#module-cdp_backend.pipeline.pipeline_config). Note that `google_credentials_file` and `get_events_function_path` should not be modified and will populate automatically if you have followed the steps above.

Be sure to review the [CDP Ingestion Model documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html) for the object definition to return from your `get_events` function.

Once your function is complete and pushed to the `main` branch, feel free to delete this setup directory.

## Other Documentation

For more documentation on adding data to your new CDP instance and maintainer or customizing your instance
please see the "admin-docs" directory.
