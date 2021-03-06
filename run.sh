#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file 
#if your program was written in Python
#
#python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
python -O ./src/h1b_main.py --input="./input/h1b_input.csv" --output_occup="./output/top_10_occupations.txt" --output_state="./output/top_10_states.txt"

## to run with debugger 
## python ./src/h1b_main.py --input="./input/h1b_input.csv" --output_occup="./output/top_10_occupations.txt" --output_state="./output/top_10_states.txt"