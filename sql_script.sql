CREATE TABLE members(
	member_id INTEGER PRIMARY KEY NOT NULL,
	username VARCHAR(20) NOT NULL,
	password VARCHAR(20) NOT NULL,
	email VARCHAR(80),
	fullname VARCHAR(40) NOT NULL,
	address TEXT,
	phone INTEGER
);

CREATE TABLE product (
	product_id INTEGER PRIMARY KEY NOT NULL,
	product_name VARCHAR(50) NOT NULL,
	product_type VARCHAR(50),
	description TEXT,
	stock INTEGER NOT NULL,
	price INTEGER NOT NULL,
	img_source VARCHAR
);

CREATE TABLE rating (
	rating_id INTEGER PRIMARY KEY NOT NULL,
	member_id INTEGER,
	product_id INTEGER,
	value INTEGER NOT NULL,
	FOREIGN KEY (member_id) REFERENCES members(member_id),
	FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE transactions (
	transaction_id INTEGER PRIMARY KEY NOT NULL,
	member_id INTEGER,
	product_id INTEGER,
	quantity INTEGER NOT NULL,
	approval_status INTEGER NOT NULL CHECK(approval_status IN (0,1)),
	FOREIGN KEY (member_id) REFERENCES members(member_id),
	FOREIGN KEY (product_id) REFERENCES product(product_id)
);


CREATE TABLE comment (
	comment_id INTEGER NOT NULL PRIMARY KEY,
	member_id INTEGER,
	product_id INTEGER,
	comment TEXT
);

CREATE TABLE cart (
	cart_id INTEGER NOT NULL PRIMARY KEY,
	product_id INTEGER,
	member_id INTEGER,
	quantity INTEGER,
	FOREIGN KEY (product_id) REFERENCES product(product_id),
	FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- INSERT INTO product (product_id,product_name,product_type,description,stock,price,img_source)
-- 	VALUES (1111,'tshirt','cloths','half sleeves tshirt',20,600,'https://faketshirt.com')