# CDP - Example

[![Infrastructure Deployment Status](https://github.com/CouncilDataProject/example/workflows/Infrastructure/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
[![Event Processing Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Gather/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Gather%22)
[![Event Index Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Index/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Index%22)
[![Web Deployment Status](https://github.com/CouncilDataProject/example/workflows/Web%20App/badge.svg)](https://CouncilDataProject/github.io/example)
[![Repo Build Status](https://github.com/CouncilDataProject/example/workflows/Build%20Main/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Build+Main%22)

---

## Council Data Project

Council Data Project is an open-source project dedicated to providing journalists, activists, researchers, and all members of each community we serve with the tools they need to stay informed and hold their Council Members accountable.

For more information about Council Data Project, please visit [our website](https://councildataproject.org/).

## Instance Information

This repo serves the municipality: **Example**

### Python Access

```python
from cdp_backend.database import models as db_models
from cdp_backend.pipeline.transcript_model import Transcript
import fireo
from gcsfs import GCSFileSystem
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client

# Connect to Database
fireo.connection(client=Client(
    project="cdp-example-eMSoBrJy",
    credentials=AnonymousCredentials()
))

# Read from Database
five_people = list(db_models.Person.collection.fetch(5))

# Connect to File Store
fs = GCSFileSystem(project="cdp-example-eMSoBrJy", token="anon")

# Read transcript details and download the transcript file to local machine
transcript_model = list(db_models.Transcript.collection.fetch(1))[0]

# Download with `get` and then load from the new local file
fs.get(transcript_model.file_ref.uri, "local-transcript.json")
with open("local-transcript.json", "r") as open_resource:
    transcript = Transcript.from_json(open_resource.read())

# Or load from directly remote
with fs.open(transcript_model.file_ref.uri, "r") as open_resource:
    transcript = Transcript.from_json(open_resource.read())

# Read transcript
with open("local-transcript.json", "r") as open_f:
    transcript = Transcript.from_json(open_f.read())
```

-   See [CDP Database Schema](https://councildataproject.org/cdp-backend/database_schema.html)
    for a Council Data Project database schema diagram.
-   See [FireO documentation](https://octabyte.io/FireO/)
    to learn how to construct queries against CDP database models models.
-   See [GCSFS documentation](https://gcsfs.readthedocs.io/en/latest/index.html)
    to learn how to retrieve files from the file store.

## Contributing

If you wish to contribute to CDP please note that the best method to do so is to contribute to the upstream libraries that compose the CDP Instances themselves. These are detailed below.

-   [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): Contains all the database models, data processing pipelines, and infrastructure-as-code for CDP deployments. Contributions here will be available to all CDP Instances. Entirely written in Python.
-   [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): Contains all of the components used by the web apps to be hosted on GitHub Pages. Contributions here will be available to all CDP Instances. Entirely written in TypeScript and React.
-   [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment): The repo used to generate new CDP Instance deployments. Like this repo!
-   [councildataproject.org](https://github.com/CouncilDataProject/councildataproject.github.io): Our landing page! Contributions here should largely be text changes and admin updates.
