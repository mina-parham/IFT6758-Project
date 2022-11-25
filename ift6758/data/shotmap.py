import textwrap

import IPython.display
import ipywidgets as widgets
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from IPython.display import clear_output, display
from ipywidgets import interact, interact_manual
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.stats import gaussian_kde


# source: https://towardsdatascience.com/nhl-analytics-with-python-6390c5d3206d
def coor_fix(df):
    """

    Inputs:
        df: df of all the seasons without na.
    Outputs:
        df: with the adjusted coordinates.
    """

    df["coordinate_x"] = np.where(
        df["coordinate_x"] > 0,
        df["coordinate_x"],
        -df["coordinate_x"],
    )
    df["coordinate_y"] = np.where(
        df["coordinate_x"] > 0,
        df["coordinate_y"] + 42,
        -df["coordinate_y"] + 42,
    )
    return df


def final(df, team, year):
    """

    Inputs:
        df: df of all the seasons without na.
        team: String of the team's name
        year: int year to visualizae
    Outputs:
        df: with the adjusted coordinates.
    """

    df = df[df["coordinate_x"].notna()]
    df = df[df["coordinate_y"].notna()]
    df_new = coor_fix(df)

    main_grid = np.zeros((100, 85))
    team_grid = np.zeros((100, 85))

    df_year = df_new[df_new["game_id"].astype(str).str[:4].astype(int) == int(year)]
    team_names = df_year["team_away_name"].unique()
    team_names = np.unique(np.append(team_names, df_year["team_home_name"].unique()))

    for i, p in df_year.iterrows():
        main_grid[int(p["coordinate_x"]), int(p["coordinate_y"])] += 1

    main_grid = main_grid / len(team_names)

    for i, p in df_year[df_year["team_name"] == team].iterrows():
        team_grid[int(p["coordinate_x"]), int(p["coordinate_y"])] += 1

    final = team_grid - main_grid
    final_gaussian = gaussian_filter(final, sigma=4)

    return final_gaussian


def plot_shot(df, PATH):
    """

    Inputs:
        df: df of all the seasons without na.
        PATH: a file path to save the visualization's .html file
    Outputs:
        .html file and interactive visualization
    """
    teams_menu = []
    for year in df.keys():
        for team in df[year].keys():
            teams_menu.append(team + "-" + str(year))

    x_grid, y_grid = np.mgrid[0:100:100j, -42.5:42.5:85j]

    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=Image.open("../figures/nhl_rink.png"),
            xref="x",
            yref="y",
            x=-100,
            y=42.5,
            sizex=200,
            sizey=85,
            sizing="stretch",
            opacity=0.5,
            layer="above",
        )
    )
    iter_i = 0
    for i, year in df.items():
        for j, team in year.items():
            if iter_i < len(teams_menu):
                fig.add_trace(
                    go.Contour(
                        x=x_grid[:, 1],
                        y=y_grid[1, :],
                        z=np.rot90(np.fliplr(team)),
                        colorscale="Inferno",
                        reversescale=True,
                        connectgaps=False,
                        name=teams_menu[iter_i],
                        colorbar=dict(title="Excess shots per hour", titleside="right"),
                    )
                )
                iter_i += 1
            else:
                break

    teams_menu_new = []
    for i in range(len(teams_menu)):
        visibility = [False] * len(teams_menu)
        visibility[i] = True
        teams_menu_new.append(
            dict(
                label=teams_menu[i],
                method="update",
                args=[
                    {"visible": visibility},
                ],
            )
        )

    fig.update_layout(
        updatemenus=[
            go.layout.Updatemenu(active=0, buttons=list(teams_menu_new)),
        ]
    )
    fig.update_layout(
        title=dict(text="Shot Map for each Team and Season", yanchor="top")
    )

    fig.show()

    fig.write_html(PATH)
