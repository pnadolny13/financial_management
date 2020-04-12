#!/bin/bash

docker save -o web.tar web
scp web.tar ec2-user@$1:/home/ec2-user/
ssh ec2-user@$1 "docker load -i /home/ec2-user/web.tar"
rm web.tar

docker save -o nginx.tar nginx
scp nginx.tar ec2-user@$1:/home/ec2-user/nginx.tar
ssh ec2-user@$1 "docker load -i /home/ec2-user/nginx.tar"
rm nginx.tar

scp docker-compose.prod.yml ec2-user@$1:/home/ec2-user/docker-compose.prod.yml
scp .env.prod ec2-user@$1:/home/ec2-user/.env.prod

ssh ec2-user@$1 "docker-compose -f /home/ec2-user/docker-compose.prod.yml up -d; docker-compose -f /home/ec2-user/docker-compose.prod.yml exec -T web python manage.py collectstatic --no-input --clear;"
