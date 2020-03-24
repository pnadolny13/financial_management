### Irma Janes - Docket App

# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

- To start the Docker containers - The current code is mounted to the container so the current code overwrites the code that was copied in when we built the image:
* `docker-compose -f docker-compose.yml up -d --build`

* `docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput`

- View at http://0.0.0.0:8000/admin 
- View at http://0.0.0.0:8000/docket/

* `docker-compose -f docker-compose.yml down -v`


#### In Prod:
##### Note: the .env.prod files need to be populated with prod credentials and database before startup (these files are in the git ignore so that prod creds dont go on github)

* `docker-compose -f docker-compose.prod.yml up -d --build`
* `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`
* `docker-compose -f docker-compose.prod.yml down -v`

- View at http://0.0.0.0:1337/admin
- View at http://0.0.0.0:1337/docket 


#### Deployment:
##### This builds the prod docker images, packages them as tar files, pushes to the server, unpacks the tar files, pushes compose and env.prod files, then executes docker-compose up on the server.

* `make deploy HOST=[EC2_PUBLIC_IP]`


Turn on RDS Instance, add user/pass/host to .env.prod file, run migration
Turn on EC2 instance, install docker and docker-compose
Run deploy make command with ip address parameter

#### Server Init:
##### This initializes a new server with docker and docker-compose so the deployment script will succeed.

* `make init_server HOST=[EC2_PUBLIC_IP]`
