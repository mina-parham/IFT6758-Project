import pandas as pd
import numpy as np
from numpy.linalg import norm
import math

    
def tiidy(df) -> pd.DataFrame:
    """
    Clean the json files downloaded with get_data.py function

    df : pd.DataFrame
    Returns
    pd.DataFrame
        pandas DataFrame of the play-by-play data where each row is an play event.
        with column names:
            events_types: events of the type “shots” and “goals”, missed shots or blocked shots for now.
            DONE game_time: game time/period information
            DONE game_id: game ID
            DONE team_info: team information (which team took the shot)
            DONEis_shot: indicator if its a shot or a goal
            DONEcoordinates_x, coordinates_y: the on-ice coordinates
            DONEshooter_name, goalie_name: the shooter and goalie name (don’t worry about assists for now)
            DONEshot_type: shot type
            ****DONEempty_name: if it was on an empty net
            DONEstrength:  whether or not a goal was at even strength, shorthanded, or on the power play.
    """
    event_idx, period_time, period, game_id, team_away_name, team_home_name, is_goal, coordinate_x,\
    coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name,\
    event_type, last_type, last_coord_x,last_coord_y, last_period, last_period_time, rebound = ([] for i in range(22))
    for i in range(df.shape[1]):
        allplays_data = df.iloc[:,i]['liveData']['plays']['allPlays']
        for j in range(len(allplays_data)):
            if(allplays_data[j]['result']['eventTypeId'] == "SHOT" or allplays_data[j]['result']['eventTypeId'] == "GOAL"):
                event_type.append(allplays_data[j]['result']['eventTypeId'])
                period.append(allplays_data[j]['about']['period'])
                period_time.append(allplays_data[j]['about']['periodTime'])
                game_id.append(df.iloc[:,i].name)
                event_idx.append(allplays_data[j]['about']['eventIdx'])
                team_away_name.append(df.iloc[:,i]['gameData']['teams']['away']['name'])
                team_home_name.append(df.iloc[:,i]['gameData']['teams']['home']['name'])
                team_name.append(allplays_data[j]['team']['name'])
                is_goal.append(allplays_data[j]['result']['eventTypeId']=="GOAL")
                coordinate_x.append(allplays_data[j]['coordinates']['x'] if  'x' in allplays_data[j]['coordinates'] else np.nan)
                coordinate_y.append(allplays_data[j]['coordinates']['y'] if  'y' in allplays_data[j]['coordinates'] else np.nan)
                shot_type.append(allplays_data[j]['result']['secondaryType'] if 'secondaryType' in allplays_data[j]['result'] else np.nan)
                strength.append(allplays_data[j]['result']['strength']['name'] if allplays_data[j]['result']['eventTypeId'] == "GOAL" else np.nan)
                if (allplays_data[j]['players'][z]['playerType'] == "Shooter" or allplays_data[j]['players'][z]['playerType'] =='Scorer' for z in range(len(allplays_data[j]['players']))):
                    shooter_name.append([allplays_data[j]['players'][z]['player']['fullName'] for z in range(len(allplays_data[j]['players']))][0])
                if (allplays_data[j]['players'][z]['playerType']=="Goalie" for z in range(len(allplays_data[j]['players']))):
                    goalie_name.append([allplays_data[j]['players'][z]['player']['fullName'] for z in range(len(allplays_data[j]['players']))][0])
                empty_net.append(True if 'emptyNet' in allplays_data[j]['result'] and allplays_data[j]['result']['emptyNet']==True else False)
                if j> 0:
                    last_type.append(allplays_data[j-1]['result']['eventTypeId'])
                    last_period.append(allplays_data[j-1]['about']['period'])
                    last_period_time.append(allplays_data[j-1]['about']['periodTime'])
                    last_coord_x.append(allplays_data[j-1]['coordinates']['x'] if  'x' in allplays_data[j-1]['coordinates'] else np.nan)
                    last_coord_y.append(allplays_data[j-1]['coordinates']['y'] if  'y' in allplays_data[j-1]['coordinates'] else np.nan)
                    rebound.append(allplays_data[j-1]['result']['eventTypeId']=="SHOT")
                        
                            
                else:
                    last_type.append(np.nan)
                    last_period.append(np.nan)
                    last_period_time.append(np.nan)
                    last_coord_x.append(np.nan)
                    last_coord_y.append(np.nan)
                    rebound.append(np.nan)
                


    assert(all(len(lists) == len(game_id) for lists in [event_idx, period_time, period, team_away_name, team_home_name, is_goal, coordinate_x,\
    coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name,\
    event_type, last_type, last_coord_x,last_coord_y, last_period, last_period_time, rebound]) )

    df_main = pd.DataFrame(np.column_stack([event_idx, period_time, period, game_id, team_away_name, team_home_name, is_goal, coordinate_x,\
    coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name,\
    event_type, last_type, last_coord_x,last_coord_y, last_period, last_period_time, rebound]),
                            columns=['event_idx', 'period_time', 'period', 'game_id', 'team_away_name', 'team_home_name','is_goal', 'coordinate_x',
                                    'coordinate_y', 'shot_type', 'strength', 'shooter_name','goalie_name', 'empty_net', 'team_name',
                                    'event_type', 'last_type', 'last_coord_x','last_coord_y', 'last_period', 'last_period_time', 'rebound'])
    
    df_main['coordinate_x'] = df_main['coordinate_x'].astype('float')
    df_main['coordinate_y'] = df_main['coordinate_y'].astype('float')
    df_main['last_coord_x'] = df_main['last_coord_x'].astype('float')
    df_main['last_coord_y'] = df_main['last_coord_y'].astype('float')
    df_main['is_goal'].replace({'False': 0, 'True': 1}, inplace=True)
    df_main['empty_net'].replace({'False': 0, 'True': 1}, inplace=True)
    df_main['distance'] = distance(df_main['coordinate_x'], df_main['coordinate_y'])
    df_main['from_last_distance']  = np.sqrt((df_main['coordinate_x'] - df_main['last_coord_x'])**2 + (df_main['coordinate_y'] - df_main['last_coord_y'])**2)

    df_main['angle'] = angle_between(df_main['coordinate_x'], df_main['coordinate_y'])
    df_main['last_angle'] = angle_between(df_main['last_coord_x'], df_main['last_coord_y'])
    df_main = convert_date(df_main)
    df_main = change_angle(df_main)

    return df_main


    
                 
def change_angle(df):
    change_angle = []
    speed = []
    for i in range(len(df['coordinate_x'])):
        if (df['rebound'][i]=='True'):
            x= df['angle'][i] - df['last_angle'][i]
            x -= 360 if x > 180 else 0
            x += 360 if x < -180 else 0
            change_angle.append(x)
            speed.append(x / df['time_from_last'][i])
        
        else:
             change_angle.append(0)
             speed.append(0)
            
    df['change_angle'] = change_angle
    df['speed'] = speed
    return df

def distance(x_coor, y_coor):
    """
    Computes the distances between the pock and the goal's center
    Inputs:
    x_coor: It takes the x coordinates
    y_coor: It takes the y_coordinates
    Outputs:
    distance: List of all the distances of all the coordinates present in the data frame
    """
    center_goal = (89, 0)
    x_distance_main = []
    for i in x_coor:
        x_distance = lambda i : center_goal[0] - i if i > 0  else -center_goal[0] - i
        x_distance_main.append(x_distance(i))
    distance = np.round_((np.sqrt(np.asarray(x_distance_main) **2 + (center_goal[1] - y_coor)**2)),decimals=4)
    return distance

def angle_between(x_coor, y_coor):
    """ 
    Returns the angle in radians between vectors 'v1 = (x_coor,y_coor)' and 'v2 (+/-89,0) -> Center of the net (left/right)'
    """
    center_goal_1 = [89,0]
    center_goal_2 = [-89,0]
    angles = []
    for i in range(len(x_coor)):
        p_v = [x_coor[i],y_coor[i]]
        if x_coor[i] > 0:
            v2 = center_goal_1
        else:
            v2 = center_goal_2
        if y_coor[i] == v2[1]:
            angle = 0.0
        else:
            angle = np.round_((np.arccos(np.dot(p_v,v2)/(norm(p_v)*norm(v2)))), decimals=4)
        angles.append(angle)
    return angles

    
def convert_date(df):
    time_1 = df['period_time'].str.split(':', expand=True).astype(int)
    time_2 = df['last_period_time'].str.split(':',expand=True).astype(int)
    time_period_1 = (df['period'].astype(int)-1)*1200
    time_period_2 = (df['last_period'].astype(int)-1)*1200
    df['time_from_last'] = (time_1[0]*60+time_1[1] + time_period_1) - (time_2[0]*60+time_period_1[1] + time_period_2)
    
    return df



