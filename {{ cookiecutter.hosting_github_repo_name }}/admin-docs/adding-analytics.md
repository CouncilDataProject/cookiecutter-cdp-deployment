# Adding Analytics

Council Data Project is setup with [Plausible Analytics](https://plausible.io/about)
by default.

## CDP Org Hosted Instances

If your CDP instance is hosted under the "councildataproject.org" domain,
you shouldn't have to change anything from the default cookiecutter settings
as the `data-domain` value for the Plausible Analytics script in `web/public/index.html`
should be set to `councildataproject.github.io` for you.

If it isn't however, please update the `data-domain` value to `councildataproject.github.io`.

Once done, the analytics for your CDP instance should be publicly available on our
[Plausible Dashboard](https://plausible.io/councildataproject.github.io?page=%2F{{ cookiecutter.municipality_slug }}%2F**).

## Self Hosted Instances

If you want to use a different analytics platform or service,
simply replace the Plausible Analytics script in `web/public/index.html` with the service
of your choosing and setup the rest as you normally would.
