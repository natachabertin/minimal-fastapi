# minimal-fastapi-template
Base repo for an easy start on simple prototypes, code challenges and non-productive projects

## Usage
* Clone this repo
* Implement the requirements and database
* Run the tests
* Modify what you need to start your prototype


## Executing the app

#### Run the backend server dockerized
##### Set up
1. Ensure you have Docker daemon/desktop running.
2. cd into `minimal-fastapi`.
3. Build the repo with `docker-compose up -d --build`.
4. You'll see app docs in [http://localhost:8000/docs](http://localhost:8000/docs).

##### Resume
1. Execute `docker-compose up`.
2. You'll see app docs in [http://localhost:8000/docs](http://localhost:8000/docs).

#### Run compose context and locally simultaneously
##### IDE setup for run and debugging
* Set `/backend` as source root in your IDE
* In the run configuration,
  * instead of script, select `module`and write `uvicorn`
  * Command: `main:app --reload` (you can add port and host, but ensure host is diff to Docker on is you wanna run them simultaneously).
  * Working dir: `D:\<my_path>\minimal-fastapi\backend\app`
  * Env file: `D:/<my_path>/minimal-fastapi/backend/.env`

