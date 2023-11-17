CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    business_name TEXT,
    business_id TEXT
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    iban TEXT,
    email TEXT,
    mobile_nr TEXT,
    post_address TEXT,
    payment_term INTEGER
);

CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    record_date DATE,
    title TEXT,
    record_type INTEGER,
    record_class TEXT,
    vat INTEGER,
    amount DOUBLE PRECISION,
    price DOUBLE PRECISION
);

CREATE TABLE invoice (
    id SERIAL PRIMARY KEY,
    record_id INTEGER REFERENCES records,
    customer TEXT,
    iban TEXT,
    email TEXT,
    mobile_nr TEXT,
    post_address TEXT,
    payment_term INTEGER
);

CREATE TABLE record_class (
    id SERIAL PRIMARY KEY,
    record_type INTEGER,
    record_class TEXT,
    vat INTEGER
);
