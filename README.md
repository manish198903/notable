# Notable Backend Challenge

## pre-requisites
- need to install docker-compose
  - https://docs.docker.com/compose/install/
  
## execution
- to run the api
  - `docker-compose up --build`
  - api should be available on http://0.0.0.0:5000
  - this runs a python flask web api with a mysql db on the host in a isolated docker network
- to shutdown
  - `docker-compose down`


