drop table if exists osirase;
create table osirase(
	id integer primary key autoincrement,
    time string not null,
    title string not null
);
