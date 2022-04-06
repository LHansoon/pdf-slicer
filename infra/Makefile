credpath ?= /Users/hanson/Documents/hansonawsacademy.pem

username = ec2-user

ip1public := 18.206.46.214
ip2internal := 10.0.1.73

.PHONY: priip, pubip, ssh
priip:
	@echo ${ip2internal}
pubip:
	@echo ${ip1public}


ssh:
	ssh -i "${credpath}" ec2-user@"${ip}"
ssh_through:
	ssh -o ProxyCommand='ssh -i '"${credpath}"' -W %h:%p ec2-user@'"${ip1}" -i "${credpath}" "ec2-user@${ip2}"

sshpublic: ip ?= ${ip1public}
sshpublic: ssh

sshprivate: ip1 ?= ${ip1public}
sshprivate: ip2 ?= ${ip2internal}
sshprivate: ssh_through



upfile: todir ?= /home/ec2-user
upfile: ip ?= ${ip1public}
upfile: fromdir ?= ${credpath}
upfile:
	scp -i ${credpath} ${fromdir} ec2-user@${ip}:${todir}

upfile_private: todir ?= /home/ec2-user
upfile_private: fromdir ?= ${credpath}
upfile_private: ip1 ?= ${ip1public}
upfile_private: ip2 ?= ${ip2internal}
upfile_private:
	scp -r -o ProxyCommand="ssh -i ${credpath} -W %h:%p ec2-user@${ip1}" -i ${credpath} ${fromdir} ec2-user@${ip2}:${todir}

upprivate: upfile_private
uppublic: upfile


configurepublic:
	@sh configure_public.sh ${ip1public}



# actual useful for WORKER

buildworker:
	@docker build --no-cache --platform linux/amd64 -t pdf-worker -f ../infra/dockerfile-worker ../worker/

pushworker:
	@aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 323940432787.dkr.ecr.us-east-1.amazonaws.com
	@docker tag pdf-worker 323940432787.dkr.ecr.us-east-1.amazonaws.com/pdf-worker:latest
	@docker push 323940432787.dkr.ecr.us-east-1.amazonaws.com/pdf-worker:latest

updatecredential:
	@cat aws_credential > ~/.aws/credentials

updateworkerimage: updatecredential buildworker pushworker

buildworkerenv:
	./build_worker_env.sh


# useful for backend

buildback:
	@docker build --no-cache -t pdf-backend -f ../infra/dockerfile-backend ../backend/

pushback:
	@aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 323940432787.dkr.ecr.us-east-1.amazonaws.com
	@docker tag pdf-backend 323940432787.dkr.ecr.us-east-1.amazonaws.com/pdf-backend:latest
	@docker push 323940432787.dkr.ecr.us-east-1.amazonaws.com/pdf-backend:latest

updatebackendimage: updatecredential buildback pushback


# useful for front end --platform linux/amd64
buildfront:
	@docker build --no-cache -t pdf-frontend -f ../infra/dockerfile-frontend ../front/pdf-slicer-ui

buildfront-express:
	@docker build --no-cache -t pdf-frontend-express -f ../infra/dockerfile-frontend-express ../front/frontend-server



updateall: updatecredential
	(cd ../worker && ./update_env.sh)
	(cd ../lambda/new-job-controller && ./update_env.sh)


#tar -czvf venv.tar.gz venv
#scp -i hansonawsacademy.pem venv.tar.gz ec2-user@10.0.1.254:/home/ec2-user

#tar -xzvf venv.tar.gz
#或者说这个也可以吧大概 tar -xf archive.tar -C /target/directory
