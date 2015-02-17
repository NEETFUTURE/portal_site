drop table if exists osirase;
create table osirase(
	id integer primary key autoincrement,
    datatime datatime not null,
    title string not null
);
