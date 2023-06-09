SELECT COUNT(*)
FROM aka_name AS an
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND n.id = an.person_id ) 
JOIN (SELECT ci.movie_id AS ci_movie_id,ci.person_id AS ci_person_id,t.id AS t_id FROM cast_info AS ci
 join role_type AS rt on (ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)', '(voice: English version)') AND rt.role_t ='actress' AND rt.id = ci.role_id ) join title AS t on (t.production_year > 2010 AND t.id = ci.movie_id ) join char_name AS chn on (chn.id = ci.person_role_id ))S1 on (n.id = S1.ci_person_id AND S1.ci_person_id = an.person_id ) 
JOIN (SELECT mc.movie_id AS mc_movie_id FROM movie_companies AS mc
 join company_name AS cn on (cn.country_code ='[us]' AND cn.id = mc.company_id ))S2 on (S2.mc_movie_id = S1.ci_movie_id AND S1.t_id = S2.mc_movie_id ) 
JOIN (SELECT mk.movie_id AS mk_movie_id FROM movie_keyword AS mk
 join keyword AS k on (k.keyword IN ('hero',  'martial-arts',  'hand-to-hand-combat') AND k.id = mk.keyword_id ))S3 on (S1.ci_movie_id = S3.mk_movie_id AND S1.t_id = S3.mk_movie_id AND S2.mc_movie_id = S3.mk_movie_id ) 
JOIN (SELECT mi.movie_id AS mi_movie_id FROM movie_info AS mi
 join info_type AS it on (mi.info != '' AND (mi.info LIKE 'Japan:%201%'  OR mi.info LIKE 'USA:%201%') AND it.info = 'release dates' AND it.id = mi.info_type_id ))S4 on (S4.mi_movie_id = S1.ci_movie_id AND S1.t_id = S4.mi_movie_id AND S2.mc_movie_id = S4.mi_movie_id AND S4.mi_movie_id = S3.mk_movie_id );