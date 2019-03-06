Start project
---------------------------------------
1. Make sure you are connected to internet

2. Make sure you have Docker and Docker Compose

3. Start project:

    console# `docker-compose up`

4. After Up Docker container run in project directory:
    
    console# `./docker/bash.sh`

5. For run parser:

    bash# `python app.py`
    
6. If you want to run parser after Up container, uncomment this row in docker-compose.yml :

    `#      - RUN_PARSER=1`

