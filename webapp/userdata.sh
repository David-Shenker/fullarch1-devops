#!/bin/bash
sudo yum update
sudo yum install -y git python3 python3-pip
python3 -m pip install flask flask-wtf pymongo boto3 flask-bootstrap

git clone https://github.com/David-Shenker/fullarch1-devops.git

python3 fullarch1-devops/webapp/app.py --mongo_uri 'mongodb://root:password@10.0.1.110:27017' \
              --s3_bucket myapp-photos-davshe \
              --aws_region us-east-1 \
              --secret_key 1123581321
