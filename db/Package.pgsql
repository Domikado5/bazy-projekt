CREATE OR REPLACE FUNCTION getProportions(product_id integer, value numeric)
    RETURNS TABLE (fats numeric, proteins numeric, carbohydrates numeric, calories numeric) AS $$
DECLARE
    prod_row products%ROWTYPE;
    prop numeric;
BEGIN
    SELECT * INTO prod_row FROM products WHERE id=product_id;
    prop := value / prod_row.base_amount;
    RETURN QUERY SELECT p.fats * prop, p.proteins * prop, p.carbohydrates * prop, p.calories * prop
    FROM products AS p WHERE p.id = product_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE updateDiary(p_diary_id integer, p_product_id integer, p_previous_amount numeric)
AS $$
DECLARE
    cur_entries cursor (d_id integer, p_id integer) for
                SELECT * FROM entries WHERE diary_id = d_id and product_id = p_id;
    entry_row entries%ROWTYPE;
    new_prod_values record;
    old_prod_values record;
BEGIN
    -- open the cursor
    open cur_entries(p_diary_id, p_product_id);

    fetch cur_entries into entry_row;

    SELECT *
    INTO old_prod_values
    FROM getProportions(p_product_id, p_previous_amount);

    SELECT *
    INTO new_prod_values
    FROM getProportions(p_product_id, entry_row.amount);

    UPDATE Diaries
    SET total_fats = total_fats + (new_prod_values.fats - old_prod_values.fats)
    WHERE id = p_diary_id;

    UPDATE Diaries
    SET total_proteins = total_proteins + (new_prod_values.proteins - old_prod_values.proteins)
    WHERE id = p_diary_id;

    UPDATE Diaries
    SET total_carbohydrates = total_carbohydrates + (new_prod_values.carbohydrates - old_prod_values.carbohydrates)
    WHERE id = p_diary_id;

    UPDATE Diaries
    SET total_calories = total_calories + (new_prod_values.calories - old_prod_values.calories)
    WHERE id = p_diary_id;

    commit;
END;
$$
LANGUAGE plpgsql;