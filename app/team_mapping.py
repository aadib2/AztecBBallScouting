import requests
import pandas as pd
from bs4 import BeautifulSoup

# read table from html
url = "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_basketball_programs"
teams_df = pd.read_html(url, attrs={"class":"wikitable"})[0]

# print out first 5 teams
#print(teams_df.head())

# clean up team names
teams_df['School'] = (teams_df['School']
    .str.replace(r'\s*\([^)]*\)', '', regex=True) # remove the parenthetical stuff
    .str.replace(r'\[.*?\]', '', regex=True) # remove the bracketed stuff (superscripts/subscripts)
    .str.strip()) # remove any trailing whitespace

#print(teams_df.tail(10))
print(teams_df.shape) # total 364 DIV 1 Teams

# now map each team name to it's corresponding team ID
team_mapping = {i+1: row['School'] for i, row in teams_df.iterrows()}

# print out first 5 teams
for k, v in list(team_mapping.items())[:5]:
    print(k, ":", v)


''' Prints: 
1 : University at Albany, SUNY
2 : Binghamton University
3 : Bryant University
4 : University of Maine
5 : University of Maryland, Baltimore County
'''

print("\nteam_id 250 maps to", team_mapping[250]) # returns Wagner College

# invert the map so can look up team id, given name
team_mapping_inv = {v: k for k,v in team_mapping.items()}

# now given a team name, can search for its corresponding id
print("SDSU team_id is", team_mapping_inv['San Diego State University']) # returns 237








