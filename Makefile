test: docker_stop docker_start test_all

test_all:
	poetry run tox

test_quick:
	poetry run tox -e py312

install: update

clear_poetry_cache:
	poetry cache clear PyPI --all --no-interaction
	poetry cache clear _default_cache --all --no-interaction

# https://github.com/python-poetry/poetry/issues/34#issuecomment-1054626460
# pip install --editable . # error: externally-managed-environment -> pipx
install_editable:
	pipx install --force --editable .

update: clear_poetry_cache
	poetry lock
	poetry install

build:
	poetry build

publish:
	poetry build
	poetry publish

format:
	poetry run tox -e format

docs:
	poetry run tox -e docs
	xdg-open docs/_build/index.html > /dev/null 2>&1

lint:
	poetry run tox -e lint

type_check:
	poetry run tox -e type-check

pin_docs_requirements:
	pipx install pip-tools
	pip-compile --output-file=docs/requirements.txt docs/requirements.in pyproject.toml

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
	sleep 1
	sudo docker logs icinga-master
	sleep 1
	sudo docker exec icinga-master /usr/sbin/icinga2 daemon -C

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


.PHONY: test install install_editable update build publish format docs lint pin_docs_requirements docker_start docker_stop
