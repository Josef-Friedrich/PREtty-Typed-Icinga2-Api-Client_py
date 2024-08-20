docker_start:
	sudo chmod -R 777 ./resources/etc-icinga2
	sudo docker run \
		--name icinga-master \
		--volume ./resources/etc-icinga2:/data/etc/icinga2 \
		--hostname icinga-master \
		--publish 5665:5665 \
		--env ICINGA_MASTER=1 \
		--detach \
		icinga/icinga2
	sleep 5
	sudo docker logs icinga-master

docker_stop:
	-sudo docker stop icinga-master
	-sudo docker rm icinga-master

.PHONY: docker_start docker_stop
