#!/usr/bin/env python
# coding: utf-8

# In[23]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
from selenium.webdriver.common.by import By

os.chdir(r'C:\Users\user\Documents\geckoDriver') # May have to change this path
driver = webdriver.Firefox()
driver.implicitly_wait(30)

# Download the ODI JSONs file
cricURL = 'https://cricsheet.org/'
driver.get(cricURL)

cricMatches = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[1]/p/a[1]')

cricMatches.click()

odiJSON = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/dl/dd[4]/a[1]')

odiJSON.click()

driver.quit()


# In[24]:


from zipfile import ZipFile

# Unzip the Zipped JSON Folder
with ZipFile('C:\\Users\\user\\Downloads\\odis_json.zip', 'r') as f:  # May have to change this path
    f.extractall('C:\\Users\\user\\Downloads\\odis_json')  # May have to change this path


# In[21]:


import sqlite3
import json
import os


# In[22]:


# Specify the folder path containing the JSON files
folder_path = 'C:\\Users\\user\\Downloads\\odis_json'  # May have to change this path

# Get a list of files in the folder
file_list = os.listdir(folder_path)


# In[17]:


# Connect to SQLite database
conn = sqlite3.connect('E:\AK-Interview-2023\Zelus\zelusdatabase.db') # May have to change this path
cursor = conn.cursor()

# Create a table to store the Match Details Data (match results)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS odi_match_details (
        match_date date,
        venue TEXT,
        event TEXT,
        match_number TEXT,
        gender TEXT,
        winner TEXT,
        player_of_match TEXT,
        team1 TEXT,
        team2 TEXT,
        margin_runs INTEGER,
        margin_wickets INTEGER,
        result TEXT
    )
''')

# Create a table to store the Team Details (universe of players)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS odi_team_details (
        team_name TEXT,
        player_name TEXT,
        PRIMARY KEY (team_name, player_name)
    )
''')

# Create a table to store the Ball-2-Ball Innings Data (ball-by-ball innings data)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS odi_ball_to_ball_details (
        match_date DATE,
        venue TEXT,
        event TEXT,
        batting_team TEXT,
        overs INTEGER,
        detailed_overs REAL,
        batter TEXT,
        bowler TEXT,
        non_striker TEXT,
        batter_runs INTEGER,
        extra_runs INTEGER,
        total_runs INTEGER,
        wickets INTEGER,
        byes INTEGER, 
        noballs INTEGER, 
        wides INTEGER
    )
''')


# In[18]:


# Iterate over each file in the folder
for file_name in file_list:
    # Check if the file is a JSON file
    if file_name.endswith('.json'):
        # Construct the file path
        file_path = os.path.join(folder_path, file_name)
        
        # Read JSON data from file
        with open(file_path, 'r') as file:
            json_data = file.read()
        
        print(file_path)
        
        # Parse JSON data
        data = json.loads(json_data)
        
        # Extract match information
        match_date = data["info"]["dates"][0]
        match_venue = data["info"]["venue"]
        
        if "event" in data["info"]:
            match_event = data["info"]["event"]["name"]
            if "match_number" in data["info"]["event"]:
                match_number = data["info"]["event"]["match_number"]
            else:
                match_number = data["info"]["match_type_number"]
        else:
            match_event = "None"
        
        
        print( "On " + match_date + ", today's event is " + match_event + " at " + match_venue )

        match_gender = data["info"]["gender"]
        match_team1 = data["info"]["teams"][0]
        match_team2 = data["info"]["teams"][1]
        
        # Check if a ["player_of_match"] is present
        if "missing" in data["info"]:
            for element in data["info"]["missing"]:
                if element == "player_of_match":
                    player_of_match = "None"
        elif "player_of_match" not in data["info"]:
            player_of_match = "None"
        else:
            player_of_match = data["info"]["player_of_match"][0]
        
        # Check if a ["info"]["outcome"]["winner"] is present
        if "outcome" in data["info"] and "winner" in data["info"]["outcome"]:
            match_winner = data["info"]["outcome"]["winner"]
            # Check if the win result is by runs or by wickets
            if "by" in data["info"]["outcome"] and "runs" in data["info"]["outcome"]["by"]:
                match_margin_runs = data["info"]["outcome"]["by"]["runs"]
                match_margin_wickets = 0
            else:
                match_margin_runs = 0
                match_margin_wickets = data["info"]["outcome"]["by"]["wickets"]
            # Check if the result is by D/L from ["info"]["outcome"]["method"] key
            if "method" in data["info"]["outcome"]:
                match_result = data["info"]["outcome"]["method"]
            else:
                match_result = "Completed"
        
        else:
            # Key is not present
            match_winner = "None"
            match_margin_runs = 0
            match_margin_wickets = 0
            player_of_match = "None"
            match_result = data["info"]["outcome"]["result"]
        
        # Insert into the odi_match_details table
        cursor.execute("INSERT INTO odi_match_details (match_date, venue, event, match_number, gender, winner, player_of_match, team1, team2, margin_runs, margin_wickets, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (match_date, match_venue, match_event, match_number, match_gender, match_winner, player_of_match, match_team1, match_team2, match_margin_runs, match_margin_wickets, match_result))
        
        # Extract team players
        team_players = {}
        teams = data["info"]["teams"]
        for team in teams:
            players = data["info"]["players"][team]
            team_players[team] = players
        
        # Insert/Replace into the odi_team_details table, regarding Team name and Team players.
        for team, players in team_players.items():
            for player in players:
                cursor.execute("INSERT OR REPLACE INTO odi_team_details (team_name, player_name) VALUES (?, ?)", (team, player))
        
        # Extract ball-by-ball innings data
        innings = data["innings"]
        for inning in innings:
            team_name = inning["team"]
            overs = inning["overs"]
            
            for over in overs:
                over_number = over["over"]
                deliveries = over["deliveries"]
                i = 0
                
                for delivery in deliveries:
                    byes = noballs = wides = wickets = 0
                    batter = delivery["batter"]
                    bowler = delivery["bowler"]
                    non_striker = delivery["non_striker"]
                    runs = delivery["runs"]
                    batter_runs = runs["batter"]
                    extras = runs["extras"]
                    total_runs = runs["total"]
                    if "extras" in delivery:
                        if "legbyes" in delivery["extras"]:
                            byes = delivery["extras"]["legbyes"]
                        elif "byes" in delivery["extras"]:
                            byes = delivery["extras"]["byes"]
                        elif "wides" in delivery["extras"]:
                            wides = delivery["extras"]["wides"]
                        elif "noballs" in delivery["extras"]:
                            noballs = delivery["extras"]["noballs"]
                    if "wickets" in delivery:
                        wickets = wickets+1
                    i = i+1
                    # Insert into the odi_ball_to_ball_details table
                    cursor.execute("INSERT INTO odi_ball_to_ball_details (match_date, venue, event, batting_team, overs, detailed_overs, batter, bowler, non_striker, batter_runs, extra_runs, total_runs, wickets, byes, noballs, wides) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (match_date, match_venue, match_event, team_name, over_number, (str(over_number)+"."+str(i)), batter, bowler, non_striker, batter_runs, extras, total_runs, wickets, byes, noballs, wides))
        print( "Insert completed for " + match_date + ", event is " + match_event + " at " + match_venue )


# In[19]:


conn.commit()


# In[20]:


conn.close()


# In[ ]:




