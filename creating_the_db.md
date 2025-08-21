#steps followed to create the db
1. Install the mysql server
2. Secure installation sudo mysql_secure_installation
3. Sudo mysql -u root -p
4. Create the db: create database ping_app
5. Create the mysql user and grant privileges: create user ‘ping_user’@‘%’ identified by ‘<pw>’; grant all privileges on ping_app.* to ‘ping_user’@‘%’; flush privileges; //% means user can connect from any host
6. Use ping_app;
7. Create table ping_counts( id int primary key, hit_counts int not null default 0, last_ip varcher(45) default null);
8. Insert into ping_counts (id, hit_counts) values (1,0,null);
9. Exit
