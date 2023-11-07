CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    IBAN TEXT,
    Business_id TEXT,
    email TEXT,
    mobile_nr TEXT,
    post_address TEXT,
    payment_term INTEGER,
    VAT INTEGER
);

CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    record_date DATE,
    title TEXT,
    record_type TEXT,
    record_class TEXT,
    amount INTEGER,
    price InTEGER
);

CREATE TABLE invoice (
    id SERIAL PRIMARY KEY,
    record_id INTEGER REFERENCES records,
    customer TEXT
);
