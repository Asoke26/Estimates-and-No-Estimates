SELECT COUNT(*)
FROM movie_keyword AS mk
join keyword AS k on (k.keyword LIKE '%mile%' AND mk.keyword_id = k.id ) 
join title AS t1 on (t1.id = mk.movie_id ) 
join movie_link AS ml on (ml.movie_id = t1.id ) 
join link_type AS lt on (lt.id = ml.link_type_id ) 
join title AS t2 on (ml.linked_movie_id = t2.id );