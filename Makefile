.PHONY: clean build gen-docs docs help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s: %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

update-from-cookiecutter: ## update this repo using latest cookiecutter-cdp-deployment
	cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment --config-file cookiecutter.yaml --no-input --overwrite-if-exists --output-dir ..