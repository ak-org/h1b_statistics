
import os.path
import sys
import io

class read_h1b_data():
    '''
    Purpose : Read the CSV file containing h1b related data
    Input Parameter : input filename
    Returns : array containing data (read from csv file)
    '''
    def __sanitize_line(self, line):
        '''
        Private Method

        This function removes semi-colon embedded within the strings enclosed by quotes.
        without this correction, the program is unable to parse the fields correctly.
        '''
        quote_start = False
        quote_end = True
        line = list(line)
        '''
        Parse the string one character at a time.
        When first " is encounter, quote_start is set to true and quote_finish is set to false
        while above condition is true, any semi-colon is replace by blank space
        once second quote is encountered, quote_start is set to flase, and quote_finish is set to true 
        this function does not handle the edge case of a scenario, when string contains just opening or closing quote 
        and not a pair of quotes.
        '''
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
        '''
        this method reads data from csv and returns it in as a python array 
        '''
        h1b_data = []
        if os.path.isfile(self.filename):
            with io.open(self.filename, mode='r', encoding = "utf8") as h1b_fd:
                ## read first line of the csv to read header and 
                ## determine number of expected columns per data row
                h1b_data.append(h1b_fd.readline().split(';'))
                columns_count = len(h1b_data[0])
                if __debug__:
                    print("Total columns = ",columns_count)
                for line in h1b_fd:
                    line = self.__sanitize_line(line)
                    ## if number of fields in data row are not same as number of columns in the header
                    ## assume data is this row is malfunctioned and skip this row
                    row_data = line.split(';')
                    if len(row_data) == columns_count:
                        h1b_data.append(row_data)
                # if less than 2 lines are read, csv data is corrupt      
                if  len(h1b_data) > 2:   
                    if __debug__:
                        print("***** Successfully Read input file : " + self.filename)
                        print("***** Size = ", len(h1b_data))
                else:
                    ## could not successfully parse csv file, return empty array 
                    h1b_data = []  
                    print("***** ERROR : Unable to read input file : " + self.filename)
        else:
            print("***** Error : Input File " + self.filename + " Not found!")
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
