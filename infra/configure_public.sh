IP=$1

echo "=== configuring public instance on $IP ==="
echo "*** configuration on $IP has finished ***"
make uppublic ip=$IP
make uppublic fromdir=Makefile ip=$IP
make uppublic fromdir=test_lambda.py ip=$IP




echo "=== configuration on $IP has finished ==="
