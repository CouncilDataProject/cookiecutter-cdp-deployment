#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cdp_backend.infrastructure import CDPStack
from pulumi import export

###############################################################################

cdp_stack = CDPStack(gcp_project_id="cdp-example", firestore_location="us-west1")

export("firestore_address", cdp_stack.firestore_app.app_id)
export("gcp_bucket_name", cdp_stack.firestore_app.default_bucket)
