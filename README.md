# Cookiecutter CDP Deployment

[![Example Deployment Status](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/workflows/Build%20Example%20Repo/badge.svg)](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/tree/example-build)

Cookiecutter template for new CDP deployments.

---

## About

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

By combining and simplifying sources of information on Council meetings and actions,
CDP ensures that everyone is empowered to participate in local government.

Each municipality that CDP supports (_a CDP instance_) has open source maintainers
which write code to gather municipality meeting information and compile them into a
single resource to then be processed, stored, and made accessible by our general CDP
tooling.

## Contributing

-   [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): Contains
    all the database models, data processing pipelines, and infrastructure-as-code for CDP
    deployments. Contributions here will be available to all CDP instances. Entirely
    written in Python.
-   [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): Contains all of
    the components used by the web apps to be hosted on GitHub Pages. Contributions here
    will be available to all CDP instances. Entirely written in
    TypeScript and React.
-   [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment):
    This repo. A template to be used by the Python `cookiecutter` package to create an
    entirely new deployment repository. This is where `cdp-backend` and `cdp-frontend` are
    imported and used. If you would like to create a new deployment under the
    `councildataproject.github.io` domain please
    [log a GitHub issue](https://github.com/CouncilDataProject/councildataproject.github.io/issues).
    If you want to utilize a different domain, simply use the template like any other
    `cookiecutter`.
-   [councildataproject.github.io](https://github.com/CouncilDataProject/councildataproject.github.io):
    Our landing page! Contributions here should largely be text changes and admin updates.

## Usage

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

To generate a new repository from this template, run:

```bash
pip install cookiecutter
cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment
```

**Free software: MIT license**
