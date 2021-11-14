#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cdp_backend.infrastructure import CDPStack
from pulumi import export

###############################################################################

cdp_stack = CDPStack(
    gcp_project_id="{{ cookiecutter.infrastructure_slug }}",
    municipality_name="{{ cookiecutter.municipality }}",
    firestore_location="{{ cookiecutter.firestore_region }}",
    hosting_github_url="{{ cookiecutter.hosting_github_url }}",
    hosting_web_app_address="{{ cookiecutter.hosting_web_app_address }}",
    governing_body="{{ cookiecutter.governing_body_type }}"
)

export("firestore_address", cdp_stack.firestore_app.app_id)
export("gcp_bucket_name", cdp_stack.firestore_app.default_bucket)
