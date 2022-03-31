worker_ip="pdf-worker.us-east-1.elasticbeanstalk.com"

aws lambda update-function-configuration --function-name new-job-controller --environment "Variables={worker_ip=${worker_ip}}"