worker_ip="10.0.1.58"
worker_port="8000"

aws lambda update-function-configuration --function-name new-job-controller --environment "Variables={worker_ip=${worker_ip},worker_port=${worker_port}}"