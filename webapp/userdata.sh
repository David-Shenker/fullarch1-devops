#!/bin/bash
sudo yum update
sudo yum install -y git python3 python3-pip
python3 -m pip install flask flask-wtf pymongo boto3 flask-bootstrap

git clone https://github.com/David-Shenker/fullarch1-devops.git

cd fullarch1-devops/webapp

python3 app.py --mongo_uri 'mongodb://root:password@3.218.164.166:27017' \
              --s3_bucket myapp-photos-davshe \
              --aws_region us-east-1 \
              --secret_key 123123123
