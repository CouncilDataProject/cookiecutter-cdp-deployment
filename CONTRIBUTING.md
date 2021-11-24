# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Cookiecutter Contribution vs Application Contribution

Please note that this repository is only the cookiecutter and not the entire
CDP tooling and infrastructure ecosystem. This repository ties all of our
tooling together into a single repository that is easy to deploy and maintain.
Contributions to this repository should largely be documentation,
devops, bugfixes, or similar.

If you experience a bug or incorrect documentation while using the cookiecutter
please do send us a Pull Request! If you want to add or fix an auto-deployment
bot, or add more GitHub Actions to the produced repository, all such contributions
welcome and appreciated.

Examples of these types of contributions include:

-   adding more instance admin documentation to the generated repository
-   updating the `cdp-backend` and `cdp-frontend` version pins
-   upgrading or fixing and auto-deployment GitHub Action
-   adding new GitHub Actions to the generated repository

For contributions to the major pipelines and infrastructure that are used by all
CDP deployments, please see:
[cdp-backend](https://github.com/councildataproject/cdp-backend)

For contributions to the web application which is used by all CDP deployments, please
see: [cdp-frontend](https://github.com/councildataproject/cdp-frontend)

For contributions to the existing event scrapers used by some CDP deployments, please
see: [cdp-scrapers](https://github.com/councildataproject/cdp-scrapers)

## Get Started!

Ready to contribute? Here's how to set up `cookiecutter-cdp-deployment` for local development.

1. Fork the `cookiecutter-cdp-deployment` repo on GitHub.

2. Clone your fork locally:

    ```bash
    git clone git@github.com:{your_name_here}/cookiecutter-cdp-deployment.git
    ```

3. Install `cookiecutter`. (It is also recommended to work in a virtualenv or anaconda environment):

    ```bash
    cd cookiecutter-cdp-deployment/
    pip install cookiecutter
    ```

4. Create a branch for local development:

    ```bash
    git checkout -b {your_development_type}/short-description
    ```

    Ex: feature/read-tiff-files or bugfix/handle-file-not-found<br>
    Now you can make your changes locally.

5. When you're done making changes, check that the cookiecutter still generates
   properly:

    ```bash
    cookiecutter . --no-input
    ```

6. Commit your changes and push your branch to GitHub:

    ```bash
    git add .
    git commit -m "Resolves gh-###. Your detailed description of your changes."
    git push origin {your_development_type}/short-description
    ```

7. Submit a pull request through the GitHub website.
