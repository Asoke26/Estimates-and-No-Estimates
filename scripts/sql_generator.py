import os,sys, time


################################################# Read plan from plan file ############################################################
PATH = "plans/Simpli2_fk_outdeg_ld.txt"
Queries =  [
		'1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6b','6c','6d','6e','6f', \
        '7a','7b','7c','8a','8b','8c','8d','9a','9b','9c','9d','10a','10b','10c','11a','11b','11c','11d','12a','12b','12c', \
        '13a','13b','13c','13d','14a','14b','14c','15a','15b','15c','15d','16a','16b','16c','16d','17a','17b','17c','17d', \
        '17e','17f','18a','18b','18c','19a','19b','19c','19d','20a','20b','20c','21a','21b','21c','22a','22b','22c','22d', \
        '23a','23b','23c','24a','24b','25a','25b','25c','26a','26b','26c','27a','27b','27c','28a','28b','28c','29a','29b', \
        '29c','30a','30b','30c','31a','31b','31c','32a','32b','33a','33b','33c'
        ]


plan_dict = dict()
for line in open(PATH,'r').readlines():
	if not line.strip():
		continue
	line = line.strip()
	key = line.split(':')[0].strip()
	plan = line.split(':')[1].strip()
	plan_dict[key] = plan

all_subs = dict()
for qry in Queries:
	
	not_visited = plan_dict[qry].split(' ')
	visited = []
	visited.append(not_visited[0])
	not_visited.remove(visited[0])
	i = 1
	j = 1
	subs = dict()
	subs[i] = plan_dict[qry]
	all_subs[qry] = subs

###############################################################################################################################################

def qry_reader(file):
	PATH = "Queries/implicit/"
	query = open(PATH+file+".sql",'r').read()
	AS_MAPPING = dict()
	FROM = query.split("WHERE")[0].split("FROM")[1]
	FROM = FROM.split(',')

	for tbl_as in FROM:
		tbl = tbl_as.split("AS")[0].strip()
		as_ = tbl_as.split("AS")[1].strip()
		AS_MAPPING[as_] = tbl

	query_lines = open(PATH+file+".sql",'r').readlines()
	SELECT_MAPPING = dict()
	JOIN_MAPPING = dict()
	for key in AS_MAPPING.keys():
		SELECT_MAPPING[key] = list()
		JOIN_MAPPING[key] = list()

	whr_flag = False
	for predicate in query_lines:
		if ';' in predicate:
			predicate = predicate.replace(';','')
		if not predicate.strip():
			continue
		if "WHERE" in predicate:
			whr_flag = True
		if whr_flag == True:
			if "WHERE" in predicate:
				predicate = predicate.replace("WHERE","",1).strip()
			elif "AND" in predicate:
				predicate = predicate.replace("AND","",1).strip()

			if '=' not in predicate:
				key1 = predicate.split('.')[0].replace('(','')
				SELECT_MAPPING[key1].append(predicate)
				continue
			left = predicate.split('=')[0].strip()
			right = predicate.split('=')[1].strip()
			if '.' in left and '.' in right and 'id' in predicate:
				left_key = left.split('.')[0]
				right_key = right.split('.')[0]
				JOIN_MAPPING[left_key].append(predicate)
				JOIN_MAPPING[right_key].append(predicate)
			else:
				key2 = predicate.split('.')[0]
				if '(' in key2:
					key2 = key2.replace('(','')
				SELECT_MAPPING[key2].append(predicate)

	return AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING

def update_join_map(_tbls,sub_no,JOIN_MAPPING,subquery_col_map):
	for tbl in _tbls:
		for pred in JOIN_MAPPING[tbl]:
			left = pred.split('=')[0].strip()
			right = pred.split('=')[1].strip()
			left_tbl = left.split('.')[0].strip()
			right_tbl = right.split('.')[0].strip()
			if left_tbl in _tbls and right_tbl in _tbls:
				JOIN_MAPPING[right_tbl].remove(pred)
				JOIN_MAPPING[left_tbl].remove(pred)


	for tbl in _tbls:
		for pred in JOIN_MAPPING[tbl]:
			pred_copy = pred
			left = pred.split('=')[0].strip()
			right = pred.split('=')[1].strip()
			if left in subquery_col_map.keys():
				pred = pred.replace(left,subquery_col_map[left])
				right_tbl = right.split('.')[0]
				JOIN_MAPPING[right_tbl].remove(pred_copy)
				JOIN_MAPPING[right_tbl].append(pred)
				JOIN_MAPPING[sub_no].append(pred)
			elif right in subquery_col_map.keys():
				pred = pred.replace(right,subquery_col_map[right])
				left_tbl = left.split('.')[0]
				JOIN_MAPPING[left_tbl].remove(pred_copy)
				JOIN_MAPPING[left_tbl].append(pred)
				JOIN_MAPPING[sub_no].append(pred)
		del JOIN_MAPPING[tbl]

def expose_columns(_tbls,sub_no,JOIN_MAPPING):
	columns_visited = []
	subquery_col_map = dict()
	select_stmt = ""
	for tbl in _tbls:
		for pred in JOIN_MAPPING[tbl]:
			left = pred.split('=')[0].strip()
			right = pred.split('=')[1].strip()
			left_tbl = left.split('.')[0].strip()
			right_tbl = right.split('.')[0].strip()
			left_attr = left.split('.')[1].strip()
			right_attr = right.split('.')[1].strip()

			if left_tbl == tbl and left not in columns_visited and right_tbl not in _tbls:
				select_stmt += left+' AS '+left_tbl+'_'+left_attr+','
				columns_visited.append(left)
				subquery_col_map[left] = sub_no+'.'+left_tbl+'_'+left_attr
			elif right_tbl == tbl and right not in columns_visited and left_tbl not in _tbls:
				select_stmt += right+' AS '+right_tbl+'_'+right_attr+','
				columns_visited.append(right)
				subquery_col_map[right] = sub_no+'.'+right_tbl+'_'+right_attr
	return select_stmt,subquery_col_map

def build_subquery(_tbls,sub_no,AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING):

		visited = []
		not_visited = _tbls.copy()
		visited.append(not_visited[0])
		not_visited.remove(visited[0])
		i = 0
		first_tbl_flag = True
		sql_stmt = " FROM "+AS_MAPPING[visited[0]]+" AS "+visited[0]+"\n"
		while(len(not_visited) != 0):
			tbl = not_visited[i]
			sql_stmt += ' join '
			sql_stmt += AS_MAPPING[tbl]+' AS '+tbl +' on ('
			if first_tbl_flag == True:
				for pred in SELECT_MAPPING[visited[0]]:
					sql_stmt += pred+' AND '
				first_tbl_flag = False	
			for pred in SELECT_MAPPING[tbl]:
				sql_stmt += pred+' AND '

			for pred in JOIN_MAPPING[tbl]:
				pred = pred.strip()
				left = pred.split('=')[0].strip()
				right = pred.split('=')[1].strip()
				left_tbl = left.split('.')[0].strip()
				right_tbl = right.split('.')[0].strip()
				if left_tbl in visited or right_tbl in visited:
					sql_stmt += pred+' AND '
			sql_stmt = sql_stmt[:-4]+')'
			visited.append(tbl)
			not_visited.remove(tbl)

		columns,subquery_col_map = expose_columns(_tbls,sub_no,JOIN_MAPPING)
		columns = columns[:-1]
		# print(columns,subquery_col_map)
		# Create sub-query statement
		subquery_stmt = "(SELECT "+columns+sql_stmt+')'+sub_no
		# print(subquery_stmt)
		update_join_map(_tbls,sub_no,JOIN_MAPPING,subquery_col_map)
		return subquery_stmt


Queries1 = [
		'1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6b','6c','6d','6e','6f', \
        '7a','7b','7c','8a','8b','8c','8d','9a','9b','9c','9d','10a','10b','10c','11a','11b','11c','11d','12a','12b','12c', \
        '13a','13b','13c','13d','14a','14b','14c','15a','15b','15c','15d','16a','16b','16c','16d','17a','17b','17c','17d', \
        '17e','17f','18a','18b','18c','19a','19b','19c','19d','20a','20b','20c','21a','21b','21c','22a','22b','22c','22d', \
        '23a','23b','23c','24a','24b','25a','25b','25c','26a','26b','26c','27a','27b','27c','28a','28b','28c', \
        '29a','29b', '29c','30a','30b','30c','31a','31b','31c','32a','32b','33a','33b','33c'
        ]
# Queries1 = ['18a']
for qry in Queries1:
	startTime = time.time()
	# print("#################################",qry,"#################################")
	# out_path = "/home/postgres/Simpli2-EXP-new/Queries/test/"
	# if not os.path.isdir(out_path):
	# 	os.mkdir(out_path)

	out_stmts = dict()

	for key,val in all_subs[qry].items():
		AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING = qry_reader(qry)
		qry_plan = val
		qry_plan_copy = qry_plan
		qry_plan = qry_plan.split(' ')
		# print("===",key,qry_plan)
		subquery_dict = dict()
		subquery = []
		subquery_str = ""
		s = 1
		sub_flag = 0
		for tbl in qry_plan:
			if '(' in tbl:
				subquery_str += tbl+" "
				tbl = tbl.replace('(','')
				subquery.append(tbl)
				sub_flag = 1
			elif ')' in tbl:
				subquery_str += tbl
				tbl = tbl.replace(')','')
				subquery.append(tbl)
				subquery_dict['S'+str(s)] = subquery.copy()
				qry_plan_copy = qry_plan_copy.replace(subquery_str,'S'+str(s))
				subquery.clear()
				subquery_str = ""
				s += 1
				sub_flag = 0
			elif sub_flag==1:
				subquery_str += tbl+" "
				subquery.append(tbl)
		
		for key1,val1 in subquery_dict.items():
			JOIN_MAPPING[key1] = []
			subquery_dict[key1] = build_subquery(val1,key1,AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING)
			# print(subquery_dict[key1])

		# Full Query 
		visited = []
		not_visited = qry_plan_copy.strip().split()
		visited.append(not_visited[0])
		not_visited.remove(visited[0])
		sql_stmt = "SELECT COUNT(*)\nFROM "+AS_MAPPING[visited[0]]+" AS "+visited[0]+"\n"
		i = 0
		first_tbl_flag = True
		while(len(not_visited) != 0):
			tbl = not_visited[i]
			if 'S' in tbl:
				sql_stmt += 'JOIN '
				sql_stmt += subquery_dict[tbl] + ' on ('
			else:
				sql_stmt += 'join '
				sql_stmt += AS_MAPPING[tbl]+' AS '+tbl+	 ' on ('
				if first_tbl_flag == True:
					for pred in SELECT_MAPPING[visited[0]]:
						sql_stmt += pred+' AND '
					first_tbl_flag = False	
				for pred in SELECT_MAPPING[tbl]:
					sql_stmt += pred+' AND '

			for pred in JOIN_MAPPING[tbl]:
				pred = pred.strip()
				left = pred.split('=')[0].strip()
				right = pred.split('=')[1].strip()
				left_tbl = left.split('.')[0].strip()
				right_tbl = right.split('.')[0].strip()
				if left_tbl in visited or right_tbl in visited:
					sql_stmt += pred+' AND '
			sql_stmt = sql_stmt[:-4]+') \n'
			visited.append(tbl)
			not_visited.remove(tbl)
		sql_stmt = sql_stmt.strip()+';'

		# print(sql_stmt)
		# # w_f = open(out_path+qry+'.sql','w')
		# # w_f.write(sql_stmt)
		# # w_f.close()
		# print("#######################################################################################################")
	endTime = time.time()
	print(qry, ',', (endTime - startTime)*1000 )

