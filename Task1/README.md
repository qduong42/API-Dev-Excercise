Build instructions:

1. Rename Task1/.env_Default to .env
2. change rootuser and rootpass to your desired mongodb root user and password
3. Run make with GNU Make 4.2.1 and python3 (with or without venv)installed.

```
make
```

- The makefile will detect if you have a .venv virtual env in your current directory, or it will use python3.
- It installs all required python packages then runs the dataReceiveStoreEnv.py then mainEnv.py which runs the server.

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
1. activate venv => on linux: venv/bin/activate
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

1.4
1. Configured env file to not have username/password in python file but in seperate .env file
2. Engineered mongo data aggregation pipeline.
3. Added checks to dataReceiveStoreEnv.py to prevent duplicated records
4. implemented makefile with commands make(all), clean, up, down
How to see inside the database within the container:

```
docker exec -it mongodb mongosh -u user -p password --authenticationDatabase admin
```
```
show dbs
```
```
use jsonplaceholder
```
```
show collections
```
```
show posts
```

### Reflections

- pip install could be done with -r requirements.txt file
- venv checking could be improved and supporting windows venv detection too. Currently only support linux .venv detection.
