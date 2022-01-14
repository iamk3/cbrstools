# SPDX-FileCopyrightText: © 2021 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

# Use bash for pushd/popd, and to fail quickly.
# No -u as virtualenv activate script has undefined vars
SHELL = bash -e -o pipefail

.DEFAULT_GOAL := help
.PHONY: test lint pylint black blacken license help

PYTHON_FILES      ?= $(wildcard *.py)
SHELL_FILES       ?= $(wildcard *.sh)
CPI_KEY           ?= $(wildcard *.p12)


# tooling
VIRTUALENV        ?= python3 -m venv

# Create the virtualenv with all the tools installed
VENV_NAME = venv_cbrs

$(VENV_NAME): requirements.txt
	$(VIRTUALENV) $@ ;\
  source ./$@/bin/activate ; set -u ;\
  python -m pip install --upgrade pip;\
  python -m pip install -r requirements.txt
	echo "To enter virtualenv, run 'source $@/bin/activate'"

test: shellcheck black pylint license ## run tests

pylint: $(VENV_NAME) ## pylint check for best practices
	source ./$</bin/activate ; set -u ;\
  pylint --version ;\
  pylint $(PYTHON_FILES)

shellcheck:  ## shellcheck shell scripts
  # SC1091 is excluded which is soucing the venv
	shellcheck -V
	shellcheck -e SC1091 $(SHELL_FILES)

black: $(VENV_NAME) ## run black on python files in check mode
	source ./$</bin/activate ; set -u ;\
  black --version ;\
  black --check $(PYTHON_FILES)

blacken: $(VENV_NAME) ## run black on python files to reformat
	source ./$</bin/activate ; set -u ;\
  black --version ;\
  black $(PYTHON_FILES)

license: $(VENV_NAME) ## Check license with the reuse tool
	source ./$</bin/activate ; set -u ;\
  reuse --version ;\
  reuse --root . lint

clean:
	rm -rf $(VENV_NAME)

help: ## Print help for each target
	@echo cbrstools make targets
	@echo
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
    | sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'
