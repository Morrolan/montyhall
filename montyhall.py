#!/usr/bin/env python

#############################################################################
#    montyhall.py - Monty Hall Problem solver
#    v0.4
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
	
	sim_id = generate_simulation_id()

	print "\nRunning simulation ID: " + str(sim_id)
	
	
	random.seed()
	
	# create a loop between 1 and number of runs
	for i in range(0, int(arg_data['runs'])):
		calculate_1_run(sim_id, arg_data)
		
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
				'runs' : None,
				'no_switch' : None,
				}

	# Create the optional arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--doors", help="Optional parameter to override number of doors.", default=3)
	parser.add_argument("-r", "--runs", help="Optional parameter to override the number of runs.", default=100)
	parser.add_argument("-s", "--switch", help="The player switches or not - enter 'y' or 'n'.")
	argu = parser.parse_args()
    
	# assign the commandline arguments to the dictionary
	arg_data['doors'] = argu.doors
	arg_data['runs'] = argu.runs
	arg_data['switch'] = argu.switch
	
	print "\nNumber of Doors:	" + str(format(int(argu.doors), ',d'))
	print "Number of Runs:		" + str(format(int(argu.runs), ',d'))
	
	if argu.switch is None:
		print "Player will randomly choose to switch."
	elif argu.switch in 'yY':
		print "Player will ALWAYS switch."
	elif argu.switch in 'nN':
		print "Player will NEVER switch."
	elif argu.switch not in 'yYnN':
		print "Invalid option specified."
		exit
	
	return arg_data
	
	
def create_table():
	cursor = CONN.cursor()
	creation_string = """
						CREATE TABLE [results] (
						[result_id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
						[simulation_id] INTEGER NOT NULL, 
						[no_of_doors] INTEGER NOT NULL, 
						[player_door] INTEGER NOT NULL, 
						[car_door] INTEGER NOT NULL, 
						[closed_door] INTEGER NOT NULL, 
						[switched] BOOLEAN NOT NULL)
						"""
	cursor.execute(creation_string)	
	

def generate_simulation_id():
	cursor = CONN.cursor()
	cursor.execute("SELECT simulation_id FROM results ORDER BY simulation_id DESC LIMIT 1")
	last_sim_id = cursor.fetchone()[0]
	
	new_sim_id = last_sim_id + 1
	
	return new_sim_id
	
	
def calculate_1_run(sim_id, arg_data):
	# Initialise all variables to be zero
	no_of_doors = int(arg_data['doors'])
	car_door = None
	player_door = None
	closed_door = None
	switch_decision = None

	# pick a door for the car
	car_door = random.randint(1, no_of_doors)
	
	# pick a door for the player
	player_door = random.randint(1, no_of_doors)
	
	# pick a door for the host to NOT open (cannot be player door)
	closed_door = random.randint(1, no_of_doors)
			
	if player_door != car_door:
		closed_door = car_door
	else:
		while closed_door == player_door:
			closed_door = random.randint(1, no_of_doors)
			
	# decide whether we switch or stick
	if arg_data['switch'] is None:
		switch_decision = random.randint(0, 1)
	elif arg_data['switch'] in 'yY':
		switch_decision = 1
	elif arg_data['switch'] in 'nN':
		switch_decision = 0
		
	
	# now lets save all of this to a database
	store_result(sim_id, no_of_doors, car_door,player_door, closed_door, switch_decision)
	
	
def store_result(simulation_id, no_of_doors, car_door,player_door, closed_door, switch_decision):
	cursor = CONN.cursor()
	cursor.execute("""INSERT INTO 'results' 
					(simulation_id, no_of_doors, car_door, player_door, closed_door, switched) 
					values (?, ?, ?, ?, ?, ?)""", (simulation_id, no_of_doors, car_door, player_door, closed_door, switch_decision))
	CONN.commit()
	
    
def produce_results(simulation_id):
	print "\n\n###################################\n"
	print "RESULTS:"
	cursor = CONN.cursor()
	cursor.execute("SELECT count(*) from results where player_door = car_door and simulation_id = {0}".format(simulation_id)
	_res = cursor.fetchone()
	_res = _res[0]
	print "\nThe player chose the car {0} times.".format(format(int(_res), 'd'))
	
	cursor.execute("SELECT count(*) from results where switched = 1 and simulation_id = {0}".format(simulation_id)
	_res = cursor.fetchone()
	_res = _res[0]    
	print "The player switched doors {0} times.".format(format(int(_res), 'd'))
    
	cursor.execute("select count(*) from results where car_door != player_door and switched = 1 and simulation_id = {0}".format(simulation_id)
	_res = cursor.fetchone()
	_result1 = _res[0]    
	
	cursor.execute("select count(*) from results where car_door == player_door and switched = 0 and simulation_id = {0}".format(simulation_id)
	_res = cursor.fetchone()
	_result2 = _res[0]
	
	_res = _result1 + _result2
	
	print "The player won the car {0} times.".format(format(int(_res), 'd'))
	
    
def main():
	begin()


######################################################

if __name__ == "__main__":
    main()
