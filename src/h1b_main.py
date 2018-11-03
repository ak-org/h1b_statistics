from h1b_readfile import read_h1b_data
from h1b_process import h1b_process
from optparse import *
import pandas as pd




def parse_input_params():
    ## define default values

    SAMPLE_INPUT_FILE='../input/h1b_input.csv'
    OUTPUT_STATES_FILE='../output/top_10_states.txt'
    OUTPUT_OCCUP_FILE = '../output/top_10_occupations.txt'

    parser = OptionParser()
    parser.add_option("--input", type="string", dest="f_input", help="Input semi-colon seperate CSV data file name")
    parser.add_option("--output_state", type="string", dest="f_output_state", help="Output semi-colon seperate CSV data file name to store top 10 states")
    parser.add_option("--output_occup", type="string", dest="f_output_occup", help="Output semi-colon seperate CSV data file name to store top 10 occupations")
    parser.set_defaults(f_input=SAMPLE_INPUT_FILE, 
                        f_output_state=OUTPUT_STATES_FILE,
                        f_output_occup=OUTPUT_OCCUP_FILE)
    return parser

def main():
    params = parse_input_params()
    (opt, args) = params.parse_args()
    h1b_datafile = opt.f_input
    h1b_state_ofilename = opt.f_output_occup
    h1b_occupation_ofilename = opt.f_output_state

    h1b = read_h1b_data(h1b_datafile)
    h1b_dataframe = h1b.read_h1b_file()
    if h1b_dataframe.shape[0] > 0:
        h1b_state_df = h1b_process(h1b_dataframe, h1b_state_ofilename, h1b_occupation_ofilename)
        h1b_state_df.top_occupation()
        h1b_state_df.top_state()
        return 0
    else:
        print("FATAL ERROR OCCURRED WHILE READING INPUT FILE")
        return -1    

if __name__ == "__main__":
    main()
    
    
