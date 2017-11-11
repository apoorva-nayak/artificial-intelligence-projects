#!/usr/bin/python
import sys
import time
import copy
import random
import math

start = time.time()
t_end = time.time() + 60 * 4.5
t_end_bfs = time.time() + 60 * 5.0

def file_write(lizard_positions, tree_position, n):
	file_output = open('output.txt', 'w+')
	file_output.write("OK")
	file_output.write("\n")
	for i in range(0, n+1):
		output_str = ""
		for j in range(0, n+1):
			if [i, j] in tree_position:
				current_print = "2"
			elif [i,j] in lizard_positions:
				current_print = "1"
			else:
				current_print = "0"
			output_str = output_str + current_print
		if(i != n):
			file_output.write(output_str)
			file_output.write("\n")
		else:
			file_output.write(output_str)
	
def count_conflicts(lizard_positions, n, tree_position):
	count = 0
	for a in range (0, len(lizard_positions)):
		
		row = lizard_positions[a][0]
		col = lizard_positions[a][1]
		
		for i in range(row+1, n+1):
			if [i, col] in tree_position:
				break
			if [i, col] in lizard_positions:
				count = count + 1

		for i in range(row-1, -1, -1):
			if [i, col] in tree_position:
				break
			if [i, col] in lizard_positions:
				count = count + 1
		
		for j in range(col-1, -1, -1):
			if [row, j] in tree_position:
				break
			if [row, j] in lizard_positions:
				count = count + 1
		
		for j in range(col+1, n+1):
			if [row, j] in tree_position:
				break
			if [row, j] in lizard_positions:
				count = count + 1
		i = row + 1
		j = col - 1
		while i <= n and j >= 0:
			if [i, j] in tree_position:
				break
			if [i, j] in lizard_positions:
				count = count + 1
			i = i + 1
			j = j - 1
		i = row + 1
		j = col + 1
		while i <= n and j <= n:
			if [i, j] in tree_position:
				break
			if [i, j] in lizard_positions:
				count = count + 1
			i = i + 1
			j = j + 1
		i = row - 1
		j = col - 1
		while i >= 0 and j >= 0:
			if [i, j] in tree_position:
				break
			if [i, j] in lizard_positions:
				count = count + 1
			i = i - 1
			j = j - 1
		i = row - 1
		j = col + 1
		while i >= 0 and j <= n:
			if [i, j] in tree_position:
				break
			if [i, j] in lizard_positions:
				count = count + 1
			i = i - 1
			j = j + 1
	return count

def select_next_random(lizard_positions,n,tree_position):
	lizard_positions_next = copy.copy(lizard_positions)
	index = random.randrange(0, len(lizard_positions))
	val = lizard_positions[index]
	lizard_positions_next.remove(val)
	liz_random = 1
	while liz_random > 0:
		i = random.randrange(0, size_of_board)
		j = random.randrange(0, size_of_board)
		if [i, j] not in tree_position:
			if [i, j] not in lizard_positions_next:
				lizard_positions_next.append([i,j])
				liz_random = liz_random - 1
	return lizard_positions_next

def sa_algorithm(size_of_board, number_of_lizards, tree_position):
	iteration = 2
	temperature = 1 / math.log(iteration)
	end_temperature = 1
	n = size_of_board - 1
	lizard_positions = []
	if number_of_lizards > size_of_board * size_of_board - len(tree_position):
		file_output = open('output.txt', 'w+')
		file_output.write("FAIL")		
	else:
		liz_random = number_of_lizards
		while liz_random > 0:
			i = random.randrange(0, size_of_board)
			j = random.randrange(0, size_of_board)
			if [i, j] not in tree_position:
				if [i, j] not in lizard_positions:
					lizard_positions.append([i,j])
					liz_random = liz_random - 1
		conflicts_curr = count_conflicts(lizard_positions, n, tree_position)
		while temperature > 0 and time.time() < t_end:
			if conflicts_curr == 0:
				file_write(lizard_positions, tree_position, n)
				return True
			else:
				lizard_positions_next = select_next_random(lizard_positions,n,tree_position)
				conflicts_next = count_conflicts(lizard_positions_next, n, tree_position)
				conflicts_diff  = conflicts_next - conflicts_curr
				if conflicts_diff < 0:
					conflicts_curr = conflicts_next
					lizard_positions = copy.copy(lizard_positions_next)
				else:
					r = random.uniform(0, 1)
					fraction = float(conflicts_diff) / float(temperature)
					p = math.exp(-fraction)
					if (r < p):
						conflicts_curr = conflicts_next
						lizard_positions = copy.copy(lizard_positions_next)				
				temperature = 1 / math.log(iteration)
				iteration = iteration + 1		
		file_output = open('output.txt', 'w+')
		file_output.write("FAIL")
		return False

def find_valid_positions_initial(row, col, n, lizard_positions, tree_position):
	valid_positions = []
	for i in range(0, n+1):
		for j in range(0, n+1):
			if  [i,j] not in tree_position:
				valid_positions.append([i,j])
			 
	return valid_positions

def find_valid_positions_new(row, col, n, lizard_positions, old, tree_position):
	old_valid_positions = old[:]
	for i in range(row, n+1):
		if [i, col] in tree_position:
			break
		if [i, col] in old_valid_positions:
			old_valid_positions.remove([i, col])
	for i in range(row-1, -1, -1):
		if [i, col] in tree_position:
			break
		if [i, col] in old_valid_positions:
			old_valid_positions.remove([i, col])
	for j in range(col-1, -1, -1):
		if [row, j] in tree_position:
			break
		if [row, j] in old_valid_positions:
			old_valid_positions.remove([row, j])
	for j in range(col, n+1):
		if [row, j] in tree_position:
			break
		if [row, j] in old_valid_positions:
			old_valid_positions.remove([row, j])
	i = row + 1
	j = col - 1
	while i <= n and j >= 0:
		if [i, j] in tree_position:
			break
		if [i, j] in old_valid_positions:
			old_valid_positions.remove([i, j])
		i = i + 1
		j = j - 1
	i = row + 1
	j = col + 1
	while i <= n and j <= n:
		if [i, j] in tree_position:
			break
		if [i, j] in old_valid_positions:
			old_valid_positions.remove([i, j])
		i = i + 1
		j = j + 1
	i = row - 1
	j = col - 1
	while i >= 0 and j >= 0:
		if [i, j] in tree_position:
			break
		if [i, j] in old_valid_positions:
			old_valid_positions.remove([i, j])
		i = i - 1
		j = j - 1
	i = row - 1
	j = col + 1
	while i >= 0 and j <= n:
		if [i, j] in tree_position:
			break
		if [i, j] in old_valid_positions:
			old_valid_positions.remove([i, j])
		i = i - 1
		j = j + 1
	valid_positions = old_valid_positions 
	return valid_positions

def find_valid_positions_new_bfs(row, col, n, lizard_positions, tree_position, origial_valid):
	old_valid_positions = origial_valid[:]
	for l in range (0, len(lizard_positions)):
		row = lizard_positions[l][0]
		col = lizard_positions[l][1]
	
		for i in range(row, n+1):
			if [i, col] in tree_position:
				break
			if [i, col] in old_valid_positions:
				old_valid_positions.remove([i, col])
		for i in range(row-1, -1, -1):
			if [i, col] in tree_position:
				break
			if [i, col] in old_valid_positions:
				old_valid_positions.remove([i, col])
		for j in range(col-1, -1, -1):
			if [row, j] in tree_position:
				break
			if [row, j] in old_valid_positions:
				old_valid_positions.remove([row, j])
		for j in range(col, n+1):
			if [row, j] in tree_position:
				break
			if [row, j] in old_valid_positions:
				old_valid_positions.remove([row, j])
		i = row + 1
		j = col - 1
		while i <= n and j >= 0:
			if [i, j] in tree_position:
				break
			if [i, j] in old_valid_positions:
				old_valid_positions.remove([i, j])
			i = i + 1
			j = j - 1
		i = row + 1
		j = col + 1
		while i <= n and j <= n:
			if [i, j] in tree_position:
				break
			if [i, j] in old_valid_positions:
				old_valid_positions.remove([i, j])
			i = i + 1
			j = j + 1
		i = row - 1
		j = col - 1
		while i >= 0 and j >= 0:
			if [i, j] in tree_position:
				break
			if [i, j] in old_valid_positions:
				old_valid_positions.remove([i, j])
			i = i - 1
			j = j - 1
		i = row - 1
		j = col + 1
		while i >= 0 and j <= n:
			if [i, j] in tree_position:
				break
			if [i, j] in old_valid_positions:
				old_valid_positions.remove([i, j])
			i = i - 1
			j = j + 1
	valid_positions = old_valid_positions[:]
	return valid_positions

def recursive_dfs(row, col, n, valid_positions, lizard_positions, number_of_lizards, lizards_placed, tree_position, cum_tree_dict):
	
	if time.time() > t_end:
		return False
	
	if lizards_placed == 0:
		valid_positions = find_valid_positions_initial(row, col, n, lizard_positions, tree_position)
	else:
		old_valid = valid_positions[:]
		valid_positions = find_valid_positions_new(row, col, n, lizard_positions, old_valid, tree_position)

	if (number_of_lizards - lizards_placed) > len(valid_positions):
		return False
	
	for vp in range(0, len(valid_positions)):
		if(n - valid_positions[vp][0] + 1 + cum_tree_dict[valid_positions[vp][0]]) < (number_of_lizards - lizards_placed):
			return False
		lizard_positions.append(valid_positions[vp])
		lizards_placed = lizards_placed + 1
		
		if lizards_placed == number_of_lizards:
			file_write(lizard_positions, tree_position, n)
			return True	
		else:
			if(recursive_dfs(valid_positions[vp][0], valid_positions[vp][1], n, valid_positions, lizard_positions, number_of_lizards, lizards_placed, tree_position, cum_tree_dict) == True):
				return True
			else:
				a = len(lizard_positions)
				lizard_positions.remove(lizard_positions[a-1])
				lizards_placed = lizards_placed - 1
	return False
	
def bfs_implement(row, col, n, valid_positions, number_of_lizards, tree_position, node_queue_dict, next_node_count, origial_valid, cum_tree_dict):
	i = 0
	while i in node_queue_dict and time.time() < t_end_bfs:
		curr_node_details = node_queue_dict[i]
		del node_queue_dict[i]
		node_to_be_expanded = curr_node_details[0]
		parent_node = i
		lizard_placed = curr_node_details[2]
		lizard_positions_init = curr_node_details[3]
		lizard_positions = lizard_positions_init[:]
		if lizard_placed == number_of_lizards:
			file_write(lizard_positions, tree_position, n)
			return True
		else:
			valid_positions = find_valid_positions_new_bfs(node_to_be_expanded[0], node_to_be_expanded[1], n, lizard_positions, tree_position, origial_valid)
			for j in range (0, len(valid_positions)):
				if (n - valid_positions[j][0] + 1 + cum_tree_dict[valid_positions[j][0]]) >= (number_of_lizards - lizard_placed):
					next_node_count = next_node_count + 1
					lizard_positions = []
					lizard_positions = lizard_positions_init[:]
					lizard_positions.append(valid_positions[j])
					node_queue_dict[next_node_count] = (valid_positions[j], parent_node, lizard_placed + 1, lizard_positions)			
		i = i + 1
	return False

def dfs_algorithm(size_of_board, number_of_lizards, tree_position, cum_tree_dict):
	lizard_positions = []
	valid_positions = []
	lizards_placed = 0
	row = 0
	col = 0
	a = recursive_dfs(row, col, size_of_board - 1, valid_positions, lizard_positions, number_of_lizards, lizards_placed, tree_position, cum_tree_dict)
	if a == False:
		file_output = open('output.txt', 'w+')
		file_output.write("FAIL")	
	
def bfs_algorithm(size_of_board, number_of_lizards, tree_position, cum_tree_dict):
	lizard_positions = []
	valid_positions = []
	row = 0
	col = 0
	parent_node_liz_count = 0
	parent_node = 0
	valid_position_dict = {}
	
	valid_positions = find_valid_positions_initial(row, col, size_of_board - 1, lizard_positions, tree_position)	
	node_queue_dict = {}
	for i in range (0, len(valid_positions)):
		lizard_positions = []
		lizard_positions.append(valid_positions[i])
		node_queue_dict[i] = (valid_positions[i], parent_node, 1, lizard_positions)
	next_node_count = i
	origial_valid = valid_positions[:]
	a = bfs_implement(row, col, size_of_board - 1, valid_positions, number_of_lizards, tree_position, node_queue_dict, next_node_count, origial_valid, cum_tree_dict)
	if a == False:
		file_output = open('output.txt', 'w+')
		file_output.write("FAIL")
	return a

file_input = open('input.txt', 'r')
file_output = open('output.txt', 'w+')
search_algorithm = file_input.readline().strip()
size_of_board = int(file_input.readline().strip())
number_of_lizards = int(file_input.readline().strip())
initialize_nursery = []
tree_position = []
row = 0
col = 0
tree_dict = {}
for line in file_input.readlines():
	line = line.replace("\n", "")
	line = line.replace("\t", "")
	line = line.replace("\r", "")
	line = line.replace(" ", "")
	tree_dict[row] = 0
	for i in range (0, len(line)):
		if line[i] == '2':
			tree_position.append([row,i])
			tree_dict[row] = tree_dict[row] + 1
	row = row + 1	

sum_now = 0
cum_tree_dict = {}
for ind in range (row-1, -1, -1):
	sum_now = sum_now + tree_dict[ind]
	cum_tree_dict[ind] = sum_now

if len(tree_position) == 0 and number_of_lizards > size_of_board:
	file_output.write("FAIL")
	sys.exit()
	
if number_of_lizards > size_of_board * size_of_board - len(tree_position):
		file_output = open('output.txt', 'w+')
		file_output.write("FAIL")
		sys.exit()

if search_algorithm == "DFS":
	dfs_algorithm(size_of_board, number_of_lizards, tree_position, cum_tree_dict)

elif search_algorithm == "BFS":
	a = bfs_algorithm(size_of_board, number_of_lizards, tree_position, cum_tree_dict)

elif search_algorithm == "SA":
	a = sa_algorithm(size_of_board, number_of_lizards, tree_position)
		
print time.time()-start
