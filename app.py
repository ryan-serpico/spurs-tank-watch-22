import pandas as pd
import requests
from bs4 import BeautifulSoup


def getSoup():
    """
    In this function we're isolating the table we want to scrape and removing extraneous HTML elements.
    """

    url = 'https://www.tankathon.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    standings_table = soup.find('table', {'class': 'draft-board'})

    # Remove td elements with class 'mobile'
    for td in standings_table.find_all('td', {'class': 'mobile'}):
        td.decompose()

    for div in standings_table.find_all('div', {'class': 'mobile'}):
        div.decompose()


    return standings_table

def clean_standings(standings_table):
    nba_city_abbrev = {
        'ATL': 'Atlanta',
        'BOS': 'Boston',
        'BKN': 'Brooklyn',
        'CHA': 'Charlotte',
        'CHI': 'Chicago',
        'CLE': 'Cleveland',
        'DAL': 'Dallas',
        'DEN': 'Denver',
        'DET': 'Detroit',
        'GSW': 'Golden State',
        'HOU': 'Houston',
        'IND': 'Indiana',
        'LAC': 'LA Clippers',
        'LAL': 'LA Lakers',
        'MEM': 'Memphis',
        'MIA': 'Miami',
        'MIL': 'Milwaukee',
        'MIN': 'Minnesota',
        'NO': 'New Orleans',
        'NY': 'New York',
        'OKC': 'Oklahoma City',
        'ORL': 'Orlando',
        'PHI': 'Philadelphia',
        'PHX': 'Phoenix',
        'POR': 'Portland',
        'SAC': 'Sacramento',
        'SAS': 'San Antonio',
        'TOR': 'Toronto',
        'UTA': 'Utah',
        'WAS': 'Washington'
    }

    df = standings_table

    # Remove empty rows
    df = df.dropna(how='all')

    # Remove the last three columns
    df = df.iloc[:, :-3]

    #  If value in any of the last two columns is NaN, replace with None
    df = df.where(pd.notnull(df), None)

    df = df.rename(columns={0: 'Pick', 1: 'Team', 2: 'Record', 3: 'Win%', 4: 'GB', 5: 'Streak', 6: 'L10', 7: 'Top 4', 8: '#1 Ovr'})
    
    # Remove the first row
    df = df.iloc[1:]

    # Split the string in each row of the 'Team' column by space. If the last element of the split string is in the nba_city_abbrev dictionary, replace the value in the 'Team' column with the value in the dictionary.
    for index, row in df.iterrows():
        team = row['Team'].split(' ')
        if team[-1] in nba_city_abbrev:
            df.loc[index, 'Team'] = nba_city_abbrev[team[-1]]

    print(df)

def get_standings():
    standings_table = getSoup()

    # Use pandas to read the table stored in standings_table
    df = pd.read_html(str(standings_table))[0]

    # Clean the data
    clean_standings(df)

get_standings()