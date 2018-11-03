
import os.path
import sys
import io

class h1b_process_no_pandas():
    '''
    process h1b data stored in a python array 
    as instructed, no pandas, numpy or other external library is used

    Assumption : STATUS Field will always be the 3rd column in the input data files.
                 If this assumption changes, a method will be needed to detect the column location for STATUS field as well.

    Methods:
        private methods
        ---------------
        ___init___ : initializes five different variables
        __find_col_idx_state : Method to find the column id of field containg work site state. 
                               Location can change between files
        __get_states_list: iterates through the array to create unique list of states
        __find_col_idx_occupation : Method to find the column id of field containg occupation's title. 
                                    Location can change between files
        __get_occupations_list: iterates through the array to create unique list of occupations
      
        public methods
        --------------
        get_certified_cases_count : Iterates through the array and calculates total number of 'CERTIFIED' cases
        find_top_states : Parses the data to calculate certified cases per state. It also sorts the table in descending order of cases
                          In case of tie, the state names are sorted alphabetically in the Ascending order
        save_to_states_file : Stores the state, case count and percent in the output file, by default in output/top_10_states.txt
                              Upto first 10 entries are written to the file
        find_top_occupations : Parses the data to calculate certified cases per state. It also sorts the table in descending order of cases
                          In case of tie, the state names are sorted alphabetically in the Ascending order
        save_to_occupations_file : Stores the occupation, case count and percent in the output file, by default in output/top_10_occupations.txt
                              Upto first 10 entries are written to the file

        
    '''

    def __init__(self, h1b_data, state_output_filename, occup_output_filename):
        self.h1b_data = h1b_data
        self.state_output_filename = state_output_filename
        self.occup_output_filename = occup_output_filename
        self.state_idx = 0
        self.occup_idx = 0
        
    def get_certified_cases_count(self):
        count = 0
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                count = count + 1
        if __debug__:
            print("Certified Case count : ", count)    
        return count   

    def __find_col_idx_state(self):
        if 'WORKSITE_STATE' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('WORKSITE_STATE')  
        elif 'LCA_CASE_WORKLOC1_STATE' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('LCA_CASE_WORKLOC1_STATE') 
        if __debug__:
            print("Column idx : ", idx, self.h1b_data[0][idx]) 
        return idx 


    def __get_states_list(self):
        states_list = []
        self.state_idx = self.__find_col_idx_state()
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                states_list.append(self.h1b_data[i][self.state_idx])
        if __debug__:
            print("total states : ", len(states_list))
        return states_list
    '''
       In the following method, dictionary's key-values are reversed to faciliate sorting of states field in case of a tie
    '''
    def find_top_state(self):
        top_10_keystore = {}
        states_list = self.__get_states_list()
        for state in states_list:
            top_10_keystore[state] = 0

        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                idx = states_list.index(self.h1b_data[i][self.state_idx])
                top_10_keystore[states_list[idx]] += 1
        top_10_keystore = sorted(top_10_keystore.items(), key = lambda x: x[1], reverse = True)
        reverse_state_keystore = {}
        for k,v in top_10_keystore:
            if v in reverse_state_keystore:
                reverse_state_keystore[v].append(k)
            else:
                reverse_state_keystore[v] = [k]
        for k in reverse_state_keystore:
            reverse_state_keystore[k] = sorted(reverse_state_keystore.get(k))

        if __debug__:
            print("key store for states : ",  reverse_state_keystore)
        return reverse_state_keystore
        

    def save_to_states_file(self, keystore, count, state_filename):
        ### File header : TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        if os.path.isfile(state_filename):
             print("*** WARNING : File already exists. " + state_filename)
        try:
            with io.open(state_filename, 'w') as state_file_fd:
                state_file_fd.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
                written_lines = 0
                for k in keystore:
                    percent = (k/count) * 100.00
                    str_percent = str(percent) + '%'
                    v = keystore.get(k)
                    for i in range(len(v)):
                        state_file_fd.write("{0};{1};{2}\n".format(v[i],k,str_percent))
                        written_lines += 1
                        if (written_lines == 10):
                            return
        except IOError:
            print("***** Error : Unable to create output file " + state_filename)
        return

    def __find_col_idx_occupation(self):
        if 'SOC_NAME' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('SOC_NAME')  
        elif 'LCA_CASE_SOC_NAME' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('LCA_CASE_SOC_NAME') 
        if __debug__:
            print("Occupation idx : ", idx, self.h1b_data[0][idx]) 
        return idx   

    def __get_occupations_list(self):
        occupations_list = []
        self.occup_idx = self.__find_col_idx_occupation()
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                self.h1b_data[i][self.occup_idx] = self.h1b_data[i][self.occup_idx].strip('\"')
                occupations_list.append(self.h1b_data[i][self.occup_idx])
        if __debug__:
            print("total occupations : ", len(occupations_list))
        return occupations_list

    '''
       In the following method, dictionary's key-values are reversed to faciliate sorting of occupation field in case of a tie
    '''
    def find_top_occupation(self):
        top_10_keystore = {}
        occupations_list = self.__get_occupations_list()
        for occupation in occupations_list:
            top_10_keystore[occupation] = 0

        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                idx = occupations_list.index(self.h1b_data[i][self.occup_idx])
                top_10_keystore[occupations_list[idx]] += 1
        top_10_keystore = sorted(top_10_keystore.items(), key = lambda x: x[1], reverse = True)
        reverse_state_keystore = {}
        for k,v in top_10_keystore:
            if v in reverse_state_keystore:
                reverse_state_keystore[v].append(k)
            else:
                reverse_state_keystore[v] = [k]
        for k in reverse_state_keystore:
            reverse_state_keystore[k] = sorted(reverse_state_keystore.get(k))

        return reverse_state_keystore

    def save_to_occupations_file(self, keystore, count, occup_filename):
        ## File header : TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        if os.path.isfile(occup_filename):
            print("*** WARNING : File already exists. " + occup_filename)
        try:
            with io.open(occup_filename, 'w') as occup_file_fd:
                occup_file_fd.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
                written_lines = 0
                for k in keystore:
                    percent = (k/count) * 100.00
                    str_percent = str(percent) + '%'
                    v = keystore.get(k)
                    for i in range(len(v)):
                        occup_file_fd.write("{0};{1};{2}\n".format(v[i],k,str_percent))
                        written_lines += 1
                        if (written_lines == 10):
                            return
        except IOError:
            print("***** Error : Unable to create output file " + occup_filename)
        return        
