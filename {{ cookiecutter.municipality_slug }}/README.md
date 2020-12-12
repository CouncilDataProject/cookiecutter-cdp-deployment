# CDP - {{ cookiecutter.municipality }}

[![Build Status](https://github.com/{{ cookiecutter.hosting_github_username_or_org }}/{{ cookiecutter.municipality_slug }}/workflows/Build%20Main/badge.svg)](https://github.com/{{ cookiecutter.hosting_github_username_or_org }}/{{ cookiecutter.municipality_slug }}/actions)

---

-   A directory structure for your project
-   A directory for the web app to build and deploy from
-   A directory for infrastructure management
-   A directory for your Python event gather function and it's requirements
-   Continuous integration
    -   Preconfigured for web app to fully deploy
    -   Preconfigured to deploy all required CDP infrastructure
    -   Preconfigured to run CDP pipelines using GitHub Actions
