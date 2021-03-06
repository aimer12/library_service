sudo service mysql start
mysql -u root -p

----------------create database------------
create database library;
use  library;

----------------create tables---------------

---------create book-------------
create table book(
book_id    SMALLINT PRIMARY KEY AUTO_INCREMENT,
book_title VARCHAR(45)  NOT NULL,
author     VARCHAR(20),
publisher  VARCHAR(45),
description   TINYTEXT, 
addr VARCHAR(40) NOT NULL,
price  FLOAT(5,2)
)ENGINE=INNODB;



---------create reader-----------
create table reader(
reader_id   SMALLINT UNSIGNED KEY AUTO_INCREMENT,
reader_name VARCHAR(20) NOT NULL,
sex         ENUM('MAN','WOMEN'),
age         TINYINT UNSIGNED DEFAULT 18,
email       VARCHAR(40),
type        TINYINT(1) DEFAULT 0 
)ENGINE=INNODB;


---------create borrow-----------
create table borrow(
brw_id       SMALLINT KEY AUTO_INCREMENT,
bookid       SMALLINT NOT NULL,
readerid     SMALLINT UNSIGNED NOT NULL,
borrowdate   INT NOT NULL,
returndate   INT NOT NULL,
renew        TINYINT(1) default 0 COMMENT '0 unrenew ,1 renewed' ,
FOREIGN KEY(bookid) REFERENCES book(book_id),
FOREIGN KEY(readerid) REFERENCES reader(reader_id)   
)ENGINE=INNODB;

---------create admin-------------

create table admin(
admin_id   SMALLINT UNSIGNED KEY AUTO_INCREMENT,
admin_name VARCHAR(20) NOT NULL,
password   CHAR(32) NOT NULL
)ENGINE=INNODB;


-------------------------operation-----------------------

--------------book------------------------
select * from book where book_id=b_id
select * from book where book_title like'%b_title%'
select * from book where author like '%b_author%'
select * from book where publisher like '%b_publisher%'
insert  book values (i_book) comment 'an list'
delete from book where book_id=b_id
update book set book_title=b_title,author=b_author,
publisher=b_pub,description=b_des,addr=b_addr,price=b_pri 
where book_id=b_id

--------------reader----------------------
select * from reader where reader_id=r_id
select * from reader where reader_name=r_name
insert reader values (i_reader)
delete from reader where reader_id=r_id
update reader set reader_name=r_name, sex=r_sex, age=r_age, 
email=r_email, type=r_type
where reader_id=r_id

--------------borrow-----------------------
select * from borrow where bookid=bb_id
select bookid from borrow where readerid=br_id
select readerid from borrow where bookid=bb_id
insert borrow values(i_borrow)
delete from borrow where bookid=bb_id

select renew from borrow where bookid=bb_id
update borrow set renew=1 where bookid=bb_id

update borrow set returndate=i_date where bookid=bb_id
delete from borrow where returndate=i_date

select bookid from borrow where returndate<i_date
delete from borrow where returndate<i_date
 
--------------admin----------
select password from admin where admin_id=a_id
select password from admin where admin_name=a_name
insert admin values(i_admin)
delete from admin where admin_id=a_id

update admin set password=a_pass where admin_id=a_id


