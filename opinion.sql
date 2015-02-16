drop table if exists entries;
create table opinion(
    question string not null,
    answer string,
    datatime datatime not null,
    id integer primary key autoincrement
);
