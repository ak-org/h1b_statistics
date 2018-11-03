import pandas as pd
import os.path
import sys
class read_h1b_data():
    '''
    Purpose : Read the CSV file containing h1b related data
    Input Parameter : input filename
    Returns : dataframe containing csv data
    '''

    def __init__(self, filename):
        self.filename = filename

    def read_h1b_file(self):
        if os.path.isfile(self.filename):
            try:
                h1b_df = pd.read_csv(self.filename, sep = ";", warn_bad_lines=True, error_bad_lines=False, index_col=0)
                if __debug__:
                    print("*** Successfully Read input file : " + self.filename)
            except IOException:
                print("Error: Could not read file " + self.filename)
                h1b_df = pd.DataFrame()
        else:
            print("Error: Could not read file " + self.filename)
            h1b_df = pd.DataFrame()      
        if __debug__:
            print("Total Records : ", h1b_df.shape)
        return h1b_df    


## Unit test cases
## from src/ directory run following commands 
### python h1b_readfile.csv "../input/sample.csv" - test should pass
### python h1b_readfile.csv "../input/sample2.csv" - test should pass

if __name__ == "__main__":
    filename = sys.argv[1]
    print("input file is : ", filename)
    inp_file_df = read_h1b_data(filename)
    inp_file_df.read_h1b_file()
