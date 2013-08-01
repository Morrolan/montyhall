montyhall
=========

Monty Hall Problem Solver

The Monty Hall problem is a probability puzzle, loosely based on the American television game show Let's Make a Deal and named after the show's original host, Monty Hall. (http://en.wikipedia.org/wiki/Monty_Hall_problem).

The question posed is:

_Suppose you're on a game show, and you're given the choice of three doors: Behind one door is a car; behind the others, goats. You pick a door, say No. 1, and the host, who knows what's behind the doors, opens another door, say No. 3, which has a goat. He then says to you, "Do you want to pick door No. 2?" Is it to your advantage to switch your choice?_

montyhall is a Python script that allows you to run through an arbitrary number of "episodes" of the game show, defining various parameters to prove the mathematics.

However, there are certain criteria that are assumed:

* The door(s) that the host opens ALWAYS contain Goats - the host never reveals the car.
* All but 1 doors are opened by the host (if overriding the default 3 doors).
* 

The default parameters are as such:

* 3 doors.
* Player tosses a coin to decide whether to switch or not (ignoring a-priori information).
* 100 "episodes" or plays of the game.

All results are written to a SQLite3 table which will be created in the same directory that the script is run from.


| Parameter     | Description   | Default  |
| ------------- |---------------| -----:|
| -d, --doors | Optional parameter to override number of doors. | 3 |
| -r, --runs | Optional parameter to override the number of runs. | 100 |
| -s, --switch | The player switches or not - enter 'y' or 'n'. | Random |

To demonstrate how to run the simulation overriding all defaults:


```
 > python montyhall.py --switch y --doors 5 --runs 10000 
```

By default, the player decides to switch doors based on the toss of a die, i.e. a 0 or 1 probability chance.  However, this essentially means that the player is ignoring the a-priori information from the host(stupid player).  In order to actually test the probability taking the a-priori information into account, you need to override the decision with the -s parameter.
