-- Set
ALTER TABLE sets
DROP CONSTRAINT fk_sets_users_id_owner,
ADD CONSTRAINT fk_sets_users_id_owner
    FOREIGN KEY (owner)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Diary
ALTER TABLE diaries
DROP CONSTRAINT fk_diaries_users_id_owner,
ADD CONSTRAINT fk_diaries_users_id_owner
    FOREIGN KEY (owner)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Post
ALTER TABLE posts
DROP CONSTRAINT fk_posts_users_id_author,
ADD CONSTRAINT fk_posts_users_id_author
    FOREIGN KEY (author)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Comment
ALTER TABLE comments
DROP CONSTRAINT fk_comments_posts_id_root_post,
ADD CONSTRAINT fk_comments_posts_id_root_post
    FOREIGN KEY (root_post)
    REFERENCES posts(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Product
ALTER TABLE products
DROP CONSTRAINT fk_products_product_categories_id_categories,
DROP CONSTRAINT fk_products_units_id_unit,
ADD CONSTRAINT fk_products_product_categories_id_categories
    FOREIGN KEY (categories)
    REFERENCES product_categories(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_products_units_id_unit
    FOREIGN KEY (unit)
    REFERENCES units(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- ProductCategory
ALTER TABLE product_categories
DROP CONSTRAINT fk_product_categories_product_categories_id_root_category,
ADD CONSTRAINT fk_product_categories_product_categories_id_root_category
    FOREIGN KEY (root_category)
    REFERENCES product_categories(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;