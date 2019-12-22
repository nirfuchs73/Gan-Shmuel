docker run -d --name providers-db -v /home/geco/Gan-Shmuel/providers/db:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=12345678 mysql:8.0.18

echo "Created providers-db mysql container for the providers database password 12346578.\nUse: docker exec -it providers-db mysql -p12345678 to access from command line."
