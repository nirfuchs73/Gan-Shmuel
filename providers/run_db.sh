docker run -d --name providers-db -v $PWD/db:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=12345678 mysql:8.0.18 --default-authentication-plugin=mysql_native_password 

echo "Created providers-db mysql container for the providers database password 12346578.
      Use: docker exec -it providers-db mysql -p12345678 to access from command line."
