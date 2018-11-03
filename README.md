# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

Create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

# Approach

The program is written in Python. I followed the object oriented methods and created indepdent class for 
- reading data file
- processing data file

As instructed, the code does not use any external libraries such as numpy or pandas.

Testing was done on csv files available at this Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing)

# How to Run the program

From the h1b_statistics directory, run the following command : 
```
python -O ./src/h1b_main.py --input=<csv file name with full or relative path> --output_occup=<csv file name with full or relative path> --output_state=<csv file name with full or relative path>

## to run with debugger 
## python -O ./src/h1b_main.py --input=<csv file name with full or relative path> --output_occup=<csv file name with full or relative path> --output_state=<csv file name with full or relative path>
```
if no input and output parameters are specified, following default parameters are used.

input ='./input/h1b_input.csv'
output_state ='./output/top_10_states.txt'
output_occup = './output/top_10_occupations.txt'