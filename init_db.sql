CREATE TABLE IF NOT EXISTS profiles (
    id            SERIAL PRIMARY KEY,
    firstName     VARCHAR(20),
    secondName    VARCHAR(20),
    interests     TEXT,
    city          VARCHAR(100)
) ENGINE=InnoDB;