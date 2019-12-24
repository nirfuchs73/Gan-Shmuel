USE db

INSERT INTO providers (providername) VALUES ('Tapuzina');
INSERT INTO providers (providername) VALUES ('Herut');
INSERT INTO providers (providername) VALUES ('Mishmeret');
INSERT INTO providers (providername) VALUES ('KfarHess');

INSERT INTO containers (id,weight,unit) VALUES ('K-8263',666,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-7854',854,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-6523',741,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-2369',120,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-7845',999,'lbs');

INSERT INTO products (product_name,rate,scope) VALUES ('Blood',122,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Mandarin',103,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Navel',97,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Blood',102,'1');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',100,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Tangerine',80,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',90,'2');

INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('77777',2,666,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66666',2,120,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('99888',1,999,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66321',3,741,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('12365',4,854,'lbs');


USE billdb

INSERT INTO Trucks (id,provider_id) VALUES ('77777',2);
INSERT INTO Trucks (id,provider_id) VALUES ('66666',2);
INSERT INTO Trucks (id,provider_id) VALUES ('99888',1);
INSERT INTO Trucks (id,provider_id) VALUES ('66321',3);
INSERT INTO Trucks (id,provider_id) VALUES ('12365',4);

INSERT INTO Provider VALUES (1,'Tapuzina');
INSERT INTO Provider VALUES (2,'Herut');
INSERT INTO Provider VALUES (3,'Mishmeret');
INSERT INTO Provider VALUES (4,'KfarHess');

