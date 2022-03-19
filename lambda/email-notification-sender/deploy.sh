# IMPORTANT: You MUST run the script in the lambda sub dir (ex. new-job-controller/)

pack_name="lambda-pack.zip"

echo Preparing the venv
python3 -m venv venv
./venv/bin/pip install -r requirements.txt --quiet

echo Packing up the zip
curr_dir=`pwd`
(cd venv/lib/python3.7/site-packages && zip -r $curr_dir/$pack_name .)
zip -g $pack_name lambda_function.py

echo Deleting the venv
rm -rf venv

aws lambda update-function-code --function-name email-notification-sender --zip-file fileb://$pack_name
rm $pack_name