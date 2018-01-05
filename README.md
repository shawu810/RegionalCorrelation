# RegionalCorrelation
Reference:
Zhenhui Li, Cheng You, Matthew Gonzales, Anna K. Wendt, Fei Wu, and Susan L. Brantley, 
Searching for Anomalous Methane in Shallow Groundwater near Shale Gas Wells. Journal of Contaminant Hydrology 195 (2016): 23-30.

Version 1 code is at here:
https://github.com/shawu810/RegionalCorrelation

# How to run the code:
1. Specify parameters in the configuration file, e.g., sample.cfg.
2. Put your data under the directory specified in the configuration file (by input_path). The data should be a csv file with the following format:
```
# input csv files the columns should be: 
# longitude, latitude, variable1, variable1 censor flag, variable 2, variable 2 censor flag
# all values need to numerical. 
# Censor flag takes value from 0 or 1. 0 being uncensored value and 1 being left censored value (<).
# example: 
#         -76.622689,41.94494,20.2,0,1795.712751,0
#         -76.622689,41.94494,20.2,0,1795.712751,0
#         -76.622689,41.94494,20.2,0,1795.712751,0
#         ...
```
3. Run the code
```bash
python main.py [your_config_file]
```

Example:
To run code with defualt parameters:
1. Put data under the data folder and name the file data.csv
2. Run
```bash
python main.py sample.cfg
```
3. Outputs are in output folder

# Only run drawing code
Alternatively, you can only run the drawing code by:
```bash
python drawing.py [your_config_file]
```

# Sample configuration file:
Here is a sample configuration file (sample.cfg). 
```
[IO Parameter]
# Path to the input csv file. Take both absolute or relative path. 
input_path = data/data.csv 

# Output folder. Take both absolute or relative path. Will create new folder if not exist.
output_path_prefix = output/


[Sliding Parameter]
# Unit for parameters step_size and w_size is degree. 0.002 is approximately 220 meters, and 0.05 is approximately 5.5 km.
# Here we setp step_size to be 0.02 (2.2km) for testing run
step_size = 0.02 
w_size = 0.05

min_lng = -76.85
max_lng = -76.15
min_lat = 41.492
max_lat = 42.008
skip_thres = 10

# Only supports cenken now (censored value adjusted Kendall Tau)
measure = cenken


[Drawing Parameter]
tick_number = 10
tick_label_precision = 2
dpi = 500
```
