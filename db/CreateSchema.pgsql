-- users
DROP TYPE IF EXISTS server_role;

CREATE TYPE server_role AS ENUM ('user', 'admin', 'writer');

DROP SEQUENCE IF EXISTS users_id_seq;

CREATE SEQUENCE users_id_seq;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users(
    id integer PRIMARY KEY DEFAULT nextval('users_id_seq'),
    username varchar(32) UNIQUE NOT NULL,
    password varchar(512) NOT NULL,
    email varchar(320) UNIQUE NOT NULL,
    role server_role DEFAULT 'user' NOT NULL
);

-- posts
DROP SEQUENCE IF EXISTS posts_id_seq;

CREATE SEQUENCE posts_id_seq;

DROP TABLE IF EXISTS Posts;

CREATE TABLE Posts(
    id integer PRIMARY KEY DEFAULT nextval('posts_id_seq'),
    title varchar(128) NOT NULL,
    content text NOT NULL,
    date timestamp NOT NULL DEFAULT current_timestamp,
    author_id integer NOT NULL REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- comments
DROP SEQUENCE IF EXISTS comments_id_seq;

CREATE SEQUENCE comments_id_seq;

DROP TABLE IF EXISTS Comments;

CREATE TABLE Comments(
    id integer PRIMARY KEY DEFAULT nextval('comments_id_seq'),
    username varchar(32) NOT NULL,
    content text NOT NULL,
    date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_id integer NOT NULL REFERENCES posts (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- units
DROP SEQUENCE IF EXISTS units_id_seq;

CREATE SEQUENCE units_id_seq;

DROP TABLE IF EXISTS units;

CREATE TABLE Units(
    id INTEGER PRIMARY KEY DEFAULT nextval('units_id_seq'),
    unitname varchar(32) NOT NULL UNIQUE
);

-- products
DROP TYPE IF EXISTS product_verified;

CREATE TYPE product_verified AS ENUM('veirfied', 'not verified');

DROP SEQUENCE IF EXISTS products_id_seq;

CREATE SEQUENCE products_id_seq;

DROP TABLE IF EXISTS Products;

CREATE TABLE Products(
    id INTEGER PRIMARY KEY DEFAULT nextval('products_id_seq'),
    productname varchar(128) NOT NULL,
    fats numeric(10, 3) NOT NULL CHECK (fats > 0),
    proteins numeric(10, 3) NOT NULL CHECK (proteins > 0),
    carbohydrates numeric(10, 3) NOT NULL CHECK (carbohydrates > 0),
    calories numeric(10, 3) NOT NULL CHECK (calories > 0),
    baseAmount numeric(10, 3) NOT NULL CHECK (baseAmount > 0),
    veirfied product_verified NOT NULL DEFAULT 'not verified',
    amountType integer NOT NULL REFERENCES Units (id) ON UPDATE CASCADE ON DELETE CASCADE
    CONSTRAINT valid_amount CHECK (fats + proteins + carbohydrates <= baseAmount)
);
