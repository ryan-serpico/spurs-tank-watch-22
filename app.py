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
        'Atlanta': 'icons/atlanta.png',
        'Boston': 'icons/boston.png',
        'Brooklyn': 'icons/brooklyn.png',
        'Charlotte': 'icons/charlotte.png',
        'Chicago': 'icons/chicago.png',
        'Cleveland': 'icons/cleveland.png',
        'Dallas': 'icons/dallas.png',
        'Denver': 'icons/denver.png',
        'Detroit': 'icons/detroit.png',
        'Golden State': 'icons/golden_state.png',
        'Houston': 'icons/houston.png',
        'Indiana': 'icons/indiana.gif',
        'LA Clippers': 'icons/los_angeles_clippers.png',
        'LA Lakers': 'icons/los_angeles_lakers.png',
        'Memphis': 'icons/memphis.png',
        'Miami': 'icons/miami.png',
        'Milwaukee': 'icons/milwaukee.png',
        'Minnesota': 'icons/minnesota.png',
        'New Orleans': 'icons/new_orleans.png',
        'New York': 'icons/new_york.gif',
        'Oklahoma City': 'icons/oklahoma_city.gif',
        'Orlando': 'icons/orlando.gif',
        'Philadelphia': 'icons/philadelphia.png',
        'Phoenix': 'icons/phoenix.png',
        'Portland': 'icons/portland.png',
        'Sacramento': 'icons/sacramento.png',
        'San Antonio': 'icons/san-antonio.gif',
        'Toronto': 'icons/toronto.png',
        'Utah': 'icons/utah.png',
        'Washington': 'icons/washington.png'
    }

    # Go through the 'Team' column in the dataframe and add the appropriate icon to the 'Team' column in markdown format
    for index, row in df.iterrows():
        try:
            team = row['Team']
            df.loc[index, 'Team'] = f'![{team}]({team_icons[team]})'
        except KeyError:
            continue

def get_standings():
    standings_table = getSoup()

    # Use pandas to read the table stored in standings_table
    df = pd.read_html(str(standings_table))[0]

    # Clean the data
    df = clean_standings(df)
    addIcons(df)

    print(df)

get_standings()