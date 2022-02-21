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
	gcloud projects create cdp-example-ryoozzsc --set-as-default
	pulumi stack init cdp-example-ryoozzsc

set-cors: ## Set cors for the bucket
	gsutil cors set cors.json gs://cdp-example-ryoozzsc.appspot.com/

destroy: ## Fully teardown Pulumi and GCloud
	pulumi stack rm cdp-example-ryoozzsc --force
	gcloud projects delete cdp-example-ryoozzsc
	rm -f .keys/cdp-example-ryoozzsc.json

gen-key: ## Generate a service account JSON
	mkdir .keys/ -p
	gcloud iam service-accounts create cdp-example-ryoozzsc \
    	--description="CDP Dev Service Account for $(USER)" \
    	--display-name="cdp-example-ryoozzsc"
	gcloud projects add-iam-policy-binding cdp-example-ryoozzsc \
    	--member="serviceAccount:cdp-example-ryoozzsc@cdp-example-ryoozzsc.iam.gserviceaccount.com" \
		--role="roles/owner"
	gcloud iam service-accounts keys create .keys/cdp-example-ryoozzsc.json \
  		--iam-account "cdp-example-ryoozzsc@cdp-example-ryoozzsc.iam.gserviceaccount.com"