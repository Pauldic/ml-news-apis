# ml-news-apis

# Requirement
* Python 3.7 
* Django 3+
* Postgres 12+

# Installation

# Ubuntu

* Clone Project
```bash
$ git clone git@gitlab.com:ml-news-platfrom/ml-news-apis.git
$ cd ml-news-apis
```

* First create Environment : 

```bash
$ sudo apt-get install python-virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cd api
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

# Env 
```bash 
SECRET_KEY='xg_#+0q0!95dzz2%er%jnfq646q9jv*xk1dsvcxsu$(+g@j)nf'
DEBUG = 'True'
ALLOWED_HOSTS = ['*']
POSTGRES_DB_NAME='mlnewsdb'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='nuTho8riChefoh4l'
POSTGRES_HOST='128.199.202.186'
POSTGRES_PORT='5432'
```

# Running On Docker

You must bring up the news-feed docker container (https://gitlab.com/ml-news-platfrom/ml-news-feed/-/tree/staging-server/), before running this one. So we will have:
- docker network ml
- docker container flask
- OPTIONAL: docker container ml-postgres (if you configured to use local postgres container)

Edit the docker-compose.yml to change the django port or other environment variable, please notice that:
- SECRET_KEY cannot contain $ (dollar sign), since docker-compose is not accepting it.
- The environment variables about postgres must be the same with ones in news-feed 's docker-compose.yml file. So they will contact to same container.

Build the docker image:

```bash
docker-compose build
#You need to re-run this command each time you pull a new code.
```

Bring up the docker-container and access on the port you set on docker-compose.yml file
```bash
docker-compose up -d
```