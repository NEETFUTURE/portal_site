drop table if exists opinion;
create table opinion(
	id integer primary key autoincrement,
    question string not null,
    answer string,
    time string not null
);
