WORK_DIR=`pwd`/../worker
DOCKER_IMAGE=python:3.7

docker run \
    --rm \
    --init \
    --platform linux/amd64\
    -v $WORK_DIR:/dot \
    --entrypoint /bin/bash \
    $DOCKER_IMAGE \
    -c 'pip install --upgrade pip --quiet &&\
        pip install virtualenv --quiet &&\
        virtualenv /dot/virt &&\
        . /dot/virt/bin/activate &&\
        pip install -r /dot/requirements.txt --quiet &&\
        rm /dot/virt/bin/python &&\
        ln -s /var/app/venv/staging-LQM1lest/bin/python /dot/virt/bin/python'
