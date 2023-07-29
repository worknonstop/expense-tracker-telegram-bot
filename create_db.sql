create table category(
    uniqname primary key,
    name
)

create table expense(
    id integer primary key,
    cost integer,
    date datetime,
    category_uniqname integer,
    foreign key(category_uniqname) references category(uniqname)
)

insert into category (uniqname, name)
values
    ("products", "продукты"),
    ("clean_suplies", "химия"),
    ("transport", "транспорт"),
    ("credit", "кредит"),
    ("education", "образование"),
    ("apartment", "квартира"),
    ("telecom", "связь"),
    ("clothes", "одежда"),
    ("hobby", "hobby"),
    ("other", "другое"),
