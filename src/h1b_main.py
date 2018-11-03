from h1b_readfile import read_h1b_data
from h1b_process import h1b_process_no_pandas
from optparse import *

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
    '''
    main function performs following actions:
     - parse input parameters
     - calls h1b process class
     - calculates total count of certified cases 
     - calculates number of unique states
     - calculates number of unique occupations
     - calculates cases for each state/occupation, calculates percentage and saves the output in the file specified by the output parameters

    '''
    params = parse_input_params()
    (opt, args) = params.parse_args()
    h1b_datafile = opt.f_input
    h1b_state_ofilename = opt.f_output_state
    h1b_occupation_ofilename = opt.f_output_occup
    h1b = read_h1b_data(h1b_datafile)
    h1b_data = h1b.read_h1b_file()

    h1b = h1b_process_no_pandas(h1b_data, h1b_state_ofilename, h1b_occupation_ofilename)
    certified_cases_count = h1b.get_certified_cases_count()
    
    top10_states = h1b.find_top_state()
    h1b.save_to_states_file(top10_states, certified_cases_count, h1b_state_ofilename)

    top10_occupations = h1b.find_top_occupation()
    h1b.save_to_occupations_file(top10_occupations, certified_cases_count, h1b_occupation_ofilename)
    

if __name__ == "__main__":
    main()
    
    
