### Zip-project
## prerequirement
    1. [docker](https://docs.docker.com/engine/install/) 
    2. [docker-compose](https://docs.docker.com/compose/install/)
    
## After cloning the project, please follow the setup steps
    $ cp .template.env .env
    $ cd zipproject
    $ docker-compose build
    $ docker-compose up -d

## Database create table schema
    $ docker-compose exec backend bash
    $ alembic upgrade head
    $ exit

## Check the db
    $ docker-compose exec db bash
    $ psql -h localhost zipproject -U develop
    $ \dt # check the db relation

## Run unittest
    $ docker-compose exec backend bash
    $ python -m unittest test/test_users.py

## Shut down docker-compose
    $ docker-compose stop
    $ docker-compose down

## Useful commend
    $ docker system prune #clean the system cached data
    $ docker-compose logs -f backend #check backend log
