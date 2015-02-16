drop table if exists entries;
create table osirase(
    datatime datatime not null,
    title string not null,
    parent_id integer
);
