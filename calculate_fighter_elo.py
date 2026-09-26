import pandas as pd
import numpy as np
import csv


# Before this point we have only used pythons built-in csv module to create and read
# CSV files. But now we need to use Pandas as we will be calculating the Elo of UFC
# fighters and making rapid modifications to a file.

# Make a dictionary with each fighter, there unique id and the number it corresponds to in a df

'''
for fight in fight_results
    search for fighters in fighters_elos
    if not in add them, base elo
    get fighters elo
    calculate new elo
    replace new elo

for fight in fight results
    get fighters elo
    calculate new fighter elo
    update fighter elo

'''

# Now what would be appropriate for O(1) lookup time would be to use a Hash map with the
# fighter ids as a key and the index of the fighter as a 

fighters_dict = {}

def calculate_elo(win_current_elo, lose_current_elo):


    return  0 #win_new_elo, lose_new_elo


with open("all_fights_results_desc.csv", "r") as fights_results:
    results_reader = csv.reader(fights_results)
    header = next(results_reader)

    for row in results_reader:
        win_fighter_id = row[1]
        lose_fighter_id = row[3]

        win_fighter_elo = fighters_dict.get(win_fighter_id)
        if win_fighter_elo == None: # If .get gives None then the fighter id is not in fighters_dict
            win_fighter_elo = 1000
        
        lose_fighter_elo = fighters_dict.get(lose_fighter_id)
        if lose_fighter_elo == None:
            lose_fighter_elo = 1000
        
        calculate_elo(win_fighter_elo, lose_fighter_elo)

#https://stats.stackexchange.com/questions/219319/what-statistical-test-to-use-comparing-models


def multiply(a, b):
    return a * b

multiply(2, 3)
