# Data Engineering Task

The package contains the library for pipeline operators and docker files to run as in container. 
The docker were run and test under Apple M1. To avoid any conflict, this demo will use docker from conda channel `conda-forge`

## Setup Docker
This initialize two containers `postgres_container` and `jupyter_container`
```
docker-compose up --build
```

### Start Demo
1. Open a link to jupyter lab
2. Open demo.ipynb
3. 

## Summary
The task is written in arround 3 days. More than 50% is to design the structure. 20 % handling on docker for M1 and remaining for coding in Python.