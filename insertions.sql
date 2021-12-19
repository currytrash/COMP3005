delete from bookstore.user;
delete from bookstore.cc;
delete from bookstore.author;
delete from bookstore.address;
delete from bookstore.publisher;
delete from bookstore.publishes;
delete from bookstore.book;
delete from bookstore.writes;


insert into bookstore.user values ('user','password','yahya','khan','yahyakhan@carleton.com','f');
insert into bookstore.user values ('admin','password','chia','liu','chialiu@carleton.com','t');

insert into bookstore.cc values ('5191230198336543','yahya','khan','1','1','564');
insert into bookstore.cc values ('5191230198339999','chia','liu','1','2','224');

insert into bookstore.user_cc values ('5191230198339999','admin');
insert into bookstore.user_cc values ('5191230198336543','user');



insert into bookstore.address values (Default,'Beatrice','210','Ottawa','Ontario','k2j5p2');
insert into bookstore.address values (Default,'Aura','40','Nepean','Ontario','k2s5j2');
insert into bookstore.address values  (Default,'HuntClub','250','Toronto','Ontario','k4s5p3');
insert into bookstore.address values  (Default,'Montreal Road','12','Montreal','Quebec','h7a5l3');

insert into bookstore.user_addr values ('1','user');
insert into bookstore.user_addr values ('2','user');
insert into bookstore.user_addr values  ('3','admin');
insert into bookstore.user_addr values  ('4','admin');




insert into bookstore.publisher values ('Penguin Canada','penguin@publishing.com','6135551234','100.00');
insert into bookstore.publisher values  ('Bloomsbury Childrens Books','bloomsburypub@publishing.com','6135431234','500.00');


insert into bookstore.book values ('0735240663','The Girl Who Lived Twice','Fantasy','448','12.86','5.25','10');
insert into bookstore.book values ('1526626586','Harry Potter and the Philosopher’s Stone','Non-Fiction','368','32.99','10.50','25');

insert into bookstore.publishes values ('Penguin Canada','0735240663','07','28','2020');
insert into bookstore.publishes values ('Bloomsbury Childrens Books','1526626586','11','10','2020');

insert into bookstore.author values ('J.K.','Rowling');
insert into bookstore.author values ('David','Lagercrantz');
insert into bookstore.author values ('George','Goulding');

insert into bookstore.writes values ('J.K.','Rowling','1526626586');
insert into bookstore.writes values ('David','Lagercrantz','0735240663');
insert into bookstore.writes values ('George','Goulding','0735240663');

