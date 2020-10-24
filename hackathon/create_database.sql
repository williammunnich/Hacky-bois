CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY AUTOINCREMENT,
    account_type int not null,
    email varchar,
    password varchar,
    unique (email, account_type)
);

