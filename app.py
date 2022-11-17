import pandas as pd


def get_standings():

    url = 'https://www.basketball-reference.com/leagues/NBA_2023.html'
    east_standings_df = pd.read_html(url)[0]
    west_standings_df = pd.read_html(url)[1]
    
    east_standings_df.rename(columns={'Eastern Conference': 'Team'}, inplace=True)
    west_standings_df.rename(columns={'Western Conference': 'Team'}, inplace=True)
    
    standings_df = pd.concat([east_standings_df, west_standings_df])

    # Drop the following columns: 'Srs' 'PS/G' 'PA/G'
    standings_df.drop(columns=['SRS', 'PS/G', 'PA/G', 'GB'], inplace=True)

    # Sort by W/L%
    standings_df.sort_values(by=['W/L%'], ascending=False, inplace=True)

    # Split the 'Team' column by space and take the second to last element
    standings_df['Team'] = standings_df['Team'].str.split(' ').str[-1]

    # Remove everything within parentheses in the 'Team' column
    standings_df['Team'] = standings_df['Team'].str.replace(r'\(.*\)', '').str.strip()

    # Reset the index
    standings_df.reset_index(drop=True, inplace=True)

    return standings_df

def adjust_picks_for_trades():
    traded_pick_dict = {
        'Lakers': 'Lakers 👉 Pelicans',
        'Timberwolves': 'Timberwolves 👉 Jazz',
        'Bulls': 'Bulls 👉 Magic',
        'Pelicans': 'Pelicans 👉 Lakers',
        'Wizards': 'Wizards 👉 Knicks',
        'Mavericks': 'Mavericks 👉 Knicks',
        'Cavaliers': 'Cavaliers 👉 Pacers',
        
    }

def determine_draft_order():
    base_odds = [14.0, 14.0, 14.0, 12.5, 10.5, 9.0, 7.5, 4.5, 4.5, 4.5, 1.8, 1.7, 1.0, 0.5]

    # Reverse the list
    base_odds.reverse()
    
    # Get the standings
    standings = get_standings()
    
    # Get the top 15 teams
    top_15 = standings.head(16)
    
    # Get the bottom 15 teams
    lottery_teams = standings.tail(14)

    # Add the base odds to lottery_teams
    lottery_teams['No. 1 odds'] = base_odds

    # Add none to the top 16 teams
    top_15['No. 1 odds'] = None

    # Concatenate the top 14 and bottom 14 teams
    draft_order = pd.concat([top_15, lottery_teams])
    
    # Reset the index
    draft_order.reset_index(drop=True, inplace=True)

    
    # return draft_order
    draft_order.sort_values(by=['W/L%'], ascending=True, inplace=True)

    print(draft_order)


determine_draft_order()