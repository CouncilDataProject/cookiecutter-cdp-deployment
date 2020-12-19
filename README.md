# CDP - Example

[![Infrastructure Deployment Status](https://github.com/CouncilDataProject/example/workflows/Infrastructure/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
[![Event Processing Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Processing/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Processing%22)
[![Event Index Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Index/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Index%22)
[![Web Deployment Status](https://github.com/CouncilDataProject/example/workflows/Web%20App/badge.svg)](https://CouncilDataProject.github.io/example)
[![Repo Build Status](https://github.com/CouncilDataProject/example/workflows/Build%20Main/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Build+Main%22)

---

## About

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

By combining and simplifying sources of information on Council meetings and actions,
CDP ensures that everyone is empowered to participate in local government.

This repo is an example of _a CDP instance_! Each municipality that CDP supports
(_a CDP instance_) has open source maintainers which write code to gather
municipality meeting information and compile them into a single resource to then be
processed, stored, and made accessible by our general CDP tooling.

## Instance Information

This repo serves the municipality: **Example**

## Contributing

If you wish to contribute to CDP please note that the best method to do so is to
contribute to the upstream libraries that compose the CDP instances themselves.
These are detailed below.

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

## Initial Repo Setup

-   [ ] Create a GitHub repo under the 'CouncilDataProject' account called 'example'
-   [ ] Turn on GitHub Pages for the `gh-pages` branch ([Repo Settings](https://github.com/CouncilDataProject/example/settings))
-   [ ] Write Python event gather function (`get_events`)
-   [ ] Add [GitHub Actions repository secrets](https://github.com/CouncilDataProject/example/settings/secrets/actions) for:
    -   [ ] Google Cloud (`GOOGLE_CREDENTIALS`)
    -   [ ] Pulumi (`PULUMI_ACCESS_TOKEN`)
