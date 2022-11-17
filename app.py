import datetime
import json

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
    df = df.where(pd.notnull(df), 0)

    df = df.rename(columns={0: 'Pick', 1: 'Team', 2: 'Record', 3: 'Win %', 4: 'GB', 5: 'Streak', 6: 'L10', 7: 'Top 4', 8: '% Chance'})
    
    # Remove any row that has a 'Team' value of 'END OF LOTTERY'
    df = df[df['Pick'] != 'END OF LOTTERY']
    
    # Remove the first row
    df = df.iloc[1:]

    # Drop the following columns: 'Record', 'Streak', 'L10', 'Top 4'
    df = df.drop(columns=['Record', 'Streak', 'L10', 'Top 4'])

    # Split the string in each row of the 'Team' column by space. If the last element of the split string is in the nba_city_abbrev dictionary, replace the value in the 'Team' column with the value in the dictionary.
    for index, row in df.iterrows():
        team = row['Team'].split(' ')
        if team[-1] in nba_city_abbrev:
            df.loc[index, 'Team'] = nba_city_abbrev[team[-1]]

    # Reset the index
    df = df.reset_index(drop=True)

    return df

def addIcons(df):
    team_icons = {
        'Atlanta': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/atlanta.png',
        'Boston': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/boston.png',
        'Brooklyn': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/brooklyn.png',
        'Charlotte': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/charlotte.png',
        'Chicago': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/chicago.png',
        'Cleveland': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/cleveland.png',
        'Dallas': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/dallas.png',
        'Denver': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/denver.png',
        'Detroit': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/detroit.png',
        'Golden State': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/golden_state.png',
        'Houston': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/houston.png',
        'Indiana': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/indiana.gif',
        'LA Clippers': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/los_angeles_clippers.png',
        'LA Lakers': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/los_angeles_lakers.png',
        'Memphis': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/memphis.png',
        'Miami': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/miami.gif',
        'Milwaukee': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/milwaukee.png',
        'Minnesota': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/minnesota.png',
        'New Orleans': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/new_orleans.png',
        'New York': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/new_york.gif',
        'Oklahoma City': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/oklahoma_city.gif',
        'Orlando': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/orlando.gif',
        'Philadelphia': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/philadelphia.png',
        'Phoenix': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/phoenix.png',
        'Portland': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/portland.png',
        'Sacramento': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/sacramento.png',
        'San Antonio': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/san-antonio.gif',
        'Toronto': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/toronto.png',
        'Utah': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/utah.png',
        'Washington': 'https://github.com/ryan-serpico/spurs-tank-watch-22/raw/main/icons/washington.png'
    }

    # Go through the 'Team' column in the dataframe and add the appropriate icon to the 'Team' column in markdown format
    for index, row in df.iterrows():
        try:
            team = row['Team']
            df.loc[index, 'Team'] = f'![{team}]({team_icons[team]})'
        except KeyError:
            continue

def get_standings():
    print('👉 Getting standings...')
    standings_table = getSoup()

    # Use pandas to read the table stored in standings_table
    df = pd.read_html(str(standings_table))[0]

    # Clean the data
    df = clean_standings(df)
    addIcons(df)

    df.to_csv('output/standings.csv', index=False)

def createMetadata():
    print('👉 Creating metadata...')
    # Save current date to variable in this format: Aug. 4, 2022
    date = datetime.datetime.now().strftime("%b. %-d, %Y")
    s = f'Data as of {date}. Teams may have more than one pick due to trades. Tied lottery teams split their odds evenly. For full list of rules that determine draft order, go to <a href="https://www.tankathon.com/">tankathon.com</a>.'
    data = {}
    
    # Create nested dictionary with metadata
    data['annotate'] = {'notes': s}

    json_data = json.dumps(data)
    with open('output/metadata.json', 'w') as f:
        f.write(json_data)

get_standings()
createMetadata()