import pandas as pd

def get_player_stats(year: int, player_type: str) -> pd.DataFrame:
    """

    Uses Pandas' built in HTML parser to scrape the tabular player statistics from
    https://www.hockey-reference.com/leagues/ . If the player played on multiple 
    teams in a single season, the individual team's statistics are discarded and
    the total ('TOT') statistics are retained (the multiple team names are discarded)

    Args:
        year (int): The first year of the season to retrieve, i.e. for the 2016-17
            season you'd put in 2016
        player_type (str): Either 'skaters' for forwards and defensemen, or 'goalies'
            for goaltenders.
    """

    if player_type not in ["skaters", "goalies"]:
        raise RuntimeError("'player_type' must be either 'skaters' or 'goalies'")
    
    url = f'https://www.hockey-reference.com/leagues/NHL_{year}_{player_type}.html'

    print(f"Retrieving data from '{url}'...")

    # Use Pandas' built in HTML parser to retrieve the tabular data from the web data
    # Uses BeautifulSoup4 in the background to do the heavylifting
    df = pd.read_html(url, header=1)[0]

    # get players which changed teams during a season
    players_multiple_teams = df[df['Tm'].isin(['TOT'])]

    # filter out players who played on multiple teams
    df = df[~df['Player'].isin(players_multiple_teams['Player'])]
    df = df[df['Player'] != "Player"]

    # add the aggregate rows
    df = df.append(players_multiple_teams, ignore_index=True)

    return df


def get_games_data(start:int, end:int, path:str):
    max_game_ID = 1272
    max_playoff = 398
    g_t = ['02','03']
    
    
    if end > 2020:
        raise RuntimeError('End year out of API range')
    for t in g_t:
        if t == '02':
            for year in range(start,end + 1):
                for i in range(1,max_game_ID):
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        game_content = json.loads(game_response.content)
                        path_file = path + str(year) + t +str(i).zfill(4) + '.json'
                        with open(path_file, "w+") as f:
                            json.dump(game_content, f)
        else:
             for year in range(start,end + 1):
                for i in range(111,max_playoff):
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        game_content = json.loads(game_response.content)
                        path_file = path + str(year) + t +str(i).zfill(4) + '.json'
                        with open(path_file, "w+") as f:
                            json.dump(game_content, f)
   
def get_games_data_2(start:int, end:int, path_reg:str, path_playoff:str):
    max_game_ID = 1272
    max_playoff = 398
    g_t = ['02','03']
    
    
    if end > 2020:
        raise RuntimeError('End year out of API range')
    for t in g_t:
        if t == '02':
            for year in range(start,end + 1):
                for i in range(1,max_game_ID):
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        game_content = json.loads(game_response.content)
                        path_file = path_reg + str(year) + t +str(i).zfill(4) + '.json'
                        with open(path_file, "w+") as f:
                            json.dump(game_content, f)
        else:
             for year in range(start,end + 1):
                for i in range(111,max_playoff):
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        game_content = json.loads(game_response.content)
                        path_file = path_playoff + str(year) + t +str(i).zfill(4) + '.json'
                        with open(path_file, "w+") as f:
                            json.dump(game_content, f)
    
