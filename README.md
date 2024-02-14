# Steps to run the Server Locally
### Clone this repository
`git clone https://github.com/AbhilakshSinghReen/kaizntree-assignment-backend.git`

### Move into the project directoyr
`cd kaizntree-assignment-backend`

### Create a virtual environment and activate it
#### If using venv
> `python -m venv env`
>> On Windows: `env\Scripts\activate`
>>  On Linux/Mac: `source env/bin/activate`

#### If using conda
> `conda create -n env python=3.10`
> `conda activate env`

### Install the dependencies
`pip install -r requirements.txt`

### Make migrations and migrate
`python manage.py makemigrations`
`python manage.py migrate --run-syncdb`

### Run redis
Using docker
`docker run --name kaizntree-redis -d -p 6379:6379 redis:7.2.4-alpine`
It is possible to run redis without docker - if you have a redis server running locally, you can use that as well. However, for the purpose of a simple testing setup, I have gone with docker.

### Check if connection to redis can be established
`py manage.py test_redis`

### Seed the database
`python manage.py seed`

### Create a file for the environment variables
Rename .env.sample file to .env

### Run the server
`python manage.py runserver`
