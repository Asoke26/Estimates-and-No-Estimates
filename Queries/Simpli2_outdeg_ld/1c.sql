SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it on (it.info = 'top 250 rank' AND it.id = mi_idx.info_type_id ) 
join title AS t on (t.production_year >2010 AND t.id = mi_idx.movie_id ) 
join movie_companies AS mc on ((mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%'  AND mc.note LIKE '%(co-production)%') AND t.id = mc.movie_id AND mc.movie_id = mi_idx.movie_id ) 
join company_type AS ct on (ct.kind = 'production companies' AND ct.id = mc.company_type_id );