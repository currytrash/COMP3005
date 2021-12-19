-- SCHEMA: bookstore

-- DROP SCHEMA bookstore;

CREATE schema bookstore
    AUTHORIZATION postgres;

-- Entities

CREATE TABLE bookstore.user (
    username 	varchar(20),
    password 	varchar(20),
    first_name 	varchar(20),
    last_name 	varchar(20),
    email 		varchar(40),
    isAdmin		boolean,

    primary key (username)
);

CREATE TABLE bookstore.cc (
    cc_number 		varchar (16),
    cc_first_name	varchar (20),
    cc_last_name	varchar(20),
    month_exp		numeric(2,0),
    year_exp		numeric(2,0),
    cvv			numeric(3,0),

    primary key(cc_number)

);

CREATE TABLE bookstore.user_cc (
    cc_number 		varchar (16),
	username 		varchar(20),

    primary key(cc_number),
	foreign key(username) references bookstore.user(username)
		on delete cascade

);



CREATE TABLE bookstore.address (
    address_id	serial, 
    address_name 	varchar(20),
    address_num 	numeric(4,0),
    city 		varchar(20),
    province 	varchar(20),
    postal_code	varchar(6),
 
   primary key (address_id)
);

CREATE TABLE bookstore.user_addr (
    address_id 		serial,
	username 		varchar(20),

    primary key(address_id),
	foreign key (address_id) references bookstore.address(address_id)
		on delete cascade,
	foreign key(username) references bookstore.user(username)
	 on delete cascade
);



CREATE TABLE bookstore.publisher (
    pub_name 	varchar(400) ,
    email_add 	varchar(40) , 
    phone_num 	numeric(10,0) ,
    acc_balance numeric(10,2),


    primary key(pub_name)
);


CREATE TABLE bookstore.book (
    isbn 		varchar(10),
    title 		varchar(200),
	genre 		varchar(200),
    pages 	   	numeric (4,0) check (pages >0),
    price 		numeric(5,2),
	royalty     numeric(4,2),
    stock 		numeric (2,0) check (stock > 0),

    
    primary key (isbn)
    
);



CREATE TABLE bookstore.publishes (
    pub_name 	varchar(400) ,
    isbn 		varchar(10),
	pub_month   numeric(2,0) check (pub_month <=12 and pub_month>=1),
	pub_day		numeric(2,0) check (pub_month <=31 and pub_month>=1),
    pub_year 	numeric(4,0) check (pub_year < 2022),

    primary key(pub_name,isbn),
    foreign key (pub_name) references bookstore.publisher (pub_name)
        on delete cascade,
    foreign key (isbn) references bookstore.book(isbn)
        on delete cascade
);

CREATE TABLE bookstore.author (
    author_first 	varchar(20) not null,
    author_last 	varchar(20) not null,
  
 primary key (author_first, author_last)
);

CREATE TABLE bookstore.writes (
    author_first 	varchar(20),
    author_last 	varchar(20),
    isbn    		varchar(10), 
    
    primary key(author_first, author_last, isbn),
    foreign key (author_first, author_last) references bookstore.author
		(author_first, author_last)
		on delete cascade,
    foreign key(isbn) references bookstore.book (isbn)
        on delete cascade
);

CREATE TABLE bookstore.basket (
    basket_id	serial,
    
    primary key(basket_id)
    
);

CREATE TABLE bookstore.book_basket (
    basket_id 	serial,
	isbn		varchar(10),
	quantity    numeric(2,0),
    
    primary key(basket_id,isbn),
	foreign key(basket_id) references bookstore.basket(basket_id)
	on delete cascade,
	foreign key(isbn) references bookstore.book(isbn)
	on delete cascade
    
);

CREATE TABLE bookstore.user_basket (
    basket_id 	serial,
	username	varchar(20),
    
    primary key(basket_id),
	foreign key(basket_id) references bookstore.basket(basket_id)
		on delete cascade,
	foreign key(username) references bookstore.user(username)
		on delete cascade
    
);




CREATE TABLE bookstore.order (
	order_num			serial,
	tracking_num 		varchar(16),
	order_date			varchar(10),
	shipping_status		varchar(20),
	
	primary key(order_num)
);

CREATE TABLE bookstore.order_address (
	order_num			serial,
	address_id 			serial,
	isBilling			boolean,
	

	primary key (order_num, address_id,isBilling),
	foreign key (order_num) references bookstore.order(order_num),
	foreign key (address_id) references bookstore.address(address_id)
	
);

CREATE TABLE bookstore.user_order (
	order_num			serial,
	username 			varchar(20),
	

	primary key (order_num, username),
	foreign key (order_num) references bookstore.order(order_num),
	foreign key (username) references bookstore.user(username)
	
);

CREATE TABLE bookstore.paid_with (
	order_num			serial,
	cc_number 			varchar(16),
	

	primary key (order_num, cc_number),
	foreign key (order_num) references bookstore.order(order_num),
	foreign key (cc_number) references bookstore.cc(cc_number)
	
);







