.PHONY: help login init set-cors destroy gen-key
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

login: ## Run GCloud and Pulumi logins
	pulumi logout
	pulumi login
	gcloud auth login
	gcloud auth application-default login

init: ## Create google project and pulumi stack
	gcloud projects create cdp-example-annwruio --set-as-default
	pulumi stack init cdp-example-annwruio

set-cors: ## Set cors for the bucket
	gsutil cors set cors.json gs://cdp-example-annwruio.appspot.com/

destroy: ## Fully teardown Pulumi and GCloud
	pulumi stack rm cdp-example-annwruio --force
	gcloud projects delete cdp-example-annwruio
	rm -f .keys/cdp-example-annwruio.json

gen-key: ## Generate a service account JSON
	mkdir .keys/ -p
	gcloud iam service-accounts create cdp-example-annwruio \
    	--description="CDP Dev Service Account for $(USER)" \
    	--display-name="cdp-example-annwruio"
	gcloud projects add-iam-policy-binding cdp-example-annwruio \
    	--member="serviceAccount:cdp-example-annwruio@cdp-example-annwruio.iam.gserviceaccount.com" \
		--role="roles/owner"
	gcloud iam service-accounts keys create .keys/cdp-example-annwruio.json \
  		--iam-account "cdp-example-annwruio@cdp-example-annwruio.iam.gserviceaccount.com"