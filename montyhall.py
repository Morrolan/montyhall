#!/usr/bin/env python

#############################################################################
#    montyhall.py - Monty Hall Problem solver
#    Copyright (C) 2013  Ian Havelock
#
#   //http://en.wikipedia.org/wiki/Monty_Hall_problem
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################


# IMPORTS ###################################################################
import sqlite3
import random
import argparse

# THIRD PARTY IMPORTS #######################################################


# PARTICULAR IMPORTS ########################################################
from datetime import datetime

# CONSTANTS #################################################################

# the name of our SQLite database
CONN = sqlite3.connect('montyhall.sqlite3')

# VARIABLES #################################################################


# FUNCTIONS #################################################################

def begin():
	print "\n\n###########################"
	print "Monty Hall Problem Solver"
	print "Morrolan 2013"
	print "###########################"

	arg_data = get_args()
	truncate_table()
	
	print "\nRunning simulation..."
	
	random.seed()
	
	# create a loop between 1 and number of runs
	for i in range(0, int(arg_data['runs'])):
		calculate_1_run(arg_data)
		
	print "\nFinished!"
	
	produce_results()
	# now lets analyze the results here
	CONN.close()

	
def get_args():
	"""Get the commandline arguments and parameters if defaults overridden."""
	
	# create a dictionary containing the argument data so it is easier to pass
	# to other functions.
	arg_data = {
				'doors' : None,
				'runs' : None
				}

	# Create the optional arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--doors", help="Optional parameter to override number of doors.", default=3)
	parser.add_argument("-r", "--runs", help="Optional parameter to override the number of runs.", default=100)
	argu = parser.parse_args()
    
	# assign the commandline arguments to the dictionary
	arg_data['doors'] = argu.doors
	arg_data['runs'] = argu.runs
	
	print "\nNumber of Doors:	" + str(format(int(argu.doors), ',d'))
	print "Number of Runs:		" + str(format(int(argu.runs), ',d'))
	return arg_data

	
def truncate_table():
	"""If the table exists, we want to truncate it.  Eventually we will replace
		this and we will assign a 'simulation ID' to each row so we can easily
		determine which simulation each row of data belongs to."""
		
	cursor = CONN.cursor()
	check_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='results'"
	cursor.execute(check_string)
	_result = cursor.fetchone()

	
	if _result is not None:
		if 'results' in _result:
			print "\nTruncating table 'results'..."
			
			truncate_string = "delete from results"
			cursor.execute(truncate_string)
	else:
		print "\nTable 'results' does not exist - creating structure..."
        	create_table()
		
	
def create_table():
	cursor = CONN.cursor()
	# creation_string = """
						# CREATE TABLE [results] (
						# [result_id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
						# [no_of_doors] INTEGER NOT NULL, 
						# [player_door] INTEGER NOT NULL, 
						# [car_door] INTEGER NOT NULL, 
						# [closed_door] INTEGER NOT NULL,
						# [switched] BOOLEAN NOT NULL,
						# [won_car] BOOLEAN NOT NULL)
						# """
						
	creation_string = """
						CREATE TABLE [results] (
						[result_id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
						[no_of_doors] INTEGER NOT NULL, 
						[player_door] INTEGER NOT NULL, 
						[car_door] INTEGER NOT NULL, 
						[closed_door] INTEGER NOT NULL,
						[switched] BOOLEAN NOT NULL)
						"""
	cursor.execute(creation_string)	
	

def calculate_1_run(arg_data):
	# Initialise all variables to be zero
	no_of_doors = int(arg_data['doors'])
	car_door = None
	player_door = None
	closed_door = None
	switch_decision = None
	won_car = None

	# pick a door for the car
	car_door = random.randint(1, no_of_doors)
	#print car_door
	
	# pick a door for the player
	player_door = random.randint(1, no_of_doors)
	#print player_door
	
	# pick a door for the host to NOT open (cannot be player door)
	closed_door = random.randint(1, no_of_doors)
			
	if player_door != car_door:
		closed_door = car_door
	else:
		while closed_door == player_door:
			closed_door = random.randint(1, no_of_doors)
			
	# decide whether we switch or stick
	switch_decision = random.randint(0, 1)
	
	# # won the car or not?
	# if player_door == car_door and switch_decision == 0:
		# won_car = 1
	# elif player_door == car_door and switch_decision == 1:
		# won_car = 0
	# elif player_door != car_door and switch_decision == 0:
		# won_car = 0
	# elif player_door != car_door and switch_decision == 1:
		# won_car = 1
		
	
	# now lets save all of this to a database
	#store_result(no_of_doors, car_door,player_door, closed_door, switch_decision, won_car)
	store_result(no_of_doors, car_door,player_door, closed_door, switch_decision)
	
	
def store_result(no_of_doors, car_door,player_door, closed_door, switch_decision):
	cursor = CONN.cursor()
	cursor.execute("""INSERT INTO 'results' 
					(no_of_doors, car_door, player_door, closed_door, switched) 
					values (?, ?, ?, ?, ?)""", (no_of_doors, car_door, player_door, closed_door, switch_decision))
	CONN.commit()
	
# def store_result(no_of_doors, car_door,player_door, closed_door, switch_decision, won_car):
	# cursor = CONN.cursor()
	# cursor.execute("""INSERT INTO 'results' 
					# (no_of_doors, car_door, player_door, closed_door, switched, won_car) 
					# values (?, ?, ?, ?, ?, ?)""", (no_of_doors, car_door, player_door, closed_door, switch_decision, won_car))
	# CONN.commit()
	
    
def produce_results():
    print "\n\n###################################\n"
    print "RESULTS:"
    cursor = CONN.cursor()
    cursor.execute("SELECT count(*) from results where player_door = car_door")
    _res = cursor.fetchone()
    _res = _res[0]
    print "\nThe player chose the car {0} times.".format(format(int(_res), 'd'))
	
    cursor.execute("SELECT count(*) from results where switched = 1")
    _res = cursor.fetchone()
    _res = _res[0]    
    print "The player switched doors {0} times.".format(format(int(_res), 'd'))
    
    # cursor.execute("SELECT count(*) from results where won_car = 1")
    # _res = cursor.fetchone()
    # _res = _res[0]  
    # print "The player won the car {0} times.".format(format(int(_res), 'd'))
    
    print "\n"
    
def main():
	begin()


######################################################

if __name__ == "__main__":
    main()
