drop table if exists entries;
create table carousel(
    pic_name string not null,
    h1_str string not null,
    link string not null,
    parent_id integer
);
