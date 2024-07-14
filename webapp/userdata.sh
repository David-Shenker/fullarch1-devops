#!/bin/bash
sudo yum update
sudo yum install -y git python3 python3-pip
python3 -m pip install flask flask-wtf pymongo boto3 flask-bootstrap

git clone https://github.com/David-Shenker/fullarch1-devops.git

cd fullarch1-devops/webapp

python3 app.py --mongo_uri your_mongodb_uri \
              --s3_bucket myapp-photos-davshe \
              --aws_region us-east-1
