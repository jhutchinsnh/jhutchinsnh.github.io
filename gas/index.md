### README

[gas.py](https://github.com/jhutchinsnh/jhutchinsnh.github.io/tree/master/gas) requires Python 3.6+ and `mysql-connector-python`.

To run the MySQL container, first modify docker-compose.yml to mount its volume in a preferred location. If using Windows, run the following before modifying the location:

	SET COMPOSE_CONVERT_WINDOWS_PATHS=1

To start the Docker container:

	docker-compose up -d

To build the database with initial contents:

	cat finals.sql | docker exec -i gas_mysql_1 /usr/bin/mysql -u root --password=root zoo

To dump the current database via Docker:

	docker exec gas_mysql_1 /usr/bin/mysqldump -u root --password=root zoo > finals.sql

### About this project

The gas.cpp project was created for CS-405, Secure Coding. As part of the curriculum, we were provided with a simulation of a gas utility company’s command line interface, and performing a code audit for errors, security holes, and other mistakes. The majority of the code was rife with problems, from logic errors to programming errors to simple pointless code (e.g. memory manipulation on variables that were not called elsewhere and performed no work). In the end, while the program itself couldn't actually compile, it was a useful exercise in providing an executive summary and identifying problems, as opposed to actually fixing the mistakes.

I chose this program for the Algorithm and Data Structures artifact as an example of porting code from an existing project to a new language, allowing for fundamental rewrites of bad code and a "clean slate" for the updated project. Legacy code and accumulated work in the backlog can be daunting, so a total rewrite (especially in the case of such poorly-written code) can sometimes be warranted, time and resources permitting. Changing the data structures from baseline C++ into Python with its built-in support for strings and dictionaries, and cleaning out the nonsensical algorithms, made this an excellent choice for the second enhancement.

Rewriting the project in Python has met my expectations, both for workload and for improvements over the original project. Determining the flow of the program without the aid of any real commentary or flowchart was difficult; since the original code doesn’t compile, it’s not possible to just run it and see what happens, so I had to follow the logic within the code to determine which calls were performed where. I also adjusted my usual programming techniques in Python to more closely match the original project’s layout; instead of placing everything in a single Python file, I replicated the different modules in gas.cpp and wrote them to resemble the intent of the original project. I also created a separate Login.py to simulate a security plugin for testing passwords and password strength. Lastly, I decided to switch from CSV to a dockerized MySQL instance, as I did in Monitoring System.
