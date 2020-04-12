export APP := spend_tracker
export ADMIN_PASS := admin
export ENV := 

deploy:
	docker-compose -f docker-compose.prod.yml build
	sh ./deploy.sh ${HOST}

init_server:
	scp ./init_server.sh ec2-user@${HOST}:/home/ec2-user/init_server.sh
	ssh ec2-user@${HOST} "sh /home/ec2-user/init_server.sh"

docker_up:
	docker-compose -f docker-compose.${ENV}yml up -d --build

docker_down:
	docker-compose -f docker-compose.${ENV}yml down -v

docker_logs:
	docker-compose -f docker-compose.${ENV}yml logs -f

migration:
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py makemigrations
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py migrate
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py collectstatic --no-input --clear
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py makemigrations ${APP}
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py migrate ${APP}

load_data:
	docker-compose exec -u root web python manage.py loaddata ${APP}

create_user:
	docker-compose -f docker-compose.${ENV}yml exec -u root web python manage.py createsuperuser	
