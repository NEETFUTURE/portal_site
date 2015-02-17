drop table if exists carousel;
create table carousel(
	id integer primary key autoincrement,
    pic_name string not null,
    h1_str string not null,
    link string not null
);
