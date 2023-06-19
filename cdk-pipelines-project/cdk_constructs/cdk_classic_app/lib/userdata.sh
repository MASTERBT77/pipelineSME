#!/bin/bash
# yum update -y
# yum -y install httpd
# systemctl start httpd.service
# systemctl enable httpd.service
# echo "<h1>Hello world from $(hostname -f)</h1>" > /var/www/html/index.html
# 
# # enable port 8080
# sed -i 's/Listen 80/Listen 8080/g' /etc/httpd/conf/httpd.conf
# php para conectar a la aurora

# taggear a si mismo con el tag de byron
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
ID=`curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id`
aws ec2 create-tags --resources $ID --tags Key=DeploymentGroup,Value=BluAge

#reboot 