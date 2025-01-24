# keep in sync with: https://github.com/kitconcept/buildout/edit/master/Makefile
# update by running 'make update'
SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

version = 3.9

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

all: build-plone-6.0

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.installed.cfg: bin/buildout *.cfg
	bin/buildout

bin/buildout: bin/pip
	bin/pip install --upgrade pip
	bin/pip install -r requirements.txt
	bin/pip install pip install black==$$(awk '/^black =/{print $$NF}' versions.cfg)
	@touch -c $@

bin/python bin/pip:
	python$(version) -m venv . || virtualenv --python=python$(version) .

build-plone-6.0:  ## Build Plone 6.0
	python$(version) -m venv .
	bin/pip install --upgrade pip
	bin/pip install -r requirements-6.0.txt
	bin/pip install pip install black==$$(awk '/^black =/{print $$NF}' versions.cfg)
	bin/buildout -c plone-6.0.x.cfg

.PHONY: Test
test:  ## Test
	bin/test

.PHONY: Test Performance
test-performance:
	jmeter -n -t performance.jmx -l jmeter.jtl

.PHONY: Code Analysis
code-analysis:  ## Code Analysis
	bin/code-analysis
	if [ -f "bin/black" ]; then bin/black src/ --check ; fi

.PHONY: Black
black:  ## Black
	bin/code-analysis
	if [ -f "bin/black" ]; then bin/black src/ ; fi

.PHONY: Build Docs
docs:  ## Build Docs
	bin/sphinxbuilder

.PHONY: Test Release
test-release:  ## Run Pyroma and Check Manifest
	bin/pyroma -n 10 -d .

.PHONY: Release
release:  ## Release
	bin/fullrelease

.PHONY: Clean
clean:  ## Clean
	git clean -Xdf

.PHONY: all clean
