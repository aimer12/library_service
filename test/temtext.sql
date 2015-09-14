insert book (book_title,  author,addr, price) values ('Introduce to tornado', 'john smith', '4-2-4',3.73);


insert book (book_title, addr, price) values ('learn python','4-2-7', 3.43);


insert book (book_title, addr, price) values ('learn python the hard way','4-2-8', 12.3);

alter table book add  unique key (addr);

alter table admin add unique key(admin_name);

insert admin values ('1','admin','aimer');

insert reader (reader_name,sex,age,email,type) values ('sanli','woman','13','ailun@evol','0');
insert reader (reader_name,sex,age,email,type) values ('ailun','0','13','juren@evol',0);

alter table borrow add brw_id smallint key auto_increment;



