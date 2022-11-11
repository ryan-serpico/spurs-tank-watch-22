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
    standings_df.sort_values(by=['W/L%'], ascending=True, inplace=True)

    # Split the 'Team' column by space and take the second to last element
    standings_df['Team'] = standings_df['Team'].str.split(' ').str[-1]

    # Remove everything within parentheses in the 'Team' column
    standings_df['Team'] = standings_df['Team'].str.replace(r'\(.*\)', '').str.strip()

    # Reset the index
    standings_df.reset_index(drop=True, inplace=True)

    print(standings_df)

get_standings()