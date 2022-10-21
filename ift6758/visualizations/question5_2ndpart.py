# Algorithm
#Step 1
# Calculate the distance of the given (x,y) co-ordinates from the opposite team rink's goal post co-ordinates (i.e., (89,0) or (-89,0)). Do this for all the events given in the csv file.'
import os
import csv
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import numpy as np

game_types = ['regular', 'playoff']
#game_types = ['regular']
#years = [2016, 2017, 2018, 2019]
list_years = [2018,2019,2020]
''' Distance is a continous random variable for which determining a discrete quantity is impossible '''
''' Compute the range of continous random variable '''

min_dist_from_shot_to_oppgoalpost = 0.0
''' Maximum distance from where shot can be taken will be the hypotenuse distance. 
Shot will take from (-+89, -+42.5) depending on which side is the opposide goal side
of the event team and it will take upto (-+89, 0) which are the co-ordinates for the goal side.'''
max_dist_from_shot_to_oppgoalpost = ((89+89)**2+(42.5)**2)**0.5

print("Min distance to take any shot from the opposite side goal post (in feet):", min_dist_from_shot_to_oppgoalpost)
print("Max distance to take any shot from the opposite side goal post (in feet):", max_dist_from_shot_to_oppgoalpost)
range_dist =  max_dist_from_shot_to_oppgoalpost - min_dist_from_shot_to_oppgoalpost
print("Range of distance (max-min) (in feet) :", range_dist)

bin_width=15
print("Bin width (in feet) :", bin_width)

print("Bins of the histogram : ")
bin_marking = 0
bar_plot_bin_marking_mapping = dict()

discrete_labels = 'distanceBin'
label_counter = 0
bin_markings = list()
while bin_marking <= range_dist:
	bin_marking = round(bin_marking + bin_width,2)
	bar_plot_bin_marking_mapping[discrete_labels+str(label_counter)] = bin_marking
	label_counter +=1
	bin_markings.append(bin_marking)

print("Bin Markings :", bin_markings)
for game in game_types:
	plt.figure(game)
	visualization_dict = dict()
	for year in years:
		print("Season Year:", year)
		sample_space_dist = list()
		sample_space_events = list()
		
		file_number = 0
		files_list = os.listdir(f'./{game}/{year}')
		for file in files_list:
			print("[",game,"][",year,"]Read ",round((file_number/len(files_list))*100,2),"% files.",sep="")
			input_file = f'./{game_type}/{year}/{file}'

            if input_file[-4:] == '.csv':
					df = pd.read_csv(input_file)
					file_number = file_number+1

					num_rows = df.shape[0]
					impt_columns = ['Event', 'Period', 'Event Team Name', 'Home Team Name', 'Home Rink Side', 'X-Coordinate', 'Y-Coordinate']
					for row_id in range(num_rows):
						
						row_series = df.iloc[row_id] # 'pandas.core.series.Series' object
						
						sub_row_series = row_series[impt_columns] # 'pandas.core.series.Series' object
						
						
						req_columns = ['Event Team Name', 'Home Team Name']
						''' Determine the goal post coordinates '''
						goalpost_y_cor = 0
						if (sub_row_series['Event Team Name']) == (sub_row_series['Home Team Name']):
							if sub_row_series['Home Rink Side'] == 'left':
								
								
								if sub_row_series['Period'] % 2 == 1:
									 
									goalpost_x_cor = 89
								else:
									
									goalpost_x_cor = -89
							else:
								
								
								if sub_row_series['Period'] % 2 == 1:
									goalpost_x_cor = -89
								else:
									goalpost_x_cor = 89
						else:
							if sub_row_series['Home Rink Side'] == 'left':
								
								
								if sub_row_series['Period'] % 2 == 1:
									goalpost_x_cor = -89
								else:
									
									goalpost_x_cor = 89
							else:
								
								
								if sub_row_series['Period'] % 2 == 1:
									goalpost_x_cor = 89
								else:
									
									goalpost_x_cor = -89
									
						
						shot_x_coordinate = sub_row_series['X-Coordinate']
						shot_y_coordinate = sub_row_series['Y-Coordinate']
						
						distance = ((shot_x_coordinate - goalpost_x_cor)**2 + (shot_y_coordinate - goalpost_y_cor)**2)**0.5
						
						
						sample_space_dist.append(distance)
						
						sample_space_events.append(subset_row_series['Event'])
						

		
		total_outcomes_in_samplespace = len(sample_space_dist)
		print("[",game_type,"][",year,"]Total number of distances :", total_outcomes_in_samplespace,sep="")
		
		
		
		
		print("Total number of shots :", len(sample_space_dist))
		
			
		label_counter = 0
		shot_counter = 0
		bar_plot_shot_data = dict()
		bar_plot_goal_data = dict()
		sorted_bin_markings = sorted(bin_markings)
		
		for distance, event in zip(sample_space_dist, sample_space_events):
			for i in range(len(sorted_bin_markings)-1):
				lower_bin_marking = sorted_bin_markings[i]
				higher_bin_marking = sorted_bin_markings[i+1]
				if distance >=  lower_bin_marking and distance <= higher_bin_marking :
					
					for _key in bar_plot_bin_marking_mapping.keys():
						if bar_plot_bin_marking_mapping[_key] == lower_bin_marking:
							key = _key
							
							if key not in bar_plot_shot_data.keys():
								bar_plot_shot_data[key] = 0
							
							bar_plot_shot_data[key] +=1
							if event == 'Goal' :
								if (key not in bar_plot_goal_data.keys()):
									bar_plot_goal_data[key] = 0
								
								bar_plot_goal_data[key] +=1
								
							
							break
						else:
							
							pass
							
		
		
		for key in bar_plot_bin_marking_mapping.keys():
			if key not in bar_plot_shot_data.keys():
				bar_plot_shot_data[key] = 0
			if key not in bar_plot_goal_data.keys():
				bar_plot_goal_data[key] = 0

		
		
        
		
		bar_plot_y_axis_values = list()
		
		
		
		for x_axis_value in sorted_bin_markings:
			for key, value in bar_plot_bin_marking_mapping.items():
				if x_axis_value == value:
					number_of_shots_taken = bar_plot_shot_data[key]
					number_of_goals = bar_plot_goal_data[key]
					
					if number_of_shots_taken:
						y_value_for_bar_plot = number_of_goals/number_of_shots_taken
						bar_plot_y_axis_values.append(y_value_for_bar_plot)
					else:
						bar_plot_y_axis_values.append(0)
					break
				else:
					
					pass
			
		print("~~~~~~~~~~~~End of Game Type(",game_type,") Season Year(",year,")~~~~~~~~~~~~~~~~",sep="")
		if str(year)  not in visualization_dict.keys():
			visualization_dict[str(year)] = bar_plot_y_axis_values
		
	print("Input data for visualization looks like this :")
	
	visualization_dataframe = pd.DataFrame(visualization_dict, index=bin_markings)
	print(visualization_dataframe)
	visualization_dataframe.plot(kind="bar")
	plt.title("Chance of shot being a goal within a range of distance")
	plt.xlabel("Distance between shot position and goal post (in feet)")
	plt.ylabel("Goals/Shots")
	plt.xticks(rotation=90)
	
	''' draw as many figures as you want at once '''
	plt.draw()
	
	print("End of Game Type(", game_type,")", sep="")

''' all the figures which were drawn can now be shown '''
plt.show()

