import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_title(left_team, right_team):                ##import both team names 
    #Input:
    #left_team: str, name of the team playing on the left side.
    #right_team: str, name of the team playing on the right side.
    title_max_length = 76
    
    spaces_len = (title_max_length - len(left_team) - len(right_team)) // 2      ##TO set  title alignment 
    
    return left_team + (' ' * spaces_len) + right_team

def plot_event(coordinates, left_team, right_team):    

    #Input:
    #coordinates: tupple, it takes a tupple of integers signaling the x,y coordinates of the event.
     #left_team: str, name of the team playing on the left side. The value is assigned based on the place where the play took place. ie. Canadiens vs Toronto .If the team responsible for the event is Canadiens and x is negative, the lef team is Toronto.
    #right_team: str, name of the team playing on the right side. The value is assigned based on the place where the play took place. ie. Canadiens vs Toronto .If the team responsible for the event is #Canadiens and x is negative, the right team is Canadiens.
    
    #Output:
    #- A plot of the play made in the rink image
    
    data = plt.imread('../figures/nhl_rink.png')     ## TO plot image

    x_min = -100                      ## TO Set axis 
    x_max = 100
    y_min = -42.5    
    y_max = 42.5

    plt.imshow(data, extent=[x_min, x_max, y_min, y_max])      ## TO plot graph

    ax = plt.gca()
    ax.set_facecolor('m')
    ax.set_title(get_title(left_team, right_team))   ##TO set team name on both side 

    x_step = 25.0
    y_step = 21.25
    ax.set_xticks(np.arange(x_min, x_max + 1, x_step))
    ax.set_yticks(np.arange(y_min, y_max + 1, y_step))

    if len(coordinates) > 1:                                                                   ##input cordinates 
        ax.scatter([coordinates['x']], [coordinates['y']], marker='8', color='b', s=[120])   ##plot cordinates 

    plt.show()
    
    