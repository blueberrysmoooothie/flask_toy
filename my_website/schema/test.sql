use testDB;

CREATE TABLE
    USER_DATA(
        idx INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_name_ VARCHAR(256) NOT NULL,
        user_id_ VARCHAR(256) NOT NULL UNIQUE Key,
        user_password_ VARCHAR(512) NOT NULL
    ) CHARSET = utf8;