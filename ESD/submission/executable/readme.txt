IS213 ESD
G2T4 Carma

The repository contains the following directories.
	docker 	- contains the source files, dockerfiles and docker-compose file used to build the containers
	html 	- contains the frontend html files
	sql 	- contains sample data for the solution

Importing data:
Import the sample data for the solution using the sql files found in the sql folder.

To build the solution:
Run docker-compose.yml file in the docker directory using "docker-compose build" then "docker-compose up"

Import the services and routes to Kong:
Open localhost:1337 and import the snapshot "KONGAsnapshot"

To make payment, login to the following sandbox account:
username: sb-3xvvm1197041@personal.example.com
password: jV6F3*5#