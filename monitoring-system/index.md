## README

Modify docker-compose.yml to mount its volume in a preferred location. If using Windows, run the following before modifying the location:

	SET COMPOSE_CONVERT_WINDOWS_PATHS=1

To start the Docker container:

	docker-compose up -d

To build the database with initial contents:

	cat finals.sql | docker exec -i monitoringsystem2_mysql_1 /usr/bin/mysql -u root --password=root zoo

To dump the current database via Docker:

	docker exec monitoringsystem2_mysql_1 /usr/bin/mysqldump -u root --password=root zoo > finals.sql

## About this project

The Zoo Monitoring System project was created for IT-145, Foundation in Application Development. The purpose of the project was to create a program described by a fictional zoo, which would allow the employees to more easily monitor the animals and their habitats. The project required finding a way to take existing data (essentially handwritten notes) and consume it, then allow the user to choose options from a menu to learn more about a specific entry. It was also required to provide a pop-up window alerting staff to potential problems with either the animals or their habitats, e.g. cleaning requirements or health issues.

I chose this program for the Databases as an example of taking disparate data and converting it into a useful form, in this case from the original notes to CSV to, eventually, MySQL. The original Java program was also suboptimal in terms of layout and data ingestion (given the way basic FileInputStream, Scanner, and arrays work). This is more easily approached with a standard database application than a CSV. Additionally, learning how to dockerize projects in part or in whole is very useful to my current field, so this was good practice.

In terms of challenges and learning, I didn’t know that Python was capable of creating pop-up windows at all, especially when the application itself is CLI. I needed to use Python 3.6.2 for this project, which is outside my usual area of expertise (all of my production systems at work rely on 2.7.6). Adjusting to the slight differences, e.g. the different requirements for print statements, has been useful to learn. Likewise, while I’ve used Docker quite a bit in Linux, I haven’t needed to run it in a Windows host environment, and I was curious to see what roadblocks or techniques I’ll discover as I try to port this simple program and a MySQL database to virtual containers. I hadn't used Windows Powershell extensively until now, so it was a good lesson in the updated tools available to Windows environments.
