#!/bin/bash


if [[ `command -v docker` ]]
then
	docker image build -t barbershop .
	docker container run --publish 8000:8000 --detach --name bb barbershop
else
	printf "Docker must be installed.\n"
fi
