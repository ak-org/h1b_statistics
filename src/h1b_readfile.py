import pandas as pd
import os.path
import sys

class read_h1b_data():
    '''
    Purpose : Read the CSV file containing h1b related data
    Input Parameter : input filename
    Returns : dataframe containing csv data
    '''
    def __sanitize_line(self, line):
        quote_start = False
        quote_end = True
        line = list(line)
        for i in range(len(line)):
            if line[i] == '"' and quote_start == False:
                quote_start = True
                quote_end = False
            elif  line[i]== '"' and quote_start == True:
                quote_end = True
                quote_start = False   
            if quote_start == True and quote_end == False and line[i] == ';':
                line[i] = ' '
                #print("".join(line))
        return "".join(line)

    def __init__(self, filename):
        self.filename = filename

    def read_h1b_file(self):
        h1b_data = []
        if os.path.isfile(self.filename):
            h1b_fd = open(self.filename, mode='r', encoding = "utf8")
            for line in h1b_fd:
                line = self.__sanitize_line(line)
                h1b_data.append(line.split(';'))
            if __debug__:
                if  len(h1b_data) > 0:
                    print("***** Successfully Read input file : " + self.filename)
                    print("***** Size = ", len(h1b_data))
                else:    
                    print("***** ERROR while reading input file : " + self.filename)
                    print("***** Size = ", len(h1b_data))
        else:
            print("***** Error : File Not found!")
        return h1b_data




## Unit test cases
## from src/ directory run following commands 
### python h1b_readfile.csv "../input/h1b_input.csv" - test should PASS
### python h1b_readfile.csv "../input/sample.csv" - test should FAIL

if __name__ == "__main__":
    filename = sys.argv[1]
    print("input file is : ", filename)
    inp_file_df = read_h1b_data(filename)
    inp_file_df.read_h1b_file()
