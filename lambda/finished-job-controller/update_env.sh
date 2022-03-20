bucket="pdf-slicer"
dir="ready/"

aws lambda update-function-configuration --function-name finished-job-controller --environment \
"Variables={bucket=${bucket},dir=${dir}}"