```pgsql

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
```