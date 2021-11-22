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

CREATE TYPE product_verified AS ENUM('verified', 'not verified');

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

-- productCategories
DROP SEQUENCE IF EXISTS product_categories_id_seq;

CREATE SEQUENCE product_categories_id_seq;

DROP TABLE IF EXISTS Product_Categories;

CREATE TABLE Product_Categories(
    id INTEGER PRIMARY KEY DEFAULT nextval('product_categories_id_seq'),
    categoryName varchar(128) NOT NULL,
    rootCategory integer REFERENCES Product_Categories (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- allergenes
DROP SEQUENCE IF EXISTS allergenes_id_seq;

CREATE SEQUENCE allergenes_id_seq;

DROP TABLE IF EXISTS Allergenes;

CREATE TABLE Allergenes(
    id INTEGER PRIMARY KEY DEFAULT nextval('allergenes_id_seq'),
    allergenName varchar(128) NOT NULL
);

-- product allergenes
DROP TABLE IF EXISTS products_allergenes;

CREATE TABLE Products_Allergenes(
    productId integer NOT NULL REFERENCES products (id) ON DELETE CASCADE ON UPDATE CASCADE,
    allergenId integer NOT NULL REFERENCES allergenes (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- diaries
DROP SEQUENCE IF EXISTS diaries_id_seq;

CREATE SEQUENCE diaries_id_seq;

DROP TABLE IF EXISTS Diaries;

CREATE TABLE Diaries(
    id INTEGER PRIMARY KEY DEFAULT nextval('diaries_id_seq'),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    totalcalories numeric(10, 3) NOT NULL CHECK (totalcalories > 0),
    totalfats numeric(10, 3) NOT NULL CHECK (totalfats > 0),
    totalproteins numeric(10, 3) NOT NULL CHECK (totalproteins > 0),
    totalcarbohydrates numeric(10, 3) NOT NULL CHECK (totalcarbohydrates > 0)
);

-- entries
DROP SEQUENCE IF EXISTS entries_id_seq;

CREATE SEQUENCE entries_id_seq;

DROP TABLE IF EXISTS Entries;

CREATE TABLE Entries(
    productId INTEGER NOT NULL REFERENCES Products (id) ON DELETE CASCADE ON UPDATE CASCADE,
    diaryId INTEGER NOT NULL REFERENCES Diaries (id) ON DELETE CASCADE ON UPDATE CASCADE,
    amount numeric(10, 3) NOT NULL CHECK (amount > 0)
);

-- sets
DROP SEQUENCE IF EXISTS sets_id_seq;

CREATE SEQUENCE sets_id_seq;

DROP TABLE IF EXISTS Sets;

CREATE TABLE Sets(
    id INTEGER PRIMARY KEY DEFAULT nextval('sets_id_seq'),
    setName varchar(128) NOT NULL,
    description text NULL,
    ownerId INTEGER NOT NULL REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- set has products
DROP TABLE IF EXISTS Sets_Products;

CREATE TABLE Sets_Products(
    productId INTEGER NOT NULL REFERENCES Products (id) ON DELETE CASCADE On UPDATE CASCADE,
    setId INTEGER NOT NULL REFERENCES Sets (id) ON DELETE CASCADE On UPDATE CASCADE
);

-- setcategories
DROP SEQUENCE IF EXISTS set_categories_id_seq;

CREATE SEQUENCE set_categories_id_seq;

DROP TABLE IF EXISTS set_categories;

CREATE TABLE set_categories(
    id INTEGER PRIMARY KEY DEFAULT nextval('set_categories_id_seq'),
    categoryName varchar(128) NOT NULL
);

-- setcategories sets
DROP TABLE IF EXISTS Sets_set_categories;

CREATE TABLE Sets_set_categories(
    setId INTEGER NOT NULL REFERENCES Sets (id) ON DELETE CASCADE ON UPDATE CASCADE,
    categoryId INTEGER NOT NULL REFERENCES Set_categories (id) On DELETE CASCADE ON UPDATE CASCADE
);