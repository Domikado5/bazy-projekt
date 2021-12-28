-- User
INSERT INTO users values(DEFAULT, 'JustDodo', '$2b$12$24Y1.a9EBA6hbPqVM/2AGeRsH5n3z7T3Y59PBYa4zvwcM1/9hxaRq', 'dodo@dodo.com', 'user'); -- 12345678
INSERT INTO users values(DEFAULT, 'RandomUser', '$2b$12$pcnu7BDnc0IIjIYVp2oYUey7nGitc/1EwLyhCSNK6ObCS4urdJ7B.', 'test@test.com', 'user'); -- Password123
INSERT INTO users values(DEFAULT, 'Joseph', '$2b$12$pcnu7BDnc0IIjIYVp2oYUey7nGitc/1EwLyhCSNK6ObCS4urdJ7B.', 'writer@letter.com', 'writer'); -- Password123
INSERT INTO users values(DEFAULT, 'kimziol', '$2b$12$L4ZKqOmVkRqEsNeCwZrVwuwDiKBtvq5iVlrzC4k17jW7Bi5q2vGIq', 'admin@root.com', 'admin'); -- Strong123


-- Post
INSERT INTO posts values(DEFAULT, 'Be strong', 'You need to eat vegetables to be strong!', CURRENT_TIMESTAMP, 3);
INSERT INTO posts values(DEFAULT, 'How to be healthy?', 'Health!!!!', CURRENT_TIMESTAMP, 3);
INSERT INTO posts values(DEFAULT, 'Best proteins', 'SKYR', CURRENT_TIMESTAMP, 3);


-- Comment
INSERT INTO comments values(DEFAULT, 'kimziol', 'SKYR', CURRENT_TIMESTAMP, 3);
INSERT INTO comments values(DEFAULT, 'JustDodo', 'SKYR', CURRENT_TIMESTAMP, 3);
INSERT INTO comments values(DEFAULT, 'Joseph', 'SKYR', CURRENT_TIMESTAMP, 3);
INSERT INTO comments values(DEFAULT, 'JustDodo', 'Cool!', CURRENT_TIMESTAMP, 2);
INSERT INTO comments values(DEFAULT, 'Joseph', 'Now Im healthy!', CURRENT_TIMESTAMP, 2);
INSERT INTO comments values(DEFAULT, 'JustDodo', 'Bleh.', CURRENT_TIMESTAMP, 1);
INSERT INTO comments values(DEFAULT, 'Joseph', 'V E G E T A B L E S ! ! !', CURRENT_TIMESTAMP, 1);

-- Unit
INSERT INTO units values(DEFAULT, 'g'); -- gramm
INSERT INTO units values(DEFAULT, 'l'); -- liter
INSERT INTO units values(DEFAULT, 'tbsp'); -- tablespoon

-- ProductCategory
INSERT INTO product_categories values(DEFAULT, 'Liquid', NULL);
INSERT INTO product_categories values(DEFAULT, 'Juices', 1);
INSERT INTO product_categories values(DEFAULT, 'Meat', NULL);

-- Product
INSERT INTO products values(DEFAULT, 'Water', 0, 0, 0, 0, 1, 'verified', 2, 1);
INSERT INTO products values(DEFAULT, 'Caprio Orange Juice 100% Free', 10, 1, 1, 5, 30, 'not verified', 3, 2);
INSERT INTO products values(DEFAULT, 'Chicken', 14, 27, 0, 239, 100, 'verified', 1, 3);

-- Allergen
INSERT INTO allergens values(DEFAULT, 'nuts');
INSERT INTO allergens values(DEFAULT, 'non-vegan');
INSERT INTO allergens values(DEFAULT, 'Sodium benzoate');

-- ProductsAllergens
INSERT INTO products_allergens values(DEFAULT, 1, 2);
INSERT INTO products_allergens values(DEFAULT, 3, 2);
INSERT INTO products_allergens values(DEFAULT, 2, 3);


-- Diary
INSERT INTO diaries values(DEFAULT, CURRENT_DATE, 0, 0, 0, 0, 1);
INSERT INTO diaries values(DEFAULT, CURRENT_DATE, 0, 0, 0, 0, 4);


-- Entry
INSERT INTO entries values(DEFAULT, 15, 2, 1);
INSERT INTO entries values(DEFAULT, 2, 1, 1);
INSERT INTO entries values(DEFAULT, 2, 1, 2);
INSERT INTO entries values(DEFAULT, 200, 3, 2);

-- Set
INSERT INTO sets values(DEFAULT, 'Typical Breakfast', NULL, 1);
INSERT INTO sets values(DEFAULT, 'Gym Breakfast', 'For strong man!', 4);

-- SetsProducts
INSERT INTO sets_products values(DEFAULT, 2, 1);
INSERT INTO sets_products values(DEFAULT, 1, 1);
INSERT INTO sets_products values(DEFAULT, 3, 2);

-- SetCategory
INSERT INTO set_categories values(DEFAULT, 'Breakfast');
INSERT INTO set_categories values(DEFAULT, 'Workout');

-- sets_setcategorys
INSERT INTO sets_setcategorys values(DEFAULT, 1, 1);
INSERT INTO sets_setcategorys values(DEFAULT, 1, 2);
INSERT INTO sets_setcategorys values(DEFAULT, 2, 2);