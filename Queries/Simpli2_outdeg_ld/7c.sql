SELECT COUNT(*)
FROM movie_link AS ml
join link_type AS lt on (lt.link IN ('references', 'referenced in', 'features', 'featured in') AND lt.id = ml.link_type_id ) 
join title AS t on (t.production_year BETWEEN 1980 AND 2010 AND ml.linked_movie_id = t.id ) 
join cast_info AS ci on (t.id = ci.movie_id AND ci.movie_id = ml.linked_movie_id ) 
join name AS n on (n.name_pcode_cf BETWEEN 'A' AND 'F' AND (n.gender='m' OR (n.gender = 'f' AND n.name LIKE 'A%')) AND ci.person_id = n.id ) 
join aka_name AS an on (an.name != '' AND (an.name LIKE '%a%' OR an.name LIKE 'A%') AND n.id = an.person_id AND an.person_id = ci.person_id ) 
join person_info AS pi on (pi.note != '' AND n.id = pi.person_id AND pi.person_id = an.person_id AND pi.person_id = ci.person_id ) 
join info_type AS it on (it.info ='mini biography' AND it.id = pi.info_type_id );