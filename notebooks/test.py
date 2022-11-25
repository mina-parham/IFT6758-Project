import sys

import pandas as pd

sys.path.append("../ift6758/data/")
from get_data import get_games_data
from tidy_data2 import tidy

data_test = get_games_data(2015, 2015, "./json")

data_train_test = tidy(data_test)
