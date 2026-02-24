#!/bin/bash
if [ -f /.dockerenv ]; then
   echo "You can not stop the development environment inside a docker container"
else
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    COMPONENT_ID="c2_treatment_nonmaleficence_valuator"
    DEV_CONTAINER_NAME="${COMPONENT_ID}_dev"
	pushd $DIR >/dev/null
	docker compose -f docker/dev/docker-compose.yml down
	if [ "$(docker container ls |grep $DEV_CONTAINER_NAME |wc -l)" -gt "0" ]
	then
		docker stop $DEV_CONTAINER_NAME
	fi
	popd >/dev/null
fi