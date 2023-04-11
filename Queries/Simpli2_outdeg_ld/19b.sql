SELECT COUNT(*)
FROM movie_companies AS mc
join company_name AS cn on (mc.note LIKE '%(200%)%' AND (mc.note LIKE '%(USA)%' OR mc.note LIKE '%(worldwide)%') AND cn.country_code ='[us]' AND cn.id = mc.company_id ) 
join title AS t on (t.production_year BETWEEN 2007 AND 2008 AND t.title LIKE '%Kung%Fu%Panda%' AND t.id = mc.movie_id ) 
join cast_info AS ci on (ci.note = '(voice)' AND t.id = ci.movie_id AND mc.movie_id = ci.movie_id ) 
join role_type AS rt on (rt.role_t ='actress' AND rt.id = ci.role_id ) 
join char_name AS chn on (chn.id = ci.person_role_id ) 
join name AS n on (n.gender ='f' AND n.name LIKE '%Angel%' AND n.id = ci.person_id ) 
join aka_name AS an on (n.id = an.person_id AND ci.person_id = an.person_id ) 
join movie_info AS mi on (mi.info != '' AND (mi.info LIKE 'Japan:%2007%' OR mi.info LIKE 'USA:%2008%') AND t.id = mi.movie_id AND mc.movie_id = mi.movie_id AND mi.movie_id = ci.movie_id ) 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id );