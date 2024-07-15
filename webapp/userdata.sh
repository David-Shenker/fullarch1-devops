#!/bin/bash

exec > /var/log/user-data.log 2>&1

sudo yum update -y
sudo yum install -y git python3 python3-pip

python3 -m pip install flask flask-wtf pymongo boto3 flask-bootstrap

git clone https://github.com/David-Shenker/fullarch1-devops.git /home/ec2-user/fullarch1-devops

sudo bash -c 'cat > /etc/systemd/system/flask_app.service << EOF
[Unit]
Description=A simple Flask app
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/fullarch1-devops/webapp
ExecStart=/usr/bin/python3 app.py --mongo_uri "mongodb://root:password@10.0.1.110:27017" --s3_bucket myapp-photos-davshe --aws_region us-east-1 --secret_key 1123581321
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl start flask_app
sudo systemctl enable flask_app

echo "User data script finished" >> /var/log/user-data.log
