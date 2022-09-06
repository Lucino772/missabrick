CREATE TEMP TABLE match_sets
AS SELECT *, themes.name AS name_theme
FROM sets, themes
WHERE themes.id = sets.theme_id
    AND set_num LIKE '%{search}%';

CREATE TEMP TABLE sets_count
AS SELECT COUNT(*) AS total_rows
FROM match_sets; 

CREATE TEMP TABLE found_sets
AS SELECT *
FROM match_sets
LIMIT {page_size}
OFFSET {offset};