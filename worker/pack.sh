pack_name=zipfile.zip

zip -g $pack_name docker-compose.yml
zip -g $pack_name worker-docker.env