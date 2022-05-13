# Corner Case Technologies

Internal cafe service

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ejaj/cornercasetech.git
$ cd cornercasetech
```

Then, active a virtual environment:

```sh
$ source venv/bin/activate
```

Create an .env file and paste all the variables from .env.keep file and set the value for them for example database
name, password, host etc.

## Run it on Docker machine.

Set a True value for DOCKER variable on env file.

```sh
DOCKER=True
```

Then run the blow command

```sh
docker-compose up -d --build
```

Then browse: http://127.0.0.1:8000/admin

For api's operation, you can see
[ api documentation doc](APIdocumentation.pdf)
````
## Run the project on localhost.

Set a blank value for DOCKER variable on env file.

```sh
DOCKER=
```

Then run these command.
For migrations
```sh
python manage.py migrate
```
For creating super user
```sh
python manage.py superuser
```

Run the tests case for model
```sh
python manage.py test restaurants/tests
```

For running project.
```sh
python manage.py runserver
```

Now you can browse: http://127.0.0.1:8000/admin

For api's operation, you can see
[ api documentation doc](APIdocumentation.pdf)

### Dependencies
```sh
- Database: PostgreSQL
```

NB: You can see the all kinds of log from project log folder.
