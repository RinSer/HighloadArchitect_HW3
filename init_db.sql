CREATE TABLE IF NOT EXISTS users (
    id           SERIAL PRIMARY KEY,
    login        VARCHAR(10),
    password     VARCHAR(100)
);

CREATE UNIQUE INDEX users_login ON users(login);

CREATE TABLE IF NOT EXISTS profiles (
    id            SERIAL PRIMARY KEY,
    user_id       INT REFERENCES users(id),
    name          VARCHAR(20),
    surname       VARCHAR(20),
    age           INT,
    gender        BOOLEAN,
    interests     TEXT,
    city          VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS friends (
    f1_user_id  INT REFERENCES users(id),
    f2_user_id  INT REFERENCES users(id),
    f1_approved BOOLEAN,
    f2_approved BOOLEAN,
    PRIMARY KEY(f1_user_id, f2_user_id)
);