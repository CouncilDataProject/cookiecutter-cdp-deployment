# list all available commands
default:
  just --list

# update this repo using latest cookiecutter-py-package
update-from-cookiecutter:
  pip install cookiecutter
  cookiecutter gh:CouncilDataProject/cookiecutter-cdp-deployment \
    --config-file cookiecutter.yaml \
    --no-input \
    --overwrite-if-exists \
    --output-dir ..