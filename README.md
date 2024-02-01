Task 1 Instructions:

1.1. Setup MongoDB with Docker Compose
Use Docker Compose to set up a MongoDB database.

1.2 Data Retrieval and Loading into MongoDB
Retrieve data from the JSONPlaceholder - Free Fake REST API and store it in MongoDB with python.

1.3 Create a RESTful API with FastAPI
Develop a FastAPI application to provide access to the mongo data. Include an endpoint to report the total number of posts and comments for each user.

Steps Taken:
1.1:

1. Create Docker Compose file, pull official mongo image from docker hub. create container_name and ports as well as environment. You can also use .env file
2. docker-compose up -d

1.2:
1. activate venv => on windows: venv/scripts/activate
2. pip install pymongo requests
3. Create script dataReceiveStore that
   - connect to DB
   - retrieve data
   - insert into DB
4. python3 dataReceiveStore.py script

1.3
1. pip install fastapi uvicorn python-dotenv
2. create fastAPI application, connects to DB and defines endpoints. runs server
3. python3 main.py

Reflections/improvements

- maybe use .env file to keep secrets safe when uploading to github

How to see inside the database within the container:

1. docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb
2. docker exec -it mongodb sh then mongosh --host 172.19.0.2

Easier way:
1. docker exec -it mongosh
2. use admin
3. db.auth("username", "password")
4. show dbs
5. use database_name
6. show collections