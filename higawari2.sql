drop table if exists higawari2;
create table higawari2(
	id integer primary key autoincrement,
	time string,
	name string,
	identify string,
	price integer,
	vote integer defalut "0"
);