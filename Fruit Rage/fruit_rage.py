#!/usr/bin/python
import sys
import time
import copy
import random
import math

start = time.time()

def file_write(board_state_after_gravity, max_position):
	row = max_position[0][0]
	col = max_position[0][1]
	str_output = chr(65 + col)
	str_output = str_output + str(row + 1)
	file_output.write(str_output)
	file_output.write("\n")
	for i in range(0, len(board_state_after_gravity)):
		str_output = ""
		for j in range(0, len(board_state_after_gravity[i])):
			str_output = str_output + str(board_state_after_gravity[i][j])
		if(i != (len(board_state_after_gravity) - 1)):
			file_output.write(str_output)
			file_output.write("\n")
		else:
			file_output.write(str_output)
			
def find_best_move(board_state, max_depth, time_remaining_given):
	main_dict, main_list = find_consecutive_fruit_counts(board_state)
	alpha = float("-inf")
	beta = float("inf")
	best_score = float("-inf")
	best_key = main_list[0]
	
	#Calibrate depth based on time remaining
	if len(main_list) >= 500:
		if time_remaining_given < 200:
			max_depth = 0
	
	elif len(main_list) >= 350:		
		if time_remaining_given < 150:
			max_depth = 0
	
	elif len(main_list) >= 200:		
		if time_remaining_given < 125:
			max_depth = 0
	
	elif len(main_list) >= 100:		
		if time_remaining_given < 100:
			max_depth = 0

	for ml in main_list:
		if time_remaining_given*0.9 < time.time()-start:
			return main_dict[best_key]
		key = ml
		cloned_board_state = copy.deepcopy(board_state)
		val = main_dict[key]
		cloned_board_state = gravity_effect(cloned_board_state, val)
		score = minimax(cloned_board_state, 1, False, len(val) * len(val), alpha, beta, max_depth)
		if score > alpha:
			best_key = key
			alpha = score
	return main_dict[best_key]
		
def evaluation_function(board_state, isMax, points):
	main_dict, main_list = find_consecutive_fruit_counts(board_state)
	cloned_board_state = copy.deepcopy(board_state)
	count_fruits = len(main_dict[main_list[0]])
	if isMax:
		return (points + count_fruits*count_fruits)
	else:
		return (points - count_fruits*count_fruits)

def minimax(board_state, depth, isMax, points, alpha, beta, max_depth):
	if check_board_empty(board_state):
		return points
	
	if depth > max_depth:
		return evaluation_function(board_state, isMax, points)
	
	if isMax:
		if depth > max_depth:
			return evaluation_function(board_state, isMax, points)
			
        	best_score = float('-inf')
        	main_dict, main_list = find_consecutive_fruit_counts(board_state)
		for ml in main_list:
			key = ml
			cloned_board_state = copy.deepcopy(board_state)
			val = main_dict[key]
			cloned_board_state = gravity_effect(cloned_board_state, val)
            		best_score = max(best_score, minimax(cloned_board_state, depth+1, False, points+(len(val) * len(val)), alpha, beta, max_depth))
            		if best_score >= beta:
            			return best_score
                		break
                	alpha = max(alpha, best_score)
        	return best_score
    	else:
        	if depth > max_depth:
			return evaluation_function(board_state, isMax, points)
        	best_score = float('inf')
        	main_dict, main_list = find_consecutive_fruit_counts(board_state)
		for ml in main_list:
			key = ml
			cloned_board_state = copy.deepcopy(board_state)
			val = main_dict[key]
			cloned_board_state = gravity_effect(cloned_board_state, val)
        	    	best_score = min(best_score, minimax(cloned_board_state, depth+1, True, points-(len(val) * len(val)), alpha, beta, max_depth))
            		if best_score <= alpha:
            			return best_score
                		break
                	beta = min(beta, best_score)
        	return best_score


def find_consecutive_fruit_counts(board_state):
	main_list = []
	main_dict = {}
	l = 0
	length_of_max_list = 0
	index_to_win = -1
	for i in range(0, len(board_state)):
		for j in range(0, len(board_state[i])):
			current_list = []
			if (board_state[i][j] != "*") and ([i, j] not in main_list):
				current_list.append([i, j])
				main_list.append([i, j])
				current_fruit = board_state[i][j]
				ind = 0
				k = 0
				while k < len(current_list):
					row = current_list[k][0]
					col = current_list[k][1]
					if (row - 1) >= 0:
						if (board_state[row-1][col] != "*") and (board_state[row-1][col] == current_fruit) and ([row-1, col] not in current_list):
							current_list.append([row-1,col])
							main_list.append([row-1,col])
					if (row + 1) < len(board_state):
						if (board_state[row+1][col] != "*") and (board_state[row+1][col] == current_fruit) and ([row+1, col] not in current_list):
							current_list.append([row+1,col])
							main_list.append([row+1,col])
					if (col - 1) >= 0:
						if (board_state[row][col-1] != "*") and (board_state[row][col-1] == current_fruit) and ([row, col-1] not in current_list):
							current_list.append([row,col-1])
							main_list.append([row,col-1])
					if (col + 1) < len(board_state):
						if (board_state[row][col+1] != "*") and (board_state[row][col+1] == current_fruit) and ([row, col+1] not in current_list):
							current_list.append([row,col+1])
							main_list.append([row,col+1])
					k = k + 1
				main_dict[l] = current_list
				current_list = []
				l = l + 1
	main_list = []
	for w in sorted(main_dict.items(), key=lambda v: len(v[1]), reverse=True):
		main_list.append(w[0])
	return main_dict, main_list 

def check_board_empty(board_state_after_gravity):
	for i in range (0, len(board_state_after_gravity)):
		for j in range (0, len(board_state_after_gravity[i])):
			if board_state_after_gravity[i][j] != "*":
				return False
	return True
				
def gravity_effect(board_state, max_position):
	board_state_after_gravity = board_state[:]
	for i in range (0, len(max_position)):
		row = max_position[i][0]
		col = max_position[i][1]
		board_state_after_gravity[row][col] = "*"
	max_position.sort(key=lambda x:(x[1], x[0]))
	num_col = len(board_state)
	for i in range (len(max_position) - 1, -1, -1):
		row = max_position[i][0]
		col = max_position[i][1]
		if num_col > col:
			num_col = col
			current_row = row
			row = row - 1
			while row > -1:
				if board_state_after_gravity[row][col] != "*":
					board_state_after_gravity[current_row][col] = board_state_after_gravity[row][col]
					board_state_after_gravity[row][col] = "*"
					current_row = current_row - 1
				row = row - 1
	return board_state_after_gravity 

file_input = open('input.txt', 'r')
file_output = open('output.txt', 'w+')
size_of_board = int(file_input.readline().strip())
number_of_fruits = int(file_input.readline().strip())
time_remaining_given = float(file_input.readline().strip())
board_state = []
for line in file_input.readlines():
	line = line.replace("\n", "")
	line = line.replace("\t", "")
	line = line.replace("\r", "")
	line = line.replace(" ", "")
	each_row = []
	for i in range (0, len(line)):
		if line[i] != "*":
			each_row.append(int(line[i]))
		else:
			each_row.append(line[i])
	board_state.append(each_row)

max_turn = 1
temp = []
alpha = float("-inf")
beta = float("inf")
max_depth = 1
original_board_state =  copy.deepcopy(board_state)
best_key = find_best_move(board_state, max_depth, time_remaining_given)
board_state_after_gravity = gravity_effect(original_board_state, best_key)
file_write(board_state_after_gravity, best_key)
print time.time()-start
