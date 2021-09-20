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
	gcloud projects create {{ cookiecutter.infrastructure_slug }} --set-as-default
	pulumi stack init {{ cookiecutter.infrastructure_slug }}

set-cors: ## Set cors for the bucket
	gsutil cors set cors.json gs://{{ cookiecutter.infrastructure_slug }}.appspot.com/

destroy: ## Fully teardown Pulumi and GCloud
	pulumi stack rm {{ cookiecutter.infrastructure_slug }} --force
	gcloud projects delete {{ cookiecutter.infrastructure_slug }}
	rm -f .keys/{{ cookiecutter.infrastructure_slug }}.json

gen-key: ## Generate a service account JSON
	mkdir .keys/ -p
	gcloud iam service-accounts create {{ cookiecutter.infrastructure_slug }} \
    	--description="CDP Dev Service Account for $(USER)" \
    	--display-name="{{ cookiecutter.infrastructure_slug }}"
	gcloud projects add-iam-policy-binding {{ cookiecutter.infrastructure_slug }} \
    	--member="serviceAccount:{{ cookiecutter.infrastructure_slug }}@{{ cookiecutter.infrastructure_slug }}.iam.gserviceaccount.com" \
		--role="roles/owner"
	gcloud iam service-accounts keys create .keys/{{ cookiecutter.infrastructure_slug }}.json \
  		--iam-account "{{ cookiecutter.infrastructure_slug }}@{{ cookiecutter.infrastructure_slug }}.iam.gserviceaccount.com"