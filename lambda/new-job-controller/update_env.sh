worker_ip="Pdfworkerscale-env.eba-hmgwnnvq.us-east-1.elasticbeanstalk.com"
worker_port="8000"

aws lambda update-function-configuration --function-name new-job-controller --environment "Variables={worker_ip=${worker_ip},worker_port=${worker_port}}"