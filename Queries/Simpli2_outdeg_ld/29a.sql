SELECT COUNT(*)
FROM complete_cast AS cc
join comp_cast_type AS cct1 on (cct1.kind ='cast' AND cct1.id = cc.subject_id ) 
join comp_cast_type AS cct2 on (cct2.kind ='complete+verified' AND cct2.id = cc.status_id ) 
join title AS t on (t.title = 'Shrek 2' AND t.production_year BETWEEN 2000 AND 2010 AND t.id = cc.movie_id ) 
join cast_info AS ci on (ci.note IN ('(voice)', '(voice) (uncredited)', '(voice: English version)') AND t.id = ci.movie_id AND ci.movie_id = cc.movie_id ) 
join role_type AS rt on (rt.role_t ='actress' AND rt.id = ci.role_id ) 
join char_name AS chn on (chn.name = 'Queen' AND chn.id = ci.person_role_id ) 
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND n.id = ci.person_id ) 
join movie_companies AS mc on (t.id = mc.movie_id AND mc.movie_id = ci.movie_id AND mc.movie_id = cc.movie_id ) 
join company_name AS cn on (cn.country_code ='[us]' AND cn.id = mc.company_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mc.movie_id = mk.movie_id AND ci.movie_id = mk.movie_id AND mk.movie_id = cc.movie_id ) 
join keyword AS k on (k.keyword = 'computer-animation' AND k.id = mk.keyword_id ) 
join aka_name AS an on (n.id = an.person_id AND ci.person_id = an.person_id ) 
join movie_info AS mi on (mi.info != '' AND (mi.info LIKE 'Japan:%200%' OR mi.info LIKE 'USA:%200%') AND t.id = mi.movie_id AND mc.movie_id = mi.movie_id AND mi.movie_id = ci.movie_id AND mi.movie_id = mk.movie_id AND mi.movie_id = cc.movie_id ) 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id ) 
join person_info AS pi on (n.id = pi.person_id AND ci.person_id = pi.person_id ) 
join info_type AS it3 on (it3.info = 'trivia' AND it3.id = pi.info_type_id );