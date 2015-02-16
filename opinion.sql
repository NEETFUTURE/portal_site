drop table if exists opinion;
create table opinion(
    question string not null,
    answer string,
    datatime datatime not null,
    id integer primary key autoincrement
);
