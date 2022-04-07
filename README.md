# pdf-slicer

This is a project about pdf slicer and combiner


# Worker

### build and push

1. create credential file in the infra dir
2. `make updateworkerimage` in infra dir

### create venv for worker (normally you don't need it)
in case you want the venv build to upload, run `./build_worker_env.sh`, it will create venv in the `worker` dir

### deploying on the Beanstalk

*we assume that you are deploying the app in private subnet*

#### Docker
1. you will need to add file called `worker-docker.env` in the zip file with all the env var you want to have.
2. zip `docker-compose.yml` along with `worker-docker.env`
3. upload and run

#### Python
1. run `./build_worker_env.sh` for the venv
2. zip the dir called `virt` (the venv we just created) along with `.ebextensions` and py source code
3. upload and run

### Potential problems
1. credential problem inside the docker
   1. you will need to have the env vars in the `worker-docker.env` contains those three cretentials
2. beanstalk problem
   1. this is getting a bit more complicated
   2. Make sure that the IAM role you created have all the permissions to access related services
   3. Make sure that the subnet you created having needed AWS service endpoints
   4. Make sure you have the port exposed in the `docker-compose.yml` matching the port number configured in `dockerfile-worker`


# Lambda

### build and push
1. There are `deploy.sh`s in each lambda dir
2. run it after you have the local credential updated, it's fully automated
3. That's it ᕕ( ᐛ )ᕗ

### update env var
1. if you really have to, update and run `update_env.sh`
2. That's it again ᕕ( ᐛ )ᕗ


# Backend
It's similar to worker

### build and push

1. create credential file in the infra dir
2. `make updatebackendimage` in infra dir

#### Docker
Depending on frontend config since we are using docker compose to run two containers in one environment