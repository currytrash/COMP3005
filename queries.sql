

/* Browse / Display All books Query */
Select title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT title, 
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year
FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
group by src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year;


/* Search Query */

Select isbn,title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT isbn,title,
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year
FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by isbn,title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
where src.{}='{}'

group by src.isbn,src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year;

/* Search Query By Author  */

Select isbn,title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT isbn,title,
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year,author_first,author_last

FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by isbn,title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
where src.author_first ='{}' {} src.author_last='{}'

group by src.isbn,src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year,src.author_first,src.author_last;




/* New User */
insert into bookstore.user values + query);

/* Check Username in DataBase */
select * from bookstore.user where username = '" + userlgn + "';

/*Check Login Credentials */ 
select first_name, last_name, isAdmin from bookstore.user where username = '" + userlgn + "' and password = '" + pwlgn + "';

/* Check if user has basket  */
select count(*) from bookstore.user_basket where username = '{}';

/*Make basket */

insert into bookstore.basket values(Default);

/*Assign user to basket */
insert into bookstore.user_basket values + query ;

/* Check if user already has cc linked */
select count(*) from bookstore.user_cc where cc_number= '{}' and username = '{}';

/* Make Credit Card  */ 

insert into bookstore.cc values + query 

/* Assign Credit Card  To User*/ 

insert into bookstore.user_cc values + query 
/* Make Basket  */ 

/* Add Address */ 

insert into bookstore.address values(Default,'{}','{}','{}','{}','{}')""").format(
            addrname, addrnum, city, province, postal);"

/* Assign User to Address */ 
insert into bookstore.user_addr values + query 


/*Check if book exists to be deleted or added */
select count(*) from bookstore.book where isbn ='{}';

/* Delete Book */
delete from bookstore.book where isbn='{}'

/* Add Book */ 
insert into bookstore.book values + query ;

/* Check if Author exist */ 
select count(*) from bookstore.author where author_first = '{}' and author_last = '{}'

/*Add Author */ 
insert into bookstore.author values + query; 

/*Assign author to book*/ 
insert into bookstore.writes values + query 

/*Check if publisher exists */
select count(*) from bookstore.publisher where pub_name = '{}';

/* Add Publisher */
insert into bookstore.publisher values + query; 

/* Insert publishes */ 

insert into bookstore.publishes values + query; 


/* Select Basket */ 

select basket_id from bookstore.user_basket where username='" + currUser + "';

/* Add book to basket */ 
insert into bookstore.book_basket values

/*Update Quantity if book already exists in Book_Basket */ 

update bookstore.book_basket set quantity = quantity + Quantity + "WHERE isbn = '" + ISBN + "' AND basket_id = '" + basketID + "';");


/* View Basket */ 
select title,isbn,quantity,price,quantity*price as TOTAL from bookstore.book
        natural join bookstore.user_basket natural join bookstore.book_basket
        where username = '{}' and basket_id ='{}'
        group by title,book.isbn,user_basket.basket_id,book_basket.quantity;
		
/*Select CC by Index */ 
select  ROW_NUMBER () OVER (ORDER BY cc_number),cc_number,cc_first_name,cc_last_name from bookstore.cc natural join bookstore.user_cc
        where username = '{}';
		
/*Select Address */ 

select
        address_id,
        address_name,
        address_num,
        city,
        province,
        postal_code

        from bookstore.user_addr natural join bookstore.address where
        bookstore.user_addr.address_id = bookstore.address.address_id and username ='{}';
		
		
/* Make Order */ 
insert into bookstore.order values + query; 

/*Add Adress to order */ 

insert into bookstore.order_address values + query; 


/*Assign order to user */ 

nsert into bookstore.user_order values + query ;
 
 /*Assign cc to order */ 
 
 insert into bookstore.paid_with values + query ;
		
/*Delete Basket after checkout */ 
delete from bookstore.basket where basket_id = '{}').format(
            basketID);
			
/* Get Royalty and publisher name */ 
select royalty,pub_name from bookstore.publisher natural join bookstore.publishes natural join bookstore.book
where isbn = '{}' ;

/*Add Royalty fee to publisher account balance */ 
pdate bookstore.publisher set acc_balance = acc_balance + {} WHERE pub_name =  '{}';

/* Get Stock of book */ 
select stock from bookstore.book where isbn = '{}';

/*Update Stock */ 
update bookstore.book set stock = stock - {} where isbn = '{}';

/*Track order status */ 
select shipping_status from bookstore.order where tracking_num = '{}';



		
