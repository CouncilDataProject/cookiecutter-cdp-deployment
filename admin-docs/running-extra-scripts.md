# Running Extra Scripts

### Background

While we hope for it to be rare, when we ship changes to `cdp-backend` or `cdp-frontend`
require changes to the data or file storage system that we cannot make during a normal
pipeline run, or if you want to manage your data in some way, there is a GitHub Action
that allows the passthrough of any command straight to the running GitHub Action
worker.

## Backfilling Session Context Hash

In our [v3.0.4 release of `cdp-backend`](https://github.com/CouncilDataProject/cdp-backend/releases/tag/v3.0.4)
we added a property to the `Session` collection that stores the `session_context_hash`.
This value is incredibly useful for programmatic work but isn't _needed_ for the
web application. As such, if you don't want to run this script, you don't need to,
but it is easy enough to run.

Open up the [Run Command](https://github.com/CouncilDataProject/example/actions/workflows/run-script.yml)
GitHub Action and click the "Run workflow" button.

Paste in the following: `add_content_hash_to_sessions --google_credentials_file google-creds.json`

Click the "Run workflow" button and the backfill process should kick off.
(If the run doesn't appear, try refreshing the page.)

If something goes wrong, please create a
[GitHub Issue in `cdp-backend`](https://github.com/CouncilDataProject/cdp-backend/issues)
