deploy:
	docker-compose -f docker-compose.prod.yml build
	sh ./deploy.sh ${HOST}

init_server:
	scp ./init_server.sh ec2-user@${HOST}:/home/ec2-user/init_server.sh
	ssh ec2-user@${HOST} "sh /home/ec2-user/init_server.sh"

docker_up:
	docker-compose -f docker-compose.yml up -d --build

docker_down:
	docker-compose -f docker-compose.yml down -v

docker_logs:
	docker-compose logs -f

migration:
	docker-compose exec web python manage.py makemigrations ${APP}
	docker-compose exec web python manage.py migrate ${APP}

create_admin_user:
	docker-compose -f docker-compose.yml exec web python manage.py createsuperuser