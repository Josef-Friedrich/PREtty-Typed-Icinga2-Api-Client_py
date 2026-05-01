# Run all recipes
all: upgrade docker_stop docker_start test format docs lint type_check chown_config_file patch_config_files

# Execute the tests
test:
	uv run --isolated --python=3.12 pytest
	uv run --isolated --python=3.13 pytest
	uv run --isolated --python=3.14 pytest

# Execute the quick tests
test_quick:
	uv run --isolated --python=3.12 pytest

# Install the dependencies (alias of upgrade)
install: upgrade

# Install the editable package based on the provided local file path
install_editable: install
	uv pip install --editable .

# Upgrade the dependencies
upgrade:
	uv sync --upgrade

# Upgrade the dependencies (alias of upgrade)
update: upgrade

# Build Python packages into source distributions and wheels
build:
	uv build

# Upload distributions to an index
publish:
	uv build
	uv publish

# Run ruff format
format:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format

# Build the documentation
docs: docs_readme_patcher docs_sphinx

# Generate the README file using the readme-patcher
docs_readme_patcher:
	uv tool run --isolated --with . --no-cache readme-patcher

# Generate the HTML documentation using Sphinx
docs_sphinx:
	rm -rf docs/_build
	uv tool run --isolated --no-cache --from sphinx --with . --with sphinx_rtd_theme --with sphinx-argparse --with sphinx-tags sphinx-build -W -q docs docs/_build
	xdg-open docs/_build/index.html

# Pin the requirements for readthedocs
pin_docs_requirements:
	rm -rf docs/requirements.txt
	uv run pip-compile --strip-extras --output-file=docs/requirements.txt docs/requirements.in pyproject.toml

# Run ruff check
lint:
	uv tool run ruff check --fix

# Perform type checking using mypy
type_check:
	uv run mypy src/pretiac tests

docker_start:
	sudo chmod -R 777 ./resources/etc-icinga2
	sudo docker run \
		--name icinga-master \
		--volume ./resources/etc-icinga2:/data/etc/icinga2 \
		--hostname icinga-master \
		--publish 5665:5665 \
		--env ICINGA_MASTER=1 \
		--detach \
		--rm \
		icinga/icinga2
	sleep 3
	sudo docker logs icinga-master
	# sleep 1
	# sudo docker exec icinga-master /usr/sbin/icinga2 daemon -C

docker_stop:
	-sudo docker stop icinga-master
	-sudo docker rm icinga-master

docker_login:
	sudo docker exec -it icinga-master /bin/bash

docker_create_api_certs:
	# https://icinga.com/blog/2022/11/16/authenticating-icinga-2-api-users-with-tls-client-certificates/

	sudo docker exec icinga-master /usr/sbin/icinga2 pki new-cert \
		--cn my-api-client \
		--key /data/my-api-client.key.pem \
		--csr /data/my-api-client.csr.pem

	sudo docker exec icinga-master /usr/sbin/icinga2 pki sign-csr \
		--csr /data/my-api-client.csr.pem \
		--cert /data/my-api-client.cert.pem

	sudo docker cp icinga-master:/var/lib/icinga2/certs/ca.crt .
	sudo docker cp icinga-master:/data/my-api-client.cert.pem .
	sudo docker cp icinga-master:/data/my-api-client.key.pem .

	sudo chown jf:jf ca.crt
	sudo chown jf:jf my-api-client.cert.pem
	sudo chown jf:jf my-api-client.key.pem

	curl \
		--cacert ca.crt \
		--cert my-api-client.cert.pem \
		--key my-api-client.key.pem \
		--header 'Accept: application/json' \
		--insecure \
		'https://localhost:5665/v1/?pretty=1'

docker_rmi:
	sudo docker rmi icinga/icinga2

set script-interpreter := ['uv', 'run', '--script']

# Own the resources folder by “jf”
chown_config_file:
	sudo chown -R jf:jf resources

# Patch the config files resources/etc-icinga2/constants.conf and resources/etc-icinga2/zones.conf to avoid noise in the commit messages
[script]
patch_config_files:
	from pathlib import Path
	import re

	CONSTANTS = Path("resources/etc-icinga2/constants.conf")
	OLD_LINE = r'const TicketSalt = ".*"'
	NEW_LINE = 'const TicketSalt = "7d65c57877b73e0df7fccb1cc43c3ee3"'
	content = CONSTANTS.read_text(encoding="utf-8")

	if re.search(OLD_LINE, content) is None:
		raise SystemExit(f"Expected line not found in {CONSTANTS}")

	updated = re.sub(OLD_LINE, NEW_LINE, content)
	CONSTANTS.write_text(updated, encoding="utf-8")
	print(f"Updated {CONSTANTS}")

	ZONES = Path("resources/etc-icinga2/zones.conf")
	OLD_LINE = r' \* on .*\n'
	NEW_LINE = ' * on 2026-04-30 20:36:53 +0000\n'
	content = ZONES.read_text(encoding="utf-8")

	if re.search(OLD_LINE, content) is None:
		raise SystemExit(f"Expected line not found in {CONSTANTS}")

	updated = re.sub(OLD_LINE, NEW_LINE, content)
	ZONES.write_text(updated, encoding="utf-8")
	print(f"Updated {ZONES}")
