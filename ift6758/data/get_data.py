import json
import os

import pandas as pd
import requests


def get_games_data(start: int, end: int, path: str) -> pd.DataFrame:
    """
    Input:
    start: int, formed using for the start of the year.
    end: int, formed using for the end of the year.
    folder_path:
    COMPLETE!!!
    """

    max_game_ID = 1272
    max_playoff = 420  # original 398 -> Changed to 420 as it seems that normally they play a 4th round in the final game (7), so it's possible to see 2017030417
    g_t = ["02", "03"]
    data = {}

    if end > 2020:
        raise RuntimeError("End year out of API range")
    for t in g_t:
        if t == "02":
            for year in range(start, end + 1):
                for i in range(1, max_game_ID):
                    path_file = (
                        f"{path}/{str(year)}/{str(year) + t +str(i).zfill(4)}.json"
                    )
                    url = (
                        "http://statsapi.web.nhl.com/api/v1/game/"
                        + str(year)
                        + t
                        + str(i).zfill(4)
                        + "/feed/live"
                    )
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        # game_content = json.loads(game_response.content)
                        if not os.path.isfile(path_file):
                            data[str(year) + t + str(i).zfill(4)] = game_response.json()
                            os.makedirs(os.path.dirname(path_file), exist_ok=True)
                            with open(path_file, "w+") as f:
                                json.dump(data[str(year) + t + str(i).zfill(4)], f)
                        elif os.path.isfile(path_file):
                            with open(path_file) as f:
                                data[str(year) + t + str(i).zfill(4)] = json.load(f)
                            f.close()
                            continue

                    else:
                        print(
                            f"Status code: {response.status_code} at gameID:{str(year) + t +str(i).zfill(4)}, not found"
                        )

        else:
            for year in range(start, end + 1):
                for i in range(111, max_playoff):
                    path_file = (
                        f"{path}/{str(year)}/{str(year) + t +str(i).zfill(4)}.json"
                    )
                    url = (
                        "http://statsapi.web.nhl.com/api/v1/game/"
                        + str(year)
                        + t
                        + str(i).zfill(4)
                        + "/feed/live"
                    )
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        if not os.path.isfile(path_file):
                            data[str(year) + t + str(i).zfill(4)] = game_response.json()
                            os.makedirs(os.path.dirname(path_file), exist_ok=True)
                            with open(path_file, "w+") as f:
                                json.dump(data[str(year) + t + str(i).zfill(4)], f)
                        else:
                            with open(path_file) as f:
                                data[str(year) + t + str(i).zfill(4)] = json.load(f)
                            f.close()
                            continue

                    else:
                        print(
                            f"Status code: {response.status_code} at gameID:{str(year) + t +str(i).zfill(4)}, not found"
                        )

    return pd.DataFrame.from_dict(data)
