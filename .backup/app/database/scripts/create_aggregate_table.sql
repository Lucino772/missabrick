CREATE TABLE agg_parts
AS SELECT
    inventory_parts.inventory_id AS inventory_id,
    parts.part_num AS part_num,
    parts.name AS part_name,
    parts.part_cat_id AS part_cat_id,
    parts.part_material AS part_material,
    colors.id AS color_id,
    colors.name AS color_name,
    colors.rgb AS color_rgb,
    colors.is_trans AS color_is_trans,
    inventory_parts.quantity AS quantity,
    inventory_parts.is_spare AS is_spare,
    inventory_parts.img_url AS img_url
FROM inventory_parts, parts, colors
WHERE colors.id = inventory_parts.color_id
    AND parts.part_num = inventory_parts.part_num