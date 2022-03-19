echo "Preparing credential file"
echo "[" > credentials.json
while IFS="" read -r p
do
    echo "{\"Namespace\": \"aws:elasticbeanstalk:application:environment\", \"OptionName\": \"$(echo $p | cut -d "=" -f 1)\", \"Value\": \"$(echo $p | cut -d "=" -f 2)\"}," >> credentials.json
done < worker-docker.env

last_line=$(grep "." worker-docker.env | tail -1)
echo "{\"Namespace\": \"aws:elasticbeanstalk:application:environment\", \"OptionName\": \"$(echo $last_line | cut -d "=" -f 1)\", \"Value\": \"$(echo $last_line | cut -d "=" -f 2)\"}" >> credentials.json

echo "]" >> credentials.json

echo "Uploading to EB"
aws elasticbeanstalk update-environment --environment-name Pdfworkerscale-env --option-settings file://credentials.json --region us-east-1 > /dev/null
rm credentials.json
echo "Configuration to EB finished"