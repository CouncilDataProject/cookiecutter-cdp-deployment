# CDP Instance Setup

This document outlines the steps necessary to finish initializing this CDP Instance.

## Before You Begin

Install the command line tools that will help shorten the setup process

1. Install [gcloud](https://cloud.google.com/sdk/docs/install)
2. Install [pulumi](https://www.pulumi.com/docs/get-started/install/)

## Initial Repository Setup

There are additional tasks required after generating this directory.
While in this `SETUP` directory:

1. Create the GitHub repository for this deployment to live in.
   [Create a new Repository](https://github.com/new)

    - Set the repo name to: **{{ cookiecutter.hosting_github_repo_name }}**
    - Set the repo owner to: **{{ cookiecutter.hosting_github_username_or_org }}**
    - Set the repo visibility to: "Public"
    - Do not initialize with any of the extra options
    - Click "Create repository".

1. Login to both Google Cloud and Pulumi.

    During this process Pulumi will provide a token to use for authentication.
    Keep this token available for use in a later step.

    ```bash
    make login
    ```

1. Initialize the basic project infrastructure.

    ```bash
    make init
    ```

1. Create (or re-use) a
   [billing account](https://console.cloud.google.com/billing/linkedaccount?project={{ cookiecutter.infrastructure_slug }})
   and attach it to your GCP account and the newly creating project.

    For more details on the cost of maintaining a CDP Instance, see our [estimated cost breakdown](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment#cost).

1. Generate a Google Service Account JSON Key for your newly create Google Project.

    This will create a directory called `.keys` within this `SETUP` directory and
    add a file called `{{ cookiecutter.infrastructure_slug }}.json` to it
    (i.e. `.keys/{{ cookiecutter.infrastructure_slug }})`. This file will be used later on.

    ```bash
    make gen-key
    ```

1. Attach the Pulumi Access Token and the
   Google Service Account JSON as GitHub Repository Secrets.

    1. Pulumi Access Token

    Create a [new secret]({{ cookiecutter.hosting_github_url }}/settings/secrets/actions/new)

    - Set the name to: **PULUMI_ACCESS_TOKEN**
    - Set the value to: The token you kept from step #2
    - Click "Add secret"

    2. Google Service Account JSON

    Create a [new secret]({{ cookiecutter.hosting_github_url }}/settings/secrets/actions/new)

    - Set the name to: **GOOGLE_CREDENTIALS**
    - Set the value to: the contents of the file `.keys/{{ cookiecutter.infrastructure_slug }}.json`
    - Click "Add secret"

1. Initialize and push the local repository to GitHub.

    - In a terminal, while in this repository's directory, run:
        ```bash
        git init
        git add -A
        git commit -m "Initial commit"
        git branch -M main
        git remote add origin {{ cookiecutter.hosting_github_url }}.git
        git push -u origin main
        ```
    - Refresh your repository's dashboard to ensure that all files were pushed.

1. Configure GitHub Pages.

    Go to your repository's [GitHub Pages Configuration]({{ cookiecutter.hosting_github_url }}/settings/pages)

    - Set the source to: "gh-pages"
    - Set the folder to: `/ (root)`
    - Click "Save"

    If you don't see these options immediately you may need to wait a minute or so and then try again.

1. Set the CORS policy for your Storage Bucket.

    ```bash
    make set-cors
    ```

1. Configure Firebase Security Rules.

    - Navigate to [Firebase Console](https://console.firebase.google.com),
      login to the Google Account you used during step #2, select the `{{ cookiecutter.infrastructure_slug }}` Firebase project
        - Navigate to "Firestore Database", select the "Rules" tab, paste the following in:
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
        - Navigate to "Storage", select the "Rules" tab, paste the following in:
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

**If all steps complete successful your web application will be viewable at: {{ cookiecutter.hosting_web_app_address }}**

## Data Gathering Setup

Once your repository, infrastructure, and web application have been set up, you will need to write an event data gathering function.

Navigate and follow the instructions in the the file: `python/cdp_{{ cookiecutter.python_municipality_slug }}_backend/scraper.py`.

As soon as you push your updates to your event gather function (`get_events`) to your GitHub repository, everything will be tested and configured for the next pipeline run.

There are some optional configurations for the data gathering pipeline which can be added to `python/event-gather-config.json`. No action is needed for a barebones pipeline run, but the optional parameters can be checked in the [CDP pipeline config documentation](https://councildataproject.org/cdp-backend/cdp_backend.pipeline.html#module-cdp_backend.pipeline.pipeline_config). Note that `google_credentials_file` and `get_events_function_path` should not be modified and will populate automatically if you have followed the steps above.

Be sure to review the [CDP Ingestion Model documentation](https://councildataproject.github.io/cdp-backend/ingestion_models.html) for the object definition to return from your `get_events` function.

Once your function is complete and pushed to the `main` branch, feel free to delete this setup file.

## Other Documentation

For more documentation on adding data to your new CDP instance and maintainer or customizing your instance
please see the "admin-docs" directory.
