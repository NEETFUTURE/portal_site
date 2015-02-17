drop table if exists opinion;
create table opinion(
	id integer primary key autoincrement,
    question string not null,
    answer string,
    datatime datatime not null
);
