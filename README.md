# RegionalCorrelation
Reference:
Zhenhui Li, Cheng You, Matthew Gonzales, Anna K. Wendt, Fei Wu, and Susan L. Brantley, 
Searching for Anomalous Methane in Shallow Groundwater near Shale Gas Wells. Journal of Contaminant Hydrology 195 (2016): 23-30.

Version 1 code is at here:
https://github.com/shawu810/RegionalCorrelation


## How to run the code:
1. Put your data under the data/ folder. The data should a csv file with the following format:
```
# input csv files the columns should be: 
# longitude, latitude, variable1, variable1 censor flag, variable 2, variable 2 censor flag
# all values need to numerical. 
# Censor flag takes value from 0 or 1. 0 being uncensored value and 1 being left censored value (<).
# example: 
#         -76.622689,41.94494,20.2,0,1795.712751,0
```
2. Run 
```bash
python main.py  -- This will load the default parameter settings. 
```



Run code with new parameterization:
Python main.py [your_config_file] -- This will load your own parameter settings


Here is a sample configuration file (sample.cfg). 
```
[IO Parameter]
# input csv files the columns should be: 
# longitude, latitude, variable1, variable1 censor flag, variable 2, variable 2 censor flag
# all values need to numerical. 
# Censor flag takes value from 0 or 1. 0 being uncensored value and 1 being left censored value (<).
# example: 
#         -76.622689,41.94494,20.2,0,1795.712751,0
input_path = data/data.csv 

# the output folder
output_path_prefix = output/


[Sliding Parameter]
step_size = 0.002
w_size = 0.05
measure = cenken
min_lng = -76.85
max_lng = -76.15
min_lat = 41.492
max_lat = 42.008
skip_thres = 10

[FLAGS]
null_flag = -10000000
```
