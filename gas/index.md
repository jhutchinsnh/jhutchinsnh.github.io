## gas.py

Modify docker-compose.yml to mount its volume in a preferred location. If using Windows, run the following before modifying the location:
        `SET COMPOSE_CONVERT_WINDOWS_PATHS=1`

To start the Docker container:
        `docker-compose up -d`

To build the database with initial contents:
        `cat finals.sql | docker exec -i gas_mysql_1 /usr/bin/mysql -u root --password=root zoo`

To dump the current database via Docker:
        `docker exec gas_mysql_1 /usr/bin/mysqldump -u root --password=root zoo > finals.sql`