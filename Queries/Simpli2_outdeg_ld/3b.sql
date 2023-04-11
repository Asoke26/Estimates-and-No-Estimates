SELECT COUNT(*)
FROM movie_keyword AS mk
join keyword AS k on (k.keyword LIKE '%sequel%' AND k.id = mk.keyword_id ) 
join title AS t on (t.production_year > 2010 AND t.id = mk.movie_id ) 
join movie_info AS mi on (mi.info IN ('Bulgaria') AND t.id = mi.movie_id AND mk.movie_id = mi.movie_id );