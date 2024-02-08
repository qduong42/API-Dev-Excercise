## Prerequisites
- Run on:
   - GNU Make 4.2.1  
   - python 3.8.10
- if using virtual environment on linux: python3.8-venv package
  ```
  sudo apt-get install python3.8-venv
  ```
   - official instructions: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

## Build instructions

1. git clone the repository
```
git clone https://github.com/qduong42/API-Dev-Excercise.git
```
2. Rename ```Task2/.env_Default``` to .env
3. change ```rootuser``` and ```rootpass``` to your desired mongodb root user and password
4. Run ```make``` with GNU Make 4.2.1 and python3.8.10 (with or without venv)installed.

```
make
```

- The Makefile tries to create a venv in the current directory if not already present with the name venv.
- If venv creation fails, it will use the system python3.
- It installs all required python packages then runs the dataReceiveStoreEnv.py then mainEnv.py which runs the server.

- Navigate to
```http://127.0.0.1:8000/docs``` for swagger documentation

- Example Usage: 
    - Turbine data from turbine 2
    - From 2016-03-01T00:30 to 2016-03-31T00:40
    - format: YYYY-MM-DDTHH:MM
    - turbine_id, start_time and end_time are all optional

```
http://localhost:8000/turbine_data?turbine_id=2&start_time=2016-03-01T00:30&end_time=2016-03-05T00:40
```
- If start time or end time is None: limit 1000 is arbitrarily placed to avoid large data output. This can be changed in the mainEnv.py file.

### Issues: 

- with dataReceiveStoreEnv.py
    - link given not to csv file
    - adding to collection only if unique
    - added indexing to turbine and Dat/Zeit since these two fields should be "unique". same turbine id and same time => document not added to record.

- with mainEnv.py
    - Serialization issue with big floats
        - second row contains units, not data. raised some parsing issues with NaN values and float. Parsed if units were to be needed later but skipped for data output.

### Technical Features:

- logging dataReceiveStoreEnv.py progress to terminal
- OS detection for python virtual environment creation, and activation and pip installation

### Features:

- Turbine ID, start and end time are all optional.
- If turbine ID is not given, both turbine data are considered.
- If start and end time are not given, all data is considered.
- if start time is given but not end time, all data from start time is considered.
- if end time is given but not start time, all data till end time is considered.

### Extensions/Reflections:
- build a frontend for easier user interaction in getting turbine data
- mongodb atlas for cloud storage
- mongodb UI for easier interaction with DB.
- date could be formatted better for consistency with csv data input
- better error handling for invalid input not just have uncaught internal server errors