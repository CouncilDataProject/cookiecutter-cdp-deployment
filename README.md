# CDP - Example

[![Infrastructure Deployment Status](https://github.com/CouncilDataProject/example/workflows/Infrastructure/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Infrastructure%22)
[![Event Processing Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Processing/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Processing%22)
[![Event Index Pipeline](https://github.com/CouncilDataProject/example/workflows/Event%20Index/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Event+Index%22)
[![Web Deployment Status](https://github.com/CouncilDataProject/example/workflows/Web%20App/badge.svg)](https://CouncilDataProject/github.io/example)
[![Repo Build Status](https://github.com/CouncilDataProject/example/workflows/Build%20Main/badge.svg)](https://github.com/CouncilDataProject/example/actions?query=workflow%3A%22Build+Main%22)

---

## CouncilDataProject

Council Data Project is an open-source project dedicated to providing journalists,
activists, researchers, and all members of each community we serve with the tools they
need to stay informed and hold their Council Members accountable.

For more information about CouncilDataProject, please visit
[our website](https://councildataproject.github.io/).

## Instance Information

This repo serves the municipality: **Example**

## Contributing

If you wish to contribute to CDP please note that the best method to do so is to
contribute to the upstream libraries that compose the CDP Instances themselves.
These are detailed below.

-   [cdp-backend](https://github.com/CouncilDataProject/cdp-backend): Contains
    all the database models, data processing pipelines, and infrastructure-as-code for CDP
    deployments. Contributions here will be available to all CDP Instances. Entirely
    written in Python.
-   [cdp-frontend](https://github.com/CouncilDataProject/cdp-frontend): Contains all of
    the components used by the web apps to be hosted on GitHub Pages. Contributions here
    will be available to all CDP Instances. Entirely written in
    TypeScript and React.
-   [cookiecutter-cdp-deployment](https://github.com/CouncilDataProject/cookiecutter-cdp-deployment):
    The repo used to generate new CDP Instance deployments. Like this repo!
-   [councildataproject.github.io](https://github.com/CouncilDataProject/councildataproject.github.io):
    Our landing page! Contributions here should largely be text changes and admin updates.
