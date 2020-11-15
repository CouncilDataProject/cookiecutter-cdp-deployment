# Cookiecutter CDP Deployment

[![Example Deployment Status](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/workflows/Build%20Example%20Repo/badge.svg)](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment/tree/example-build)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Cookiecutter template for new CDP deployments.

---

## About
`Cookiecutter` is a Python package to generate templated projects.
This repository is a template for `cookiecutter` to generate a CDP deployment which
contains following:

* A directory structure for your project
* A directory for the web app to build and deploy from
* A directory for infrastructure management
* A directory for your Python event gather function and it's requirements
* Continuous integration
  * Preconfigured for web app to fully deploy
  * Preconfigured to deploy all required CDP infrastructure
  * Preconfigured to run CDP pipelines using GitHub Actions


**Original repo:** https://github.com/audreyr/cookiecutter-pypackage/
