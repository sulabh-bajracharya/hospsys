# Hospsys

### Pre-requisites
1. Install Postgresql.
2. Install redis. (required for websockets)


### Database Configuration
1. Create role with createdb permissions.
2. Go to postgres command line with psql.
3. Create database `hospsys_development`.
4. Create postgres configuration file in home folder with host, user, password, dbname and port credentials.
5. Create .pgpass file with postgres login credentials in home folder.
6. Instead of steps 4 & 5, alternately follow the steps in https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-DATABASES


### Project Configuration
1. Create a folder and clone the repo into that folder.
2. Create python virtual environment using virtualenv inside the folder.
3. Go to project root folder containing requirements.txt file.
4. Install project requirements using `pip install -r requrements.txt`.
5. Apply migrations using `python manage.py migrate`.
6. Run the project using `python manage.py runserver`.

